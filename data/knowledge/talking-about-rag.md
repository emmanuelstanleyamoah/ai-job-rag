# How to talk about RAG in interviews

Retrieval-Augmented Generation is the most common "AI engineer" project. Interviewers have seen dozens. You stand out by owning retrieval quality, grounding, and evaluation — not by naming a framework.

## One-minute explanation

"RAG means the model does not rely on parametric memory for facts. We retrieve relevant chunks from a corpus we control, put them in the prompt, and require citations. That gives us fresher knowledge and a way to debug wrong answers: was retrieval bad, or did the model ignore context?"

## Design choices they will probe

- **Chunk size**: too small loses meaning; too large dilutes the query and blows the context window. Start around 500–1000 characters or 300–800 tokens, then measure recall@k.
- **Overlap**: 10–20% overlap reduces boundary misses for sentences split across chunks.
- **Lexical vs dense**: TF-IDF/BM25 is strong on exact terms (API names, error codes). Embeddings catch paraphrases. Hybrid is the default production move.
- **Metadata filters**: time, product, permission. Retrieval is also an access-control problem.
- **Abstain**: if top score is low, say "not in the knowledge base" instead of guessing.

## Eval story (memorize this shape)

"We built N questions from real user language. For each, we labeled the source file that should be retrieved. We tracked recall@k. Then we sampled generated answers for faithfulness to the retrieved text. When we changed chunking, we reran the suite. One change improved keyword questions and hurt paraphrases, so we kept hybrid search."

If you did not build an eval set, say so and describe how you would. Do not fake numbers.

## Failure modes to volunteer

- Corpus is stale; ingest is not scheduled.
- Tables and code blocks chunk poorly.
- User question is underspecified; retrieval returns mixed products.
- Prompt stuffing: too many chunks, model latches onto the wrong one.
- Prompt injection in retrieved documents.

Volunteering failure modes signals production instinct.

## Frameworks

LangChain, LlamaIndex, Haystack, or a small custom pipeline are all fine. Be ready to implement retrieve-then-generate without a framework: load chunks, score, prompt, parse citations. That is the coding-round version of RAG.
