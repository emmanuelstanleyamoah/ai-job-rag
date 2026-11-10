from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Chunk:
    chunk_id: str
    source: str
    title: str
    text: str


def split_text(text: str, chunk_size: int, overlap: int) -> list[str]:
    """Split on paragraph boundaries, then fall back to sliding windows."""
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")
    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("overlap must be >= 0 and < chunk_size")

    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks: list[str] = []
    buf = ""

    for para in paragraphs:
        candidate = f"{buf}\n\n{para}".strip() if buf else para
        if len(candidate) <= chunk_size:
            buf = candidate
            continue
        if buf:
            chunks.append(buf)
        if len(para) <= chunk_size:
            buf = para
            continue
        start = 0
        while start < len(para):
            end = start + chunk_size
            chunks.append(para[start:end].strip())
            start = end - overlap
        buf = ""

    if buf:
        chunks.append(buf)
    return chunks


def load_markdown_chunks(
    knowledge_dir: Path,
    chunk_size: int,
    overlap: int,
) -> list[Chunk]:
    files = sorted(knowledge_dir.glob("*.md"))
    if not files:
        raise FileNotFoundError(f"No markdown files in {knowledge_dir}")

    chunks: list[Chunk] = []
    for path in files:
        raw = path.read_text(encoding="utf-8")
        title = _title_from_markdown(raw, fallback=path.stem.replace("-", " ").title())
        for i, text in enumerate(split_text(raw, chunk_size, overlap)):
            chunks.append(
                Chunk(
                    chunk_id=f"{path.stem}-{i}",
                    source=path.name,
                    title=title,
                    text=text,
                )
            )
    return chunks


def _title_from_markdown(raw: str, fallback: str) -> str:
    for line in raw.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return fallback
