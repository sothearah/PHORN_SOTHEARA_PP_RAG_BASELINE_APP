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

<<<<<<< HEAD
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
=======
### Question

How many in-office days per week do hybrid employees need?

### Retrieved Chunks

1. Source: `remote_work_policy.txt`
   - Chunk Index: `1`
   - Distance: `0.5865`
   - Preview: `one-time home-office stipend of $400 for desk and chair setup. Employees are res...`

2. Source: `remote_work_policy.txt`
   - Chunk Index: `0`
   - Distance: `0.6941`
   - Preview: `Remote Work Policy — Novalink Devices Effective Date: January 2026 1. Eligibil...`

3. Source: `onboarding_guide.txt`
   - Chunk Index: `1`
   - Distance: `0.7449`
   - Preview: `gineering new hires shadow a senior engineer on two code reviews and complete th...`

4. Source: `remote_work_policy.txt`
   - Chunk Index: `2`
   - Distance: `0.8607`
   - Preview: `k arrangements are reviewed every 6 months. The arrangement may be revoked if pe...`

### Generated Answer

According to the context provided, hybrid employees are required to be in the
office at least 2 days per week, specifically Tuesday and Thursday, for team
collaboration sessions.

### Evaluation

The retrieval was successful because several of the highest-ranked chunks came
from `remote_work_policy.txt`, which contains the answer. The final answer was
grounded in the retrieved context.

---

## Test 2 — Home-Office Equipment Stipend

### Question

How much is the home-office equipment stipend?

### Retrieved Chunks

1. Source: `remote_work_policy.txt`
   - Chunk Index: `1`
   - Distance: `0.6209`
   - Preview: `one-time home-office stipend of $400 for desk and chair setup. Employees are res...`

2. Source: `remote_work_policy.txt`
   - Chunk Index: `0`
   - Distance: `0.8536`
   - Preview: `Remote Work Policy — Novalink Devices Effective Date: January 2026 1. Eligibil...`

3. Source: `onboarding_guide.txt`
   - Chunk Index: `0`
   - Distance: `0.9917`
   - Preview: `New Hire Onboarding Guide — Novalink Devices Week 1: Setup Day 1 is spent in IT...`

4. Source: `003_Configuring_VPN_Access_for_Remote_Workers.txt`
   - Chunk Index: `0`
   - Distance: `0.9996`
   - Preview: `Configuring VPN Access for Remote Workers Overview This article provid...`

### Generated Answer

According to `remote_work_policy.txt`, the one-time home-office stipend for
remote employees is $400.

### Evaluation

The top retrieved chunk directly contained the stipend information, so the
retrieval and generated answer were successful.
>>>>>>> f3da57414c59a7a873df238a5f7a841c307147c8

---

## Test 3 — Expense Report Deadline

<<<<<<< HEAD
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
=======
### Question

How long do I have to submit an expense report?

### Retrieved Chunks

1. Source: `expense_policy.txt`
   - Chunk Index: `1`
   - Distance: `0.6024`
   - Preview: `d Transportation Rideshare and taxi expenses are reimbursed for airport transfer...`

2. Source: `expense_policy.txt`
   - Chunk Index: `0`
   - Distance: `0.8911`
   - Preview: `Travel and Expense Policy — Novalink Devices Approval Any business trip expecte...`

3. Source: `remote_work_policy.txt`
   - Chunk Index: `2`
   - Distance: `0.9843`
   - Preview: `k arrangements are reviewed every 6 months. The arrangement may be revoked if pe...`

4. Source: `remote_work_policy.txt`
   - Chunk Index: `1`
   - Distance: `1.0129`
   - Preview: `one-time home-office stipend of $400 for desk and chair setup. Employees are res...`

### Generated Answer

According to the expense policy, expense reports must be submitted within 30
days of the expense being incurred.

### Evaluation

The two strongest matches came from `expense_policy.txt`. The final answer
correctly extracted the 30-day deadline.

---

## Test 4 — CEO Home Address — Out of Scope

### Question

What is the CEO's home address?

### Retrieved Chunks

1. Source: `003_Configuring_VPN_Access_for_Remote_Workers.txt`
   - Chunk Index: `3`
   - Distance: `0.9547`
   - Preview: `has changed to a company-assigned IP address. If you continue to experience is...`

2. Source: `remote_work_policy.txt`
   - Chunk Index: `1`
   - Distance: `0.9766`
   - Preview: `one-time home-office stipend of $400 for desk and chair setup. Employees are res...`

