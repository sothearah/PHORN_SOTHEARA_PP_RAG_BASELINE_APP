"""
The whole app, end to end, exposed as a tiny API — no framework magic,
just three plain functions wired together.

Run it:
    poetry run uvicorn app.main:app --reload

Then test it with curl (see README.md for full examples):
    curl -X POST http://127.0.0.1:8000/ingest
    curl -X POST http://127.0.0.1:8000/chat -H "Content-Type: application/json" \
         -d '{"question": "What is the vacation policy?"}'
"""
import logging

logging.getLogger("chromadb.telemetry.product.posthog").setLevel(logging.CRITICAL)

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.generate import generate_answer
from app.ingest import build_index
from app.retrieval import retrieve

app = FastAPI(title="Baseline Chat-with-Documents API")


class ChatRequest(BaseModel):
    question: str
    top_k: int | None = None


class ChatResponse(BaseModel):
    answer: str
    sources: list[str]


@app.post("/ingest")
def ingest():
    """(Re)build the vector index from everything in data/."""
    try:
        count = build_index()
    except FileNotFoundError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"chunks_indexed": count}


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    """The full retrieve -> augment -> generate loop for one question."""
    if not req.question.strip():
        raise HTTPException(status_code=400, detail="question must not be empty")

    chunks = retrieve(req.question, top_k=req.top_k) if req.top_k else retrieve(req.question)
    answer = generate_answer(req.question, chunks)
    sources = sorted({c["source"] for c in chunks})
    return ChatResponse(answer=answer, sources=sources)

# add cli in termianl
def run_cli():
    print("Baseline RAG Chat")
    print("Type 'exit' to quit.\n")

    while True:
        question = input("You: ").strip()

        if question.lower() == "exit":
            print("Goodbye!")
            break

        if not question:
            print("Please enter a question.\n")
            continue

        chunks = retrieve(question)
        answer = generate_answer(question, chunks)

        print("\nRetrieved chunks:")
        for c in chunks:
            print(
                f"- [{c['source']} #{c['chunk_index']}] "
                f"distance={c['distance']:.4f}"
            )

        print(f"\nAssistant: {answer}\n")


if __name__ == "__main__":
    run_cli()