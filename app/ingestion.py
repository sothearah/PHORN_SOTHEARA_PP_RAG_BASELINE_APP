"""
Load raw documents and split them into chunks.

Run this module to rebuild the vector index:
    poetry run python -m app.ingestion
"""

import os
from typing import List, Tuple, TypedDict

from pypdf import PdfReader

from app.config import DATA_DIR, CHUNK_SIZE, CHUNK_OVERLAP
from app.embeddings import embed_texts
from app.vector_store import rebuild_collection


class DocumentChunk(TypedDict):
    id: str
    text: str
    source: str
    chunk_index: int


def _read_text_file(path: str) -> str:
    with open(path, "r", encoding="utf-8") as file:
        return file.read()


def _read_pdf(path: str) -> str:
    reader = PdfReader(path)
    return "\n".join(page.extract_text() or "" for page in reader.pages)


def load_documents(data_dir: str = DATA_DIR) -> List[Tuple[str, str]]:
    """
    Load all supported documents from data_dir.

    Returns:
        [(filename, full_text), ...]
    """
    if not os.path.isdir(data_dir):
        raise FileNotFoundError(f"Data folder '{data_dir}' does not exist.")

    documents: List[Tuple[str, str]] = []

    for filename in sorted(os.listdir(data_dir)):
        path = os.path.join(data_dir, filename)

        if not os.path.isfile(path):
            continue

        extension = os.path.splitext(filename)[1].lower()

        if extension in {".txt", ".md"}:
            text = _read_text_file(path)
        elif extension == ".pdf":
            text = _read_pdf(path)
        else:
            continue

        if text.strip():
            documents.append((filename, text))

    return documents


def chunk_text(
    text: str,
    chunk_size: int = CHUNK_SIZE,
    overlap: int = CHUNK_OVERLAP,
) -> List[str]:
    """
    Split text into fixed-size character chunks with overlap.
    """
    text = text.strip()

    if not text:
        return []

    if overlap >= chunk_size:
        raise ValueError("CHUNK_OVERLAP must be smaller than CHUNK_SIZE.")

    chunks: List[str] = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])

        if end >= len(text):
            break

        start = end - overlap

    return chunks


def prepare_chunks(data_dir: str = DATA_DIR) -> List[DocumentChunk]:
    """
    Load documents and convert them into chunks with metadata.
    """
    documents = load_documents(data_dir)

    if not documents:
        raise FileNotFoundError(
            f"No .txt, .md, or .pdf documents found in '{data_dir}/'."
        )

    prepared: List[DocumentChunk] = []

    for filename, full_text in documents:
        chunks = chunk_text(full_text)

        for index, text in enumerate(chunks):
            prepared.append(
                {
                    "id": f"{filename}::{index}",
                    "text": text,
                    "source": filename,
                    "chunk_index": index,
                }
            )

    return prepared


def build_index(data_dir: str = DATA_DIR) -> int:
    """
    Offline RAG pipeline:
    load -> chunk -> embed -> store in ChromaDB.
    """
    chunks = prepare_chunks(data_dir)
    texts = [chunk["text"] for chunk in chunks]
    embeddings = embed_texts(texts)

    rebuild_collection(chunks, embeddings)

    return len(chunks)


if __name__ == "__main__":
    count = build_index()
    print(f"Indexed {count} chunks from '{DATA_DIR}/' into ChromaDB.")
