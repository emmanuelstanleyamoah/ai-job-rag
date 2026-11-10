# AI engineering resume that gets interviews

Your resume has about 20 seconds on a first pass. It must answer: can this person ship an AI system, and can they talk about impact in numbers?

## Structure (one page if you have under 8 years)

1. Header: name, city + timezone, GitHub, LinkedIn, email. Optional: portfolio URL.
2. Title line: `AI Engineer | RAG, evals, Python, FastAPI` — not "Aspiring AI enthusiast."
3. Selected projects (2–3), then experience, then skills. Education last unless you are a new grad with a relevant degree.

## Project bullets that work

Use: **verb + system + constraint + metric**.

Weak: "Built a chatbot using LangChain and OpenAI."

Strong: "Shipped a FastAPI RAG assistant over 120 internal docs; hybrid TF-IDF + embeddings cut unsupported answers from 31% to 9% on a 80-question eval set; p95 latency 1.8s."

Every AI project bullet should include at least two of: data size, eval metric, latency, cost, or user outcome.

## What to put near the top

- Retrieval and evaluation, not just "prompt engineering."
- Python backend work: APIs, tests, Docker.
- One production-shaped detail: logging, tracing, caching, or guardrails.
- Domain if you have it (support, search, code, healthcare) — hiring teams buy problem context.

## Skills section

Group by how you actually used them:

- Languages: Python
- LLM/RAG: chunking, TF-IDF/hybrid search, rerank, citations, eval harness
- Serving: FastAPI, Gradio/Streamlit for demos, Docker
- Data: pandas, Postgres, object storage
- Optional: PyTorch only if you trained or fine-tuned something you can defend

Do not list 30 libraries you completed a tutorial in. Interviewers pick a skill and go deep.

## Common rejection reasons

- No metrics.
- Every bullet is "used X to do Y" with no ownership of quality.
- Job title soup ("CEO of my freelance brand") that hides junior scope.
- Typos in a one-page document. That is a signal about production care.

## Worked rewrite: security detection copilot

Before:

Built an AI Security Detection & Response Copilot using Python, Streamlit, FastAPI, Gemini, LangGraph, ChromaDB, Microsoft Presidio, and Guardrails AI. Implemented secure RAG pipelines, multi-agent incident investigation workflows, MITRE ATT&CK enrichment, Sigma/KQL rule generation, explainable AI, and AI governance controls to automate SOC operations and improve investigation efficiency.

After:

Built a SOC investigation copilot (Python, FastAPI, Streamlit) that retrieves detection context through a guarded RAG pipeline, maps findings to MITRE ATT&CK, and drafts Sigma/KQL rules with cited evidence. Presidio redacts sensitive fields and Guardrails checks prompts before Gemini generation; LangGraph logs triage, enrichment, and rule-draft steps so an analyst can see which chunk and tool produced the recommendation.

Skills line, not a second laundry list: Python; RAG (ChromaDB, citations); agents (LangGraph); security (MITRE ATT&CK, Sigma, KQL, Presidio, Guardrails); serving (FastAPI, Streamlit); models (Gemini).

What changed:

- The first line names the system, the constraint (guarded RAG with citations), and the SOC outcome (ATT&CK mapping and Sigma/KQL drafts).
- Three tools stay in the bullet. The others appear only where they do a job.
- Submit the After paragraph as the resume bullet and put the skills line in the skills section. Do not append a corpus size or outcome until you have measured it.
