# RAG Test Log

<<<<<<< HEAD
## Configuration

- Generation Model: `llama3.2`
- Embedding Model: `nomic-embed-text`
- Vector Database: ChromaDB
- Top-K: `4`
- Chunk Size: `800`
- Chunk Overlap: `120`
=======
This document records the questions used to test the baseline RAG application,
the retrieved chunks, vector distances, and final answers.

## Configuration

- Generation model: `llama3.2`
- Embedding model: `nomic-embed-text`
- Vector database: ChromaDB
- Top-K retrieval: `4`
- Chunk size: `800` characters
- Chunk overlap: `120` characters
>>>>>>> f3da57414c59a7a873df238a5f7a841c307147c8

---

## Test 1 — Hybrid Work Policy

**Question:**  
How many in-office days per week do hybrid employees need?

**Top Retrieved Sources:**
- `remote_work_policy.txt` — distance `0.5865`
- `remote_work_policy.txt` — distance `0.6941`

**Answer:**  
Hybrid employees are required to be in the office at least **2 days per week**, specifically Tuesday and Thursday.

**Result:** Correct retrieval and answer.

---

## Test 2 — Home-Office Stipend

**Question:**  
How much is the home-office equipment stipend?

**Top Retrieved Source:**
- `remote_work_policy.txt` — distance `0.6209`

**Answer:**  
The one-time home-office stipend is **$400**.

**Result:** Correct retrieval and answer.

---

## Test 3 — Expense Report Deadline

**Question:**  
How long do I have to submit an expense report?

**Top Retrieved Source:**
- `expense_policy.txt` — distance `0.6024`

**Answer:**  
Expense reports must be submitted within **30 days**.

**Result:** Correct retrieval and answer.

---

## Test 4 — CEO Home Address (Out of Scope)

**Question:**  
What is the CEO's home address?

**Answer:**  
> I don't have enough information in the documents to answer that.

**Result:** The model stayed grounded and did not invent an answer.

---

## Test 5 — Cat Name (Out of Scope)

**Question:**  
What is my cat name?

**Best Retrieval Distance:** `1.2309`

**Answer:**  
> I don't have enough information in the documents to answer that.

**Result:** The retrieved chunks were weak matches, but the model correctly refused to guess.

---

## Test 6 — Employee Onboarding

**Question:**  
What should a new employee complete during onboarding?

**Top Retrieved Sources:**
- `onboarding_guide.txt` — `0.4581`
- `onboarding_guide.txt` — `0.5536`
- `onboarding_guide.txt` — `0.8007`
- `remote_work_policy.txt` — `0.8337`

**Answer:**  
The model correctly identified several onboarding activities, including account setup, department-specific training, and engineering tasks.

However, it also included the **$400 home-office stipend**, which came from a less relevant remote-work chunk.

**Result:** Mostly correct, but retrieval noise affected the final answer.

---

## Overall Result

The Naive RAG pipeline successfully:

- retrieved relevant document chunks
- answered in-scope questions correctly
- refused to guess for out-of-scope questions
- exposed retrieval noise in one test

The main limitation is that **Top-K retrieval always returns the nearest chunks**, even when some are weakly relevant.

Future improvements could include **re-ranking or relevance filtering** before sending retrieved context to the LLM.
