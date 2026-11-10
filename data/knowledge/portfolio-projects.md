# Portfolio projects that get AI engineering interviews

Recruiters and hiring managers click GitHub. They want a README that reads like a design doc, a runnable demo, and evidence you measured quality.

## Build 2–3 projects, not 12 tutorials

Depth beats volume. Each project should have:

- A real user and a failure mode (hallucination, latency, cost, stale data).
- A README with architecture diagram, how to run, and eval results.
- Tests for chunking/retrieval or data transforms.
- A demo (Gradio/Streamlit) plus an API.

## Project 1: Domain RAG assistant (highest signal)

Pick a narrow corpus: bootcamp handbook, company policies, a public RFC set, or job-search guides.

Must-haves:

- Ingest markdown/PDF → chunks with source metadata.
- Retriever you can explain (BM25/TF-IDF, embeddings, or hybrid).
- Generator that is not allowed to answer outside context.
- Citations in the UI.
- Offline eval: 30–100 questions with expected doc IDs; report recall@k and groundedness.

Talking point: "When retrieval misses, the model abstains. We logged misses and added those docs."

## Project 2: Eval harness or RAG quality dashboard

Interviewers love this because most candidates never measure.

- Golden question set versioned in git.
- Metrics: recall@k, MRR, answer faithfulness, token cost, latency.
- A script that fails CI if recall drops more than a threshold.

Talking point: "We caught a chunk-size regression before it shipped."

## Project 3: Small production shape

Take project 1 and add one backend concern:

- Auth + rate limits
- Request tracing IDs
- Caching frequent queries
- A feedback thumbs-down that writes to a labeled miss file

This is how you look like an engineer, not a notebook user.

## Projects to skip as your headline

- "ChatGPT clone" with no retrieval or eval.
- Fine-tuning a 7B model on a tiny scraped dataset with loss curves only.
- AutoGPT-style agents that loop until they time out, with no tool tests.

Those can be appendix work. Lead with RAG + evals + an API.

## README template

1. Problem and user
2. Architecture (ingest → index → retrieve → generate → cite)
3. Quickstart
4. Eval table (before/after)
5. Limitations and next experiments
6. License
