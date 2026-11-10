from pathlib import Path

from app.retriever import TfidfRetriever


def test_search_returns_resume_doc(tmp_path: Path, monkeypatch):
    knowledge = tmp_path / "knowledge"
    knowledge.mkdir()
    (knowledge / "resume.md").write_text(
        "# Resume\n\nQuantify impact with metrics. Put RAG and evaluation near the top.",
        encoding="utf-8",
    )
    (knowledge / "interviews.md").write_text(
        "# Interviews\n\nExpect a coding round plus ML system design for retrieval systems.",
        encoding="utf-8",
    )
    monkeypatch.setattr("app.retriever.settings.knowledge_dir", knowledge)
    monkeypatch.setattr("app.retriever.settings.index_dir", tmp_path / "index")
    monkeypatch.setattr("app.retriever.settings.chunk_size", 400)
    monkeypatch.setattr("app.retriever.settings.chunk_overlap", 40)

    retriever = TfidfRetriever.build(knowledge)
    hits = retriever.search("How do I write a RAG resume?")
    assert hits
    assert hits[0].source == "resume.md"
    assert hits[0].score > 0
