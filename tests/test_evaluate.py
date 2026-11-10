import json
from pathlib import Path

from app.evaluate import load_questions, recall_at_k
from app.retriever import TfidfRetriever


def test_recall_counts_expected_source(tmp_path: Path, monkeypatch):
    knowledge = tmp_path / "knowledge"
    knowledge.mkdir()
    (knowledge / "resume.md").write_text(
        "# Resume\n\nProject bullets need a metric and a constraint.",
        encoding="utf-8",
    )
    (knowledge / "interviews.md").write_text(
        "# Interviews\n\nThe loop has a coding round and a system design round.",
        encoding="utf-8",
    )
    monkeypatch.setattr("app.retriever.settings.knowledge_dir", knowledge)
    monkeypatch.setattr("app.retriever.settings.index_dir", tmp_path / "index")
    questions = [
        {"question": "How do I write a project bullet with a metric?", "expected": ["resume.md"]},
        {"question": "What is in the interview loop coding round?", "expected": ["interviews.md"]},
    ]
    report = recall_at_k(TfidfRetriever.build(knowledge), questions, k=2)
    assert report.hits == 2
    assert report.recall_at_k == 1.0
    assert "recall@2" in report.render()


def test_golden_questions_file_is_well_formed():
    questions = load_questions()
    assert len(questions) >= 8
    for item in questions:
        assert item["question"]
        assert item["expected"]
        json.dumps(item)
