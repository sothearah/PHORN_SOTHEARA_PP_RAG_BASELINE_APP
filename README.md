# Baseline Chat-with-Documents RAG

## Overview

This project is a local **Naive Retrieval-Augmented Generation (RAG)** application built with Python, Ollama, and ChromaDB.

The application loads local documents, splits them into chunks, creates embeddings, stores them in a vector database, retrieves relevant chunks for a user question, and uses a local LLM to generate a grounded answer.

```text
Documents
   ↓
Ingestion & Chunking
   ↓
Embedding
   ↓
ChromaDB
   ↓
Retrieval
   ↓
Generation
   ↓
Answer
```

## Technologies

- Python
- Poetry
- Ollama
- ChromaDB
- FastAPI
- Uvicorn
- PyPDF

## Models

**Generation model:** `llama3.2`

```bash
ollama pull llama3.2
```

**Embedding model:** `nomic-embed-text`

```bash
ollama pull nomic-embed-text
```

The same embedding model is used for both document chunks and user questions.

---

## Project Structure

```text
RAG-BASELINE-APP/
│
├── app/
│   ├── config.py
│   ├── ingestion.py
│   ├── embeddings.py
│   ├── vector_store.py
│   ├── retriever.py
│   ├── generator.py
│   ├── pipeline.py
│   └── main.py
│
├── data/
├── scripts/
│   └── test_queries.py
│
├── README.md
├── test_log.md
├── reflection.md
├── requirements.txt
├── pyproject.toml
└── poetry.lock
```

## RAG Pipeline

### 1. Ingestion and Chunking

`app/ingestion.py`

Documents from `data/` are loaded and divided into chunks.

Supported formats:

- `.txt`
- `.md`
- `.pdf`

Current chunking configuration:

```python
CHUNK_SIZE = 800
CHUNK_OVERLAP = 120
```

The overlap helps preserve information that may occur near chunk boundaries.

### 2. Embedding

`app/embeddings.py`

Document chunks are converted into vectors using `nomic-embed-text`.

### 3. Vector Storage

`app/vector_store.py`

The embeddings, chunk text, source filename, and chunk index are stored persistently in ChromaDB.

### 4. Retrieval

`app/retriever.py`

The user's question is embedded and compared with stored vectors.

```python
TOP_K = 4
```

The four closest chunks are returned as context.

### 5. Generation

`app/generator.py`

The retrieved context and user question are sent to `llama3.2`.

The model is instructed to answer only from the provided context. If the answer is not available, it should say:

```text
I don't have enough information in the documents to answer that.
```

### 6. Pipeline

`app/pipeline.py`

Connects the retrieval and generation stages:

```text
Question → Retrieve → Generate → Answer
```

---

## Setup

Install dependencies:

```bash
poetry install
```

Install Ollama models:

```bash
ollama pull llama3.2
ollama pull nomic-embed-text
```

Verify:

```bash
ollama list
```

## Build the Vector Index

Place the source documents inside `data/`, then run:

```bash
poetry run python -m app.ingestion
```

This performs:

```text
Load → Chunk → Embed → Store
```

The current document collection produced **28 chunks**.

## Run the Application

Start the CLI:

```bash
poetry run python -m app.main
```

Ask questions and type:

```text
exit
```

to stop the application.

## Run Tests

```bash
poetry run python -m scripts.test_queries
```

The test script displays:

- question
- retrieved chunks
- source files
- vector distances
- generated answer

Detailed results are available in `test_log.md`.

## Optional FastAPI

Start the API:

```bash
poetry run uvicorn app.main:app --reload
```

Then open:

```text
http://127.0.0.1:8000/docs
```

Available endpoints:

- `POST /ingest`
- `POST /chat`

## Testing Summary

The system was tested with six questions, including document-related and out-of-scope questions.

It correctly answered questions about the home-office stipend and expense policy and refused questions whose answers were not contained in the documents.

One limitation was **retrieval noise**. For the onboarding question, an unrelated remote-work chunk was retrieved and introduced unnecessary information into the answer.

Future improvements could include **re-ranking, relevance filtering, semantic chunking, and hybrid retrieval**.

## Reflection

See `reflection.md` for the 150–300 word project reflection.