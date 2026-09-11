"""
Run the pipeline against a handful of known questions and print what came
back at every stage — not just the final answer, but *what was retrieved*
and *how far away* each chunk was. That's what makes it possible to debug
whether a bad answer is a retrieval problem or a generation problem.

Run:
    poetry run python -m scripts.test_queries

Make sure you've run `poetry run python -m app.ingest` at least once first.
"""
from app.pipeline import ask


TEST_QUESTIONS = [
    "How many in-office days per week do hybrid employees need?",
    "How much is the home-office equipment stipend?",
    "How long do I have to submit an expense report?",
    "What is the CEO's home address?",
    "What is my cat name?",
    "What should a new employee complete during onboarding?",
]


def run_query(question: str) -> None:
    print("=" * 80)
    print(f"Q: {question}")

    result = ask(question)
    chunks = result["chunks"]

    print(f"\nRetrieved {len(chunks)} chunks:")

    for chunk in chunks:
        preview = chunk["text"][:80].replace("\n", " ")

        print(
            f"  - [{chunk['source']} #{chunk['chunk_index']}] "
            f"dist={chunk['distance']:.4f} "
            f'"{preview}..."'
        )

    print(f"\nA: {result['answer']}")

    best_distance = min(
        (chunk["distance"] for chunk in chunks),
        default=None,
    )

    if best_distance is not None and best_distance > 1.0:
        print(
            "\n[note] Weak retrieval match (best distance > 1.0) — "
            "check whether the answer stayed cautious instead of guessing."
        )


if __name__ == "__main__":
    for question in TEST_QUESTIONS:
        run_query(question)

    print("=" * 80)
