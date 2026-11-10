from pathlib import Path

from app.bullets import SECURITY_COPILOT_BEFORE
from app.rag import RagPipeline
from app.retriever import TfidfRetriever


def test_pipeline_rewrites_pasted_bullet(tmp_path: Path, monkeypatch):
    knowledge = tmp_path / "knowledge"
    knowledge.mkdir()
    (knowledge / "resume.md").write_text(
        "# AI engineering resume that gets interviews\n\n"
        "Project bullets use verb, system, constraint, and metric.\n",
        encoding="utf-8",
    )
    (knowledge / "interviews.md").write_text(
        "# Interviews\n\nExpect a coding round and a system design round.\n",
        encoding="utf-8",
    )
    monkeypatch.setattr("app.retriever.settings.knowledge_dir", knowledge)
    monkeypatch.setattr("app.retriever.settings.index_dir", tmp_path / "index")
    pipeline = RagPipeline(TfidfRetriever.build(knowledge))

    result = pipeline.ask(SECURITY_COPILOT_BEFORE)

    assert "SOC investigation copilot" in result.answer
    assert "31%" not in result.answer
    assert result.sources[0].source == "resume.md"
