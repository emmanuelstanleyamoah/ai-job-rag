from __future__ import annotations

from functools import lru_cache

from fastapi import FastAPI
from pydantic import BaseModel, Field

from app.rag import RagPipeline


class ChatRequest(BaseModel):
    question: str = Field(min_length=1, max_length=4000)
    top_k: int | None = Field(default=None, ge=1, le=10)


class Source(BaseModel):
    source: str
    title: str
    score: float
    excerpt: str


class ChatResponse(BaseModel):
    answer: str
    sources: list[Source]


@lru_cache(maxsize=1)
def get_pipeline() -> RagPipeline:
    return RagPipeline()


app = FastAPI(
    title="AI Job Coach RAG",
    description="Retrieval-augmented career coach for AI engineering bootcamp students.",
    version="0.1.0",
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest) -> ChatResponse:
    result = get_pipeline().ask(req.question, top_k=req.top_k)
    return ChatResponse(
        answer=result.answer,
        sources=[
            Source(
                source=hit.source,
                title=hit.title,
                score=round(hit.score, 4),
                excerpt=hit.text[:400],
            )
            for hit in result.sources
        ],
    )
