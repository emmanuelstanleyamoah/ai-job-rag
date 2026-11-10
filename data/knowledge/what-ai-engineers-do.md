# What AI engineers actually do

Hiring managers are not looking for someone who "likes ChatGPT." They hire people who can take an unstructured business problem, turn it into a measurable ML or LLM system, ship it behind an API, and keep it reliable in production.

## Core job loop

1. Clarify the user problem and the success metric (latency, cost, factuality, conversion).
2. Choose the simplest system that can hit that metric: rules, classical ML, fine-tuning, or RAG.
3. Build data pipelines: ingest, clean, chunk, label, evaluate.
4. Serve a model or retrieval stack through an API with auth, logging, and tracing.
5. Watch production: regressions, prompt drift, retrieval quality, token cost, and abuse.

## Titles you will see

- **AI Engineer / LLM Engineer**: product features on top of foundation models (RAG, agents, evals, tool use).
- **Machine Learning Engineer**: training, feature stores, batch/online inference, model registry.
- **MLOps / Platform**: CI/CD for models, GPU clusters, observability.
- **Applied Scientist**: more research, ablations, papers-to-product.

For a bootcamp graduate targeting first jobs, **AI Engineer** and **junior MLE** are the realistic lanes. Staff/research titles usually require prior shipped systems or a graduate research track.

## Skills that show up on real job posts

- Python as the daily language: APIs, data, tests, notebooks that get turned into jobs.
- Retrieval: chunking, embeddings, hybrid search, reranking, citation.
- Evaluation: golden sets, LLM-as-judge with human spot checks, offline vs online metrics.
- Backend basics: FastAPI or similar, Docker, Postgres or a vector store, queues.
- Communication: write a one-pager that says what you built, why, the metric, and the failure modes.

## What does not get you hired by itself

A list of courses, a fine-tune of a tiny model with no eval, or a chatbot that only wraps a single API call without retrieval, tests, or observability. Interviewers will ask what broke, how you measured it, and what you would do next.
