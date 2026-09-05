# Baseline Chat-with-Documents App

A minimal, hands-on RAG (Retrieval-Augmented Generation) pipeline exposed as a
real REST API with FastAPI. Every stage is a plain Python function you can read
top to bottom — nothing is hidden behind a framework's abstractions.

---

## What is RAG? (Read this first)

Large language models (LLMs) like Llama or Qwen are trained on public internet
data. They are smart at reasoning, but they know nothing about *your* documents
— your company policies, your research notes, your own data.

**RAG is the solution.** Instead of retraining the model (expensive, slow), RAG
retrieves the relevant pieces of *your* documents at query time and hands them
to the LLM as extra context in the prompt. The LLM then answers based on what
you gave it, not what it already knows.

The full loop has four stages:

```
Stage 1 — LOAD & CHUNK
  Your documents (.txt / .pdf) are split into small overlapping chunks
  (e.g. 800 characters each). Smaller pieces are easier to match against
  a specific question.

Stage 2 — EMBED & STORE
  Each chunk is converted into a vector (a list of numbers that captures
  meaning) by an embedding model. The vectors are stored in a vector
  database (ChromaDB). This is the "index".

Stage 3 — RETRIEVE
  When the user asks a question, the question is also embedded into a
  vector. The vector DB finds the chunks whose vectors are closest to the
  question vector (semantic similarity, not keyword match).

Stage 4 — GENERATE
  The top-k retrieved chunks + the original question are assembled into a
  prompt and sent to the LLM. The LLM generates an answer grounded only
  in those chunks.
```

Key insight: the model never "searches" anything. It only reads what you put
in front of it. RAG is the system that decides *what* to put in front of it.

---

## Architecture of This App

```
data/*.txt, *.pdf
        |
  [app/ingest.py]          ← Stage 1 & 2: chunk, embed, store
        |
  chroma_db/               ← persisted vector index
        |
        |←── user question
  [app/retrieval.py]       ← Stage 3: embed question, find top-k chunks
        |
  top-k chunks + question
        |
  [app/generate.py]        ← Stage 4: build prompt, call Ollama LLM
        |
  grounded answer
```

All of this is wired together in `app/main.py` as a FastAPI application with
three HTTP endpoints — making the whole pipeline accessible from any client
(browser, mobile app, Postman, another service).

---

## Prerequisites

### 1. Ollama (local LLM server)

