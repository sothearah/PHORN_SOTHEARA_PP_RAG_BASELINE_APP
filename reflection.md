# Reflection

Building this Naive RAG prototype helped me understand how the main RAG
components work together: document loading, chunking, embedding, vector
storage, retrieval, and generation.

One part that worked well was retrieving information for questions that were
clearly answered by the documents. For example, questions about the home-office
stipend and expense report deadline retrieved the correct policy documents and
produced correct answers. The system also handled out-of-scope questions well.
When I asked for the CEO's home address or my cat's name, the model responded
that there was not enough information in the documents instead of inventing an
answer.

One challenge was understanding retrieval quality. ChromaDB always returns the
nearest chunks even when some of them are not very relevant. In the onboarding
test, three chunks came from the onboarding guide, but another chunk came from
the remote work policy. This extra context caused the generated answer to
include the $400 home-office stipend, which was not directly relevant to the
question.

If I improve this system using Advanced RAG techniques, I would add re-ranking
or relevance filtering after vector retrieval. This could remove weak or
unrelated chunks before they are passed to the LLM and improve the accuracy and
groundedness of generated answers.