# Baseline Chat-with-Documents RAG

## Overview

This project is a local Naive Retrieval-Augmented Generation (RAG) application.

It reads documents from the `data/` folder, splits them into chunks, converts those chunks into embeddings, stores the embeddings in ChromaDB, retrieves the most relevant chunks for a user question, and sends those chunks to a local LLM through Ollama to generate a grounded answer.

The main RAG flow is:

```text
Documents
→ Ingestion
→ Chunking
→ Embedding
→ Vector Storage
→ Retrieval
→ Generation
→ Answer
```

---

## What Is RAG?

Large language models can answer many general questions, but they do not automatically know the contents of private or local documents.

Retrieval-Augmented Generation (RAG) solves this by retrieving relevant pieces of local documents at query time and providing them to the language model as context.

This baseline system follows these stages:

1. **Load and chunk** the source documents.
2. **Embed and store** the chunks in a vector database.
3. **Retrieve** the chunks most similar to the user's question.
4. **Generate** an answer using the retrieved context.

The language model does not search the vector database itself. The RAG pipeline retrieves the context first and then sends that context to the model.

---

## Technologies Used

- Python 3.12
- Poetry
- Ollama
- ChromaDB
- FastAPI
- Uvicorn
- PyPDF

---

## Models

### Generation Model

`llama3.2`

This model generates the final answer from the user question and retrieved document context.

Install it with:

```bash
ollama pull llama3.2
```

### Embedding Model

`nomic-embed-text`

This model converts document chunks and user questions into numerical vectors that can be compared using vector similarity search.

Install it with:

```bash
ollama pull nomic-embed-text
```

Verify the installed models:

```bash
ollama list
```

---

## Vector Database

This project uses **ChromaDB in persistent mode**.

The vector database is stored in:

```text
chroma_db/
```

For each chunk, the vector store keeps information such as:

- chunk text
- embedding vector
- source filename
- chunk index
- metadata

---

## Project Structure

```text
RAG-BASELINE-APP/
│
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── embeddings.py
│   ├── generate.py
│   ├── ingest.py
│   ├── main.py
│   └── retrieval.py
│
├── data/
│   └── source documents
│
├── scripts/
│   └── test_queries.py
│
├── chroma_db/
├── README.md
├── test_log.md
├── poetry.lock
└── pyproject.toml
```

---

## RAG Pipeline

### 1. Ingestion

`app/ingest.py`

The ingestion stage reads supported source files from the `data/` folder.

Supported formats in the current implementation are:

- `.txt`
- `.md`
- `.pdf`

Text files are read directly. PDF text is extracted using PyPDF.

---

### 2. Chunking

The project uses **fixed-size character chunking with overlap**.

Current configuration:

```python
CHUNK_SIZE = 800
CHUNK_OVERLAP = 120
```

Each chunk contains up to 800 characters. Consecutive chunks share 120 characters.

Example:

```text
Chunk 1
0 ------------------------ 800

Chunk 2
                     680 ------------------------ 1480
                     <---- 120 overlap ---->
```

### Why This Chunking Strategy Was Used

Fixed-size chunking was chosen because it is simple and appropriate for a baseline Naive RAG implementation.

The 120-character overlap helps preserve context when important information is located near a chunk boundary. Without overlap, a sentence or idea could be split between two chunks and become harder to retrieve.

A future improvement could use semantic chunking or document-structure-aware chunking so that related ideas remain together more naturally.

---

### 3. Embedding

`app/embeddings.py`

Each chunk is converted into an embedding using:

```text
nomic-embed-text
```

Conceptually:

```text
Document chunk
      ↓
nomic-embed-text
      ↓
[0.12, -0.43, 0.71, ...]
```

The same embedding model is also used for user questions during retrieval.

---

### 4. Vector Storage

The chunk text, embeddings, and metadata are stored in ChromaDB.

Each chunk receives a unique ID based on its source filename and chunk index.

Example:

```text
expense_policy.txt::0
expense_policy.txt::1
```

---

### 5. Retrieval

`app/retrieval.py`

When the user asks a question:

1. The question is embedded with `nomic-embed-text`.
2. ChromaDB compares the question vector with the stored chunk vectors.
3. The most relevant chunks are returned.

Current configuration:

```python
TOP_K = 4
```

Therefore, the application retrieves the top 4 chunks for each question.

The test script also prints vector distance values. Lower distances generally indicate a stronger semantic match.

---

### 6. Generation

`app/generate.py`

The retrieved chunks and the original user question are passed to:

```text
llama3.2
```

The system prompt instructs the model to answer only using the retrieved context.

If the documents do not contain enough information, the expected response is:

```text
I don't have enough information in the documents to answer that.
```

This helps keep answers grounded in the document collection.

---

## Setup

### 1. Install Project Dependencies

From the project folder, run:

```bash
poetry install
```

Check the Python version used by Poetry:

```bash
poetry run python --version
```

This project was tested with Python 3.12.

### 2. Install the Required Ollama Models

```bash
ollama pull llama3.2
ollama pull nomic-embed-text
```

Verify:

```bash
ollama list
```

---

## Prepare Documents

Place 3–5 source documents inside:

```text
data/
```

The current implementation supports `.txt`, `.md`, and `.pdf` files.

---

## Build the Vector Index

Run:

```bash
poetry run python -m app.ingest
```

Result from this project:

```text
Indexed 28 chunks from 'data/' into Chroma at 'chroma_db/'.
```

This performs:

```text
Load documents
→ Split into chunks
→ Generate embeddings
→ Store embeddings in ChromaDB
```

---

## Test Retrieval and Generation

Run:

```bash
poetry run python -m scripts.test_queries
```

The script prints:

- the question
- retrieved source files
- chunk indexes
- vector distances
- chunk previews
- the generated answer

The complete test results are recorded in `test_log.md`.

---

## Run the CLI Chat

If the CLI loop has been added to `app/main.py`, run:

```bash
poetry run python -m app.main
```

The CLI repeatedly accepts questions and allows the user to type `exit` to quit.

---

## Run the FastAPI Server

Run:

```bash
poetry run uvicorn app.main:app --reload
```

Open the interactive API documentation at:

```text
http://127.0.0.1:8000/docs
```

Available endpoints:

```text
POST /ingest
POST /chat
```

### POST `/ingest`

Rebuilds the ChromaDB index from the files inside `data/`.

### POST `/chat`

Accepts a question, retrieves relevant chunks, generates an answer, and returns the answer together with the source filenames.

---

## Testing Summary

The RAG application was tested with six questions:

1. Hybrid work requirements
2. Home-office equipment stipend
3. Expense report deadline
4. CEO home address — out of scope
5. Personal cat name — out of scope
6. Employee onboarding

The out-of-scope tests showed that the model stayed grounded and responded that it did not have enough information instead of inventing an answer.

---

## Observed Limitation

The onboarding test retrieved three relevant chunks from `onboarding_guide.txt`, but the fourth retrieved chunk came from `remote_work_policy.txt`.

Because all four retrieved chunks were passed to the generation model, the final answer included information about the $400 home-office stipend even though that information was not directly relevant to the onboarding question.

This demonstrates a limitation of basic Top-K vector retrieval: a retrieved chunk can be semantically related but still introduce unnecessary context.

Possible future improvements include:

- re-ranking retrieved chunks
- adding a relevance threshold
- query rewriting
- semantic chunking
- hybrid keyword + vector retrieval

---

## Test Log

Detailed test results are available in `test_log.md`.

---

## Reflection

A separate 150–300 word reflection should summarize:

- what worked well
- what was harder than expected
- one future Advanced RAG improvement
