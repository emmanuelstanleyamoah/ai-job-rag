from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from app.config import settings
from app.retriever import TfidfRetriever

DEFAULT_QUESTIONS = settings.index_dir.parent / "eval" / "questions.json"


@dataclass(frozen=True)
class EvalReport:
    k: int
    recall_at_k: float
    hits: int
    total: int
    misses: list[str]

    def render(self) -> str:
        lines = [
            f"recall@{self.k} {self.recall_at_k:.3f} "
            f"({self.hits}/{self.total} questions retrieved an expected source)",
        ]
        lines.extend(f"miss: {miss}" for miss in self.misses)
        return "\n".join(lines)


def load_questions(path: Path | None = None) -> list[dict]:
    question_path = path or DEFAULT_QUESTIONS
    return json.loads(question_path.read_text(encoding="utf-8"))


def recall_at_k(
    retriever: TfidfRetriever,
    questions: list[dict],
    k: int | None = None,
) -> EvalReport:
    top_k = k or settings.top_k
    hits = 0
    misses: list[str] = []
    for item in questions:
        found = {hit.source for hit in retriever.search(item["question"], top_k=top_k)}
        expected = set(item["expected"])
        if found & expected:
            hits += 1
        else:
            misses.append(item["question"])
    total = len(questions)
    score = hits / total if total else 0.0
    return EvalReport(k=top_k, recall_at_k=score, hits=hits, total=total, misses=misses)


def run_eval(question_path: Path | None = None) -> EvalReport:
    report = recall_at_k(TfidfRetriever.load_or_build(), load_questions(question_path))
    print(report.render())
    return report