3. Source: `remote_work_policy.txt`
   - Chunk Index: `0`
   - Distance: `0.9883`
   - Preview: `Remote Work Policy — Novalink Devices Effective Date: January 2026 1. Eligibil...`

4. Source: `onboarding_guide.txt`
   - Chunk Index: `2`
   - Distance: `1.0075`
   - Preview: `uddy is available for informal questions ("who do I ask about X") and is not the...`

### Generated Answer

I don't have enough information in the documents to answer that.

### Evaluation

The retrieved chunks did not contain the requested information. The model
correctly stayed grounded and refused to invent an answer.

---

## Test 5 — Cat Name — Out of Scope

### Question

What is my cat name?

### Retrieved Chunks

1. Source: `onboarding_guide.txt`
   - Chunk Index: `2`
   - Distance: `1.2309`
   - Preview: `uddy is available for informal questions ("who do I ask about X") and is not the...`

2. Source: `003_Configuring_VPN_Access_for_Remote_Workers.txt`
   - Chunk Index: `3`
   - Distance: `1.2611`
   - Preview: `has changed to a company-assigned IP address. If you continue to experience is...`

3. Source: `onboarding_guide.txt`
   - Chunk Index: `1`
   - Distance: `1.3224`
   - Preview: `gineering new hires shadow a senior engineer on two code reviews and complete th...`

4. Source: `002_Resetting_a_Forgotten_PIN.txt`
   - Chunk Index: `0`
   - Distance: `1.3253`
   - Preview: `Resetting a Forgotten PIN If you have forgotten your PIN, you can reset it ...`

### Generated Answer

I don't have enough information in the documents to answer that.

### Evaluation

This was a weak retrieval case because the best distance was greater than 1.0.
ChromaDB still returned the nearest available chunks even though none of them
were actually relevant to the question.

The generation model correctly refused to guess.
>>>>>>> f3da57414c59a7a873df238a5f7a841c307147c8

---

## Test 6 — Employee Onboarding

<<<<<<< HEAD
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
=======
### Question

What should a new employee complete during onboarding?

### Retrieved Chunks

1. Source: `onboarding_guide.txt`
   - Chunk Index: `0`
   - Distance: `0.4581`
   - Preview: `New Hire Onboarding Guide — Novalink Devices Week 1: Setup Day 1 is spent in IT...`

2. Source: `onboarding_guide.txt`
   - Chunk Index: `1`
   - Distance: `0.5536`
   - Preview: `gineering new hires shadow a senior engineer on two code reviews and complete th...`

3. Source: `onboarding_guide.txt`
   - Chunk Index: `2`
   - Distance: `0.8007`
   - Preview: `uddy is available for informal questions ("who do I ask about X") and is not the...`

4. Source: `remote_work_policy.txt`
   - Chunk Index: `0`
   - Distance: `0.8337`
   - Preview: `Remote Work Policy — Novalink Devices Effective Date: January 2026 1. Eligibil...`

### Generated Answer

According to the context, a new employee should complete the following during
onboarding:

- Set up and access their email, chat, and internal wiki accounts by the end of Week 1.
- Complete the "Local Dev Environment" setup checklist as a new hire in Engineering.
- Shadow a senior engineer on two code reviews.
- Complete CRM training as a new hire in Sales.
- Complete a Week 2 curriculum specific to their department.
- Set up their laptop, desk, and chair at home with the help of a $400 stipend provided by the company.
- Complete the "Local Dev Environment" setup checklist as a new hire in Engineering.

### Evaluation

The three strongest retrieved chunks came from `onboarding_guide.txt`, so the
retrieval was mostly successful.

However, the fourth retrieved chunk came from `remote_work_policy.txt`. Because
all four chunks were passed to the generation model, the final answer included
the $400 home-office stipend even though that information was not directly
relevant to the onboarding question.

This demonstrates retrieval noise in a basic Top-K RAG system and shows why
re-ranking or relevance filtering could improve the pipeline.

---

## Overall Test Summary

The system answered the main in-scope policy questions correctly and stayed
grounded for the two out-of-scope questions.

The main weakness observed was retrieval noise. The onboarding query retrieved
one less relevant remote-work chunk, which influenced the final generated
answer.

A future improvement could add a re-ranking stage or a relevance threshold
before sending retrieved chunks to the generation model.
>>>>>>> f3da57414c59a7a873df238a5f7a841c307147c8
