# AI engineer interview loop

Most companies run some mix of recruiter screen, coding, ML/LLM fundamentals, system design, and behavioral. Junior AI engineer loops are still software interviews with extra retrieval and evaluation questions.

## Recruiter screen (20–30 min)

Have a 90-second story: who you help, what you shipped, the metric, what you want next.

Be ready for:

- Location / timezone / work authorization
- Salary range (know the market band for your city and level)
- "Walk me through your strongest RAG project"

## Coding round

Expect Python: arrays/hashes, parsing, small APIs, or data transforms. AI teams still filter on whether you can write correct, readable code.

Practice:

- Implement chunking with overlap and write tests.
- Given documents and a query, return top-k by TF-IDF cosine similarity.
- Parse JSON logs and compute p95 latency.

Talk while you work: constraints, complexity, tests, failure cases.

## ML / LLM fundamentals

You do not need a PhD. You do need crisp definitions and tradeoffs.

High-yield topics:

- Precision vs recall; why recall@k matters for RAG.
- Embeddings vs lexical search; when hybrid wins.
- Temperature, context window, tokenization at a practical level.
- Hallucinations as a retrieval + prompt + eval problem, not magic.
- Fine-tune vs RAG: RAG for changing knowledge and citations; fine-tune for style/format/tool patterns when you have data.

If you used TF-IDF in a project, be able to explain IDF and why stop words are removed. If you used embeddings, explain cosine similarity and chunk-size vs missed context.

## ML system design (45–60 min)

Prompt: "Design a support assistant over our help center."

A strong answer walks:

1. Users, SLAs, and what "wrong" costs.
2. Ingest and chunking; metadata (product, version, date).
3. Index: lexical + vector; rerank if needed.
4. Generation: grounded prompt, citations, abstain behavior.
5. Eval: golden set, online thumbs-down, hallucination sampling.
6. Ops: latency budget, cache, cost per query, PII, rate limits, rollback.

Always mention a metric you would ship with, not just "we will use GPT-4."

## Behavioral

Use situation → action → result. Prefer stories about:

- You found the model was confidently wrong, and you added evals.
- You cut scope to hit a deadline.
- You disagreed on chunking or model choice and used data.

## Questions you should ask them

- How do you measure answer quality in production?
- What does on-call look like for the AI stack?
- Is this role mostly prompting, or do I own retrieval data and APIs?
