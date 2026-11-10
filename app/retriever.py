from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path

import joblib
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from app.chunking import Chunk, load_markdown_chunks
from app.config import settings


@dataclass(frozen=True)
class Hit:
    chunk_id: str
    source: str
    title: str
    text: str
    score: float


class TfidfRetriever:
    """Offline lexical retriever. Fast, deterministic, no model download."""

    def __init__(self, vectorizer: TfidfVectorizer, matrix, chunks: list[Chunk]):
        self.vectorizer = vectorizer
        self.matrix = matrix
        self.chunks = chunks

    @classmethod
    def build(cls, knowledge_dir: Path | None = None) -> TfidfRetriever:
        chunks = load_markdown_chunks(
            knowledge_dir or settings.knowledge_dir,
            settings.chunk_size,
            settings.chunk_overlap,
        )
        # max_df below 1.0 is invalid when the corpus is a single chunk.
        max_df = 0.95 if len(chunks) > 1 else 1.0
        vectorizer = TfidfVectorizer(
            lowercase=True,
            stop_words="english",
            ngram_range=(1, 2),
            min_df=1,
            max_df=max_df,
        )
        matrix = vectorizer.fit_transform([c.text for c in chunks])
        retriever = cls(vectorizer, matrix, chunks)
        retriever.save(settings.index_dir)
        return retriever

    @classmethod
    def load_or_build(cls) -> TfidfRetriever:
        index_dir = settings.index_dir
        required = [index_dir / "vectorizer.joblib", index_dir / "matrix.joblib", index_dir / "chunks.json"]
        if all(p.exists() for p in required):
            return cls.load(index_dir)
        return cls.build()

    def save(self, index_dir: Path) -> None:
        index_dir.mkdir(parents=True, exist_ok=True)
        joblib.dump(self.vectorizer, index_dir / "vectorizer.joblib")
        joblib.dump(self.matrix, index_dir / "matrix.joblib")
        (index_dir / "chunks.json").write_text(
            json.dumps([asdict(c) for c in self.chunks], indent=2),
            encoding="utf-8",
        )

    @classmethod
    def load(cls, index_dir: Path) -> TfidfRetriever:
        vectorizer = joblib.load(index_dir / "vectorizer.joblib")
        matrix = joblib.load(index_dir / "matrix.joblib")
        raw = json.loads((index_dir / "chunks.json").read_text(encoding="utf-8"))
        chunks = [Chunk(**item) for item in raw]
        return cls(vectorizer, matrix, chunks)

    def search(self, query: str, top_k: int | None = None) -> list[Hit]:
        k = top_k or settings.top_k
        if not query.strip():
            return []
        q = self.vectorizer.transform([query])
        scores = cosine_similarity(q, self.matrix).ravel()
        if not np.any(scores):
            return []
        k = min(k, len(scores))
        idxs = np.argpartition(scores, -k)[-k:]
        idxs = idxs[np.argsort(scores[idxs])[::-1]]
        hits: list[Hit] = []
        for i in idxs:
            chunk = self.chunks[int(i)]
            score = float(scores[int(i)])
            if score < settings.min_score:
                continue
            hits.append(
                Hit(
                    chunk_id=chunk.chunk_id,
                    source=chunk.source,
                    title=chunk.title,
                    text=chunk.text,
                    score=score,
                )
            )
        return hits
