# From AI bootcamp to the first engineering job

A bootcamp is a compressed curriculum. Hiring teams still hire for evidence. Your job is to convert coursework into two public, evaluated systems and a story you can tell in 90 seconds.

## First 30 days after (or during) the capstone

1. Pick the capstone most like production AI work (usually RAG or an eval-heavy pipeline).
2. Delete tutorial leftovers. Add tests, a clean README, Docker or a lockfile, and a demo.
3. Write 40 evaluation questions against your own corpus. Report recall@k.
4. Record a 2-minute walkthrough: problem, architecture, metric, failure mode.
5. Rewrite the resume around that project.

## Story you should be able to tell cold

"I built an assistant for [user] over [corpus]. Retrieval uses [method]. We measure [metric]. When it fails, it is usually [failure]. Next I would add [rerank/hybrid/monitoring]."

If you cannot fill those brackets, the project is not interview-ready.

## Skills gap most bootcamp grads have

- Writing Python that other people can run (packaging, env files, tests).
- SQL and basic data modeling.
- Reading logs and explaining a bug without blaming the model.
- Estimating cost and latency.
- Saying "I don't know" and then proposing how to find out.

Close the gap with small, visible work: add tests to the RAG app, log retrieval scores, cache repeated queries.

## Networking without cringe

- Share your eval writeup in bootcamp Slack and ask for a mock interview.
- Comment technically on a company's AI engineering blog, then follow up once.
- Alumni referrals beat cold apply. Ask for a 15-minute "what does the loop look like" chat, not "can you hire me."

## Red flags in your own process

- You keep starting new repos instead of finishing evals.
- You cannot run your demo on a clean machine from the README.
- You describe tools ("I used LangChain") instead of outcomes ("unsupported answers dropped 9 points").

Finish one system until it is the artifact you lead with. That is how bootcamp work turns into an AI engineering job.
