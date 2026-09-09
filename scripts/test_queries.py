"""
Run the pipeline against a handful of known questions and print what came
back at every stage — not just the final answer, but *what was retrieved*
and *how far away* each chunk was. That's what makes it possible to debug
whether a bad answer is a retrieval problem or a generation problem.

Run:
    poetry run python -m scripts.test_queries

Make sure you've run `poetry run python -m app.ingest` at least once first.
"""
from app.generate import generate_answer
from app.retrieval import retrieve

# Three "in scope" questions the sample documents can actually answer,
# and one "out of scope" question to check the model admits it doesn't know
# instead of making something up.
TEST_QUESTIONS = [
    "How many in-office days per week do hybrid employees need?",
    "How much is the home-office equipment stipend?",
    "How long do I have to submit an expense report?",
    "What is the CEO's home address?",  # deliberately not in any document
    "What is my cat name?",
    "What should a new employee complete during onboarding?",
]


def run_query(question: str) -> None:
    print("=" * 80)
    print(f"Q: {question}")

    chunks = retrieve(question)
    print(f"\nRetrieved {len(chunks)} chunks:")
    for c in chunks:
        preview = c["text"][:80].replace("\n", " ")
        print(f"  - [{c['source']} #{c['chunk_index']}] dist={c['distance']:.4f}  \"{preview}...\"")

    answer = generate_answer(question, chunks)
    print(f"\nA: {answer}")

    # Very basic sanity check, not a real eval metric: did the model cite a
    # source, or at least stay short and cautious, when nothing relevant was
    # retrieved? This is the kind of check worth automating once you have
    # more than a handful of questions.
    best_distance = min((c["distance"] for c in chunks), default=None)
    if best_distance is not None and best_distance > 1.0:
        print("\n[note] Weak retrieval match (best distance > 1.0) — "
              "worth checking if the answer stayed cautious rather than guessing.")


if __name__ == "__main__":
    for q in TEST_QUESTIONS:
        run_query(q)
    print("=" * 80)
