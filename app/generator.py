"""
Generate a grounded answer from the user's question and retrieved chunks.
"""

from typing import List

import ollama

from app.config import GEN_MODEL, SYSTEM_PROMPT
from app.retriever import RetrievedChunk


def build_prompt(query: str, chunks: List[RetrievedChunk]) -> str:
    """
    Build the augmented prompt sent to the local LLM.
    """
    if not chunks:
        context_block = "(no relevant context was found)"
    else:
        context_block = "\n\n".join(
            f"[{index + 1}] Source: {chunk['source']}\n{chunk['text']}"
            for index, chunk in enumerate(chunks)
        )

    return (
        f"Context:\n{context_block}\n\n"
        f"Question: {query}\n\n"
        "Answer using only the context above. "
        "If there is not enough information in the context, say so."
    )


def generate_answer(
    query: str,
    chunks: List[RetrievedChunk],
) -> str:
    """
    Send the augmented prompt to the local Ollama generation model.
    """
    prompt = build_prompt(query, chunks)

    response = ollama.chat(
        model=GEN_MODEL,
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
    )

    return response.message.content 