Ollama runs LLMs locally on your machine. Install it from [ollama.com](https://ollama.com),
then pull the two models this app needs:

```bash
ollama pull nomic-embed-text   # embedding model (Stage 2 & 3)
ollama pull qwen3:8b           # generation model (Stage 4)
```

Verify Ollama is running:
```bash
ollama list   # should show both models
```

### 2. Poetry (Python package manager)

Poetry manages Python dependencies cleanly. Install it once:
```bash
pipx install poetry
```

Or check [python-poetry.org](https://python-poetry.org) for other install options.

---

## Setup

```bash
cd rag-baseline-app
poetry install        # installs all dependencies into an isolated virtual env
```

---

## Running the App — Step by Step

### Step 1: Build the Index

This reads all files in `data/`, splits them into chunks, embeds them, and
stores them in `chroma_db/`. You must do this before asking any questions.

```bash
poetry run python -m app.ingest
```

Expected output:
```
Indexed 8 chunks from 'data/' into Chroma at 'chroma_db/'.
```

> **To use your own documents:** drop `.txt`, `.md`, or `.pdf` files into
> `data/`, delete the old `chroma_db/` folder, and re-run this command.

### Step 2: Start the API Server

```bash
poetry run uvicorn app.main:app --reload
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

The `--reload` flag means the server restarts automatically when you save a
file — great for development.

### Step 3: Test the API

Open a new terminal tab (keep the server running) and try these commands:

**Health check — is the server alive?**
```bash
curl http://127.0.0.1:8000/health
```

**Re-trigger ingestion over HTTP** (same as Step 1, but via the API):
```bash
curl -X POST http://127.0.0.1:8000/ingest
```

**Ask a question:**
```bash
curl -X POST http://127.0.0.1:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "How many in-office days per week do hybrid employees need?"}'
```

Expected response shape:
```json
{
  "answer": "Hybrid employees are required to be in the office at least 2 days per week...",
  "sources": ["remote_work_policy.txt"]
}
```

**Ask something the documents cannot answer:**
```bash
curl -X POST http://127.0.0.1:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the CEO home address?"}'
```

A well-grounded system should reply: *"I don't have enough information in the
documents to answer that."* — not make something up. If it hallucinates, look
at the `SYSTEM_PROMPT` in `app/config.py` — that's what controls this behaviour.

### Step 4: Inspect Retrieval Quality

```bash
poetry run python -m scripts.test_queries
```

This runs several preset questions and prints, for each one:
- which chunks were retrieved
- their similarity distance scores
- the final generated answer

Read the raw retrieved chunks. If the answer is wrong, the problem is almost
always here — the wrong chunk was retrieved, not the LLM making things up. This
is the most important debugging skill in RAG.

---

## How FastAPI Turns RAG into a Real API

Without FastAPI, the RAG pipeline is just Python functions you call in a
script. FastAPI wraps those functions so any client — a web app, mobile app,
or another backend service — can use them over HTTP.

Here is what happens when you hit `/chat`:

```
POST /chat  {"question": "..."}
        |
  app/main.py  →  retrieve(question)   # calls retrieval.py
                →  generate_answer(question, chunks)  # calls generate.py
                →  returns JSON response
```

Look at `app/main.py` — the entire API is about 50 lines. Notice:

- **`BaseModel` (Pydantic):** FastAPI automatically validates the request body
  against `ChatRequest`. If a required field is missing or the wrong type, it
  returns a clear error — you don't write any validation code yourself.
- **`response_model=ChatResponse`:** FastAPI serializes the return value to
  JSON and validates its shape before sending it. The client always gets a
  predictable structure.
- **Automatic docs:** FastAPI generates interactive documentation at
  `http://127.0.0.1:8000/docs` — open it in a browser and you can try all
  endpoints without curl.

The interactive docs URL (try it now):
```
http://127.0.0.1:8000/docs
```

---

## Project Layout

```
app/
  config.py       ← every tunable value in one place: models, chunk size, top_k, system prompt
  embeddings.py   ← embed_texts() / embed_query() — shared by ingest and retrieval
  ingest.py       ← load_documents(), chunk_text(), build_index() — Stages 1 & 2
  retrieval.py    ← retrieve() — embed the question, query ChromaDB — Stage 3
  generate.py     ← build_prompt(), generate_answer() — augmentation + LLM call — Stage 4
  main.py         ← FastAPI app: /health, /ingest, /chat
data/             ← source documents (swap in your own .txt / .pdf files)
chroma_db/        ← auto-generated vector index (do not edit manually)
scripts/
  test_queries.py ← sample questions + retrieval/answer inspection tool
```

---

## All the Knobs You Can Turn (in `app/config.py`)

| Setting | Default | What it does |
|---|---|---|
| `EMBED_MODEL` | `nomic-embed-text` | Ollama model used for embedding |
| `GEN_MODEL` | `qwen3:8b` | Ollama model used for generation |
| `CHUNK_SIZE` | `800` | Characters per chunk |
| `CHUNK_OVERLAP` | `120` | Characters shared between adjacent chunks |
| `TOP_K` | `4` | How many chunks to retrieve per question |
| `SYSTEM_PROMPT` | (see file) | Instruction to the LLM about grounding |

---

## Live Experiments to Try with Students

1. **Chunk size experiment**
   Change `CHUNK_SIZE` from `800` to `200`, delete `chroma_db/`, re-run
   `app.ingest`, then ask questions that span two ideas. Watch retrieval
   quality change.

2. **Top-k experiment**
   Change `TOP_K` from `4` to `1`. Watch the model start missing context
   on multi-part questions.

3. **Hallucination experiment**
   Comment out the `SYSTEM_PROMPT` grounding instruction and ask an
   out-of-scope question. Watch the model make things up instead of saying
   "I don't know".

4. **Print the prompt**
   In `app/generate.py`, add `print(prompt)` before the Ollama call.
   Run a query and see exactly what the LLM receives — this demystifies
   "prompt augmentation" completely.

5. **Swap your own documents**
   Replace the files in `data/` with anything you like (meeting notes,
   textbook chapters, recipes). Re-run `app.ingest` and the whole pipeline
   immediately works on your new content.
