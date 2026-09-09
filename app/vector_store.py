"""
Store and search chunk vectors in persistent ChromaDB.
"""

import logging
from typing import List, Sequence

import chromadb
from chromadb.config import Settings

from app.config import CHROMA_DB_DIR, COLLECTION_NAME

logging.getLogger("chromadb.telemetry.product.posthog").setLevel(logging.CRITICAL)

_CHROMA_SETTINGS = Settings(anonymized_telemetry=False)


def get_client():
    """
    Return a persistent Chroma client.
    """
    return chromadb.PersistentClient(
        path=CHROMA_DB_DIR,
        settings=_CHROMA_SETTINGS,
    )


def get_collection():
    """
    Return the RAG document collection.
    """
    client = get_client()
    return client.get_or_create_collection(name=COLLECTION_NAME)


def rebuild_collection(chunks, embeddings: Sequence[Sequence[float]]) -> None:
    """
    Delete the existing collection, recreate it, and store all chunks.
    """
    client = get_client()

    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass

    collection = client.get_or_create_collection(name=COLLECTION_NAME)

    ids = [chunk["id"] for chunk in chunks]
    documents = [chunk["text"] for chunk in chunks]
    metadatas = [
        {
            "source": chunk["source"],
            "chunk_index": chunk["chunk_index"],
        }
        for chunk in chunks
    ]

    collection.add(
        ids=ids,
        documents=documents,
        embeddings=list(embeddings),
        metadatas=metadatas,
    )


def search_collection(
    query_embedding: List[float],
    top_k: int,
):
    """
    Search ChromaDB and return the nearest chunks.
    """
    collection = get_collection()

    if collection.count() == 0:
        raise RuntimeError(
            "The vector database is empty. "
            "Run `poetry run python -m app.ingestion` first."
        )

    return collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=["documents", "metadatas", "distances"],
    )
