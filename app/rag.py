from __future__ import annotations

from dataclasses import dataclass

from app.bullets import extract_bullet, format_rewrite, rewrite_project_bullet
from app.config import settings
from app.llm import ABSTAIN, generate_answer
from app.retriever import Hit, TfidfRetriever


@dataclass(frozen=True)
class RagResponse:
    answer: str
    sources: list[Hit]


class RagPipeline:
    def __init__(self, retriever: TfidfRetriever | None = None):
        self.retriever = retriever or TfidfRetriever.load_or_build()

    def ask(self, question: str, top_k: int | None = None) -> RagResponse:
        bullet = extract_bullet(question)
        query = (
            "AI engineering resume project bullet verb system constraint metric"
            if bullet
            else question
        )
        hits = self.retriever.search(query, top_k=top_k or settings.top_k)
        if bullet:
            return RagResponse(
                answer=format_rewrite(rewrite_project_bullet(bullet)),
                sources=hits,
            )
        if not hits:
            return RagResponse(answer=ABSTAIN, sources=[])
        context = _format_context(hits)
        answer = generate_answer(question, context)
        return RagResponse(answer=answer, sources=hits)


def _format_context(hits: list[Hit]) -> str:
    if not hits:
        return ""
    blocks = []
    for hit in hits:
        blocks.append(
            f"[{hit.source}] {hit.title} (score={hit.score:.3f})\n{hit.text}"
        )
    return "\n\n---\n\n".join(blocks)
