# Local Naive RAG — Chat with Documents

A local **Naive Retrieval-Augmented Generation (RAG)** application built with Python, Ollama, and ChromaDB.

The system retrieves information from local documents and uses a local LLM to answer questions based only on the retrieved context.

## RAG Flow

```text
Documents
    ↓
Load & Chunk
    ↓
Embedding
    ↓
ChromaDB
    ↓
Retrieve Top-K Chunks
    ↓
LLM Generation
    ↓
Answer
```

## Technologies

- Python
- Poetry
- Ollama
- ChromaDB
- FastAPI
- PyPDF

## Models

| Purpose | Model |
|---|---|
| Generation | `llama3.2` |
| Embedding | `nomic-embed-text` |

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

## Configuration

The baseline uses:

```python
CHUNK_SIZE = 800
CHUNK_OVERLAP = 120
TOP_K = 4
```

The overlap helps preserve context when information occurs near a chunk boundary.

---

# First-Time Setup

Use these steps when running the project for the **first time**.

### 1. Install dependencies

With Poetry:

```bash
poetry install
```

Or, if using `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 2. Install Ollama models

```bash
ollama pull llama3.2
ollama pull nomic-embed-text
```

Check the models:

```bash
ollama list
```

### 3. Add documents

Place `.txt`, `.md`, or `.pdf` documents inside:

```text
data/
```

### 4. Build the vector database

```bash
poetry run python -m app.ingestion
```

This performs:

```text
Load → Chunk → Embed → Store in ChromaDB
```

### 5. Run the RAG application

```bash
poetry run python -m app.main
```

Ask questions in the terminal and type:

```text
exit
```

to quit.

---

# Run After the First Time

If the dependencies, Ollama models, and ChromaDB index already exist, you normally only need:

```bash
poetry run python -m app.main
```

You **do not need to run ingestion every time** because ChromaDB is persistent.

Run ingestion again only when you:

- add documents
- remove documents
- modify document content
- change chunking settings
- change the embedding model

Then run:

```bash
poetry run python -m app.ingestion
poetry run python -m app.main
```

---

## Run Tests

```bash
poetry run python -m scripts.test_queries
```

The tests display the question, retrieved chunks, vector distances, and generated answer.

See `test_log.md` for the recorded test results.

## Optional FastAPI

Start the API:

```bash
poetry run uvicorn app.main:app --reload
```

Open:

```text
http://127.0.0.1:8000/docs
```

Available endpoints:

- `POST /ingest`
- `POST /chat`

## Known Limitation

Basic Top-K retrieval can return weakly relevant chunks. This may introduce unnecessary context into the generated answer.

Possible future improvements include **re-ranking, relevance filtering, semantic chunking, and hybrid retrieval**.
