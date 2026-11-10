# AI Job Coach

https://github.com/emmanuelstanleyamoah/ai-job-rag

A Python RAG chatbot for an AI engineering bootcamp. Students ask how to land AI engineering jobs; answers are retrieved from a local knowledge base (resumes, portfolios, interviews, search strategy) and then generated with citations.

This is a teaching-shaped stack: a small custom retrieve-then-generate pipeline you can explain in an interview, not a hidden framework.

## Architecture

```
markdown corpus  →  chunk  →  TF-IDF index  →  top-k retrieve  →  LLM  →  cited answer
                                      ↑
                              Gradio UI / FastAPI
```

- **Frontend:** Gradio chat (`python -m app.main ui`)
- **Backend:** FastAPI (`python -m app.main api`) plus the RAG pipeline in `app/`
- **Retrieval:** scikit-learn TF-IDF + cosine similarity (offline, no model download)
- **Generation:** Ollama by default, or OpenAI if `OPENAI_API_KEY` is set. If neither is up, the app returns extractive snippets so the demo still runs.
- **Abstain:** a question with no chunk above `MIN_SCORE` (default 0.08) is refused. The model is not called.

## Quickstart

```powershell
cd $HOME\ai-job-rag
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
python -m app.main ingest
python -m app.main ui
```

Open http://127.0.0.1:7860

Optional local LLM:

```powershell
ollama pull llama3
```

API instead of the UI:

```powershell
python -m app.main api
# POST http://127.0.0.1:8000/chat  {"question":"How should I structure an AI resume?"}
```

## Tests

```powershell
pytest -q
```

Retrieval eval (rebuild the index first if the knowledge files changed):

```powershell
python -m app.main ingest
python -m app.main eval
```

## Project map

| Path | Role |
| --- | --- |
| `data/knowledge/` | Source of truth the model is allowed to use |
| `app/chunking.py` | Paragraph-aware splitting with overlap |
| `app/retriever.py` | Build/load TF-IDF index, cosine top-k |
| `app/llm.py` | OpenAI → Ollama → extractive fallback |
| `Dockerfile` | Demo image; UI listens on 0.0.0.0:7860 |
| `app/rag.py` | Glue: retrieve, format context, generate |
| `app/api.py` | FastAPI `/chat` and `/health` |
| `app/ui.py` | Gradio chat with source list |
| `app/bullets.py` | Resume-bullet rewrite (no invented metrics) |
| `app/evaluate.py` | recall@k over `data/eval/questions.json` |
| `data/eval/questions.json` | Golden questions and expected source files |

## Limitations

- Retrieval is lexical. A paraphrase that shares no terms with the notes will abstain.
- The corpus is the bootcamp notes in this repo. It does not know live job posts or salaries.
- Resume rewrites will not invent metrics. Add a number only after you measure it.
- Cited answers need Ollama or an OpenAI-compatible key. Otherwise the reply is the retrieved text.

## Why TF-IDF here

Bootcamp interviews often ask you to implement retrieval without a GPU. Lexical search is strong on exact terms (`RAG`, `recall@k`, `FastAPI`), is fully deterministic, and is easy to eval. You can later swap in embeddings or hybrid search without changing the UI or API.
