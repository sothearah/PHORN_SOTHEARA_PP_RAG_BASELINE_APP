"""
Connect retrieval and generation into one online RAG flow.

Question -> retrieve relevant chunks -> generate grounded answer.
"""

from typing import TypedDict, List

from app.generator import generate_answer
from app.retriever import RetrievedChunk, retrieve


class RAGResult(TypedDict):
    question: str
    answer: str
    chunks: List[RetrievedChunk]


def ask(question: str, top_k: int | None = None) -> RAGResult:
    """
    Run one complete RAG question-answer cycle.
    """
    if not question.strip():
        raise ValueError("Question cannot be empty.")

    chunks = retrieve(question, top_k=top_k) if top_k else retrieve(question)
    answer = generate_answer(question, chunks)

    return {
        "question": question,
        "answer": answer,
        "chunks": chunks,
    }
