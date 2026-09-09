"""
Create embeddings with the local Ollama embedding model.
"""

from typing import List

import ollama

from app.config import EMBED_MODEL


def embed_texts(texts: List[str]) -> List[List[float]]:
    """
    Turn a batch of strings into vectors.
    """
    if not texts:
        return []

    response = ollama.embed(
        model=EMBED_MODEL,
        input=texts,
    )

    return list(response.embeddings)  # type: ignore


def embed_query(text: str) -> List[float]:
    """
    Embed one user question.
    """
    if not text.strip():
        raise ValueError("Query cannot be empty.")

    return embed_texts([text])[0]
