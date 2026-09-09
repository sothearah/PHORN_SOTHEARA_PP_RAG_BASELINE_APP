"""
Main entry point for the local Naive RAG application.

CLI:
    poetry run python -m app.main

Optional FastAPI server:
    poetry run uvicorn app.main:app --reload
"""

import logging

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.ingestion import build_index
from app.pipeline import ask

logging.getLogger("chromadb.telemetry.product.posthog").setLevel(logging.CRITICAL)

app = FastAPI(title="Local Naive RAG")


class ChatRequest(BaseModel):
    question: str
    top_k: int | None = None


class ChatResponse(BaseModel):
    answer: str
    sources: list[str]


@app.post("/ingest")
def ingest():
    """
    Rebuild the local vector index from documents in data/.
    """
    try:
        count = build_index()
    except FileNotFoundError as error:
        raise HTTPException(status_code=400, detail=str(error))

    return {"chunks_indexed": count}


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    """
    Answer one question through the full RAG pipeline.
    """
    if not request.question.strip():
        raise HTTPException(
            status_code=400,
            detail="question must not be empty",
        )

    result = ask(request.question, top_k=request.top_k)
    sources = sorted(
        {chunk["source"] for chunk in result["chunks"]}
    )

    return ChatResponse(
        answer=result["answer"],
        sources=sources,
    )


def run_cli() -> None:
    """
    Run a simple terminal chat loop.
    """
    print("Local Naive RAG Chat")
    print("Type 'exit' to quit.\n")

    while True:
        question = input("You: ").strip()

        if question.lower() == "exit":
            print("Goodbye!")
            break

        if not question:
            print("Please enter a question.\n")
            continue

        try:
            result = ask(question)
        except RuntimeError as error:
            print(f"\nError: {error}\n")
            continue

        print("\nRetrieved chunks:")
        for chunk in result["chunks"]:
            print(
                f"- [{chunk['source']} #{chunk['chunk_index']}] "
                f"distance={chunk['distance']:.4f}"
            )

        print(f"\nAssistant: {result['answer']}\n")


if __name__ == "__main__":
    run_cli()
