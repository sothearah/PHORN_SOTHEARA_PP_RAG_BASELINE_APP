"""
Given a question, retrieve the most relevant document chunks.
"""

from typing import List, TypedDict

from app.config import TOP_K
from app.embeddings import embed_query
from app.vector_store import search_collection


class RetrievedChunk(TypedDict):
    text: str
    source: str
    chunk_index: int
    distance: float


def retrieve(query: str, top_k: int = TOP_K) -> List[RetrievedChunk]:
    """
    Embed the query and retrieve top-k nearest chunks from ChromaDB.
    """
    if not query.strip():
        return []

    query_embedding = embed_query(query)
    results = search_collection(query_embedding, top_k)

    documents = results["documents"][0]  # type: ignore
    metadatas = results["metadatas"][0]  # type: ignore
    distances = results["distances"][0]  # type: ignore

    chunks: List[RetrievedChunk] = []

    for text, metadata, distance in zip(
        documents,
        metadatas,
        distances,
    ):
        chunks.append(
            {
                "text": text,
                "source": metadata.get("source", "unknown"),
                "chunk_index": metadata.get("chunk_index", -1),
                "distance": float(distance),
            }
        )

    return chunks
