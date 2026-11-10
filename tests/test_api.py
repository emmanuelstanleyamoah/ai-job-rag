from fastapi.testclient import TestClient

from app.api import app
from app.bullets import SECURITY_COPILOT_BEFORE
from app.llm import ABSTAIN
from app.rag import RagPipeline


def test_health():
    response = TestClient(app).get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_chat_rewrites_security_bullet():
    response = TestClient(app).post("/chat", json={"question": SECURITY_COPILOT_BEFORE})
    assert response.status_code == 200
    body = response.json()
    assert "SOC investigation copilot" in body["answer"]
    assert body["sources"]


def test_unknown_question_abstains_without_calling_the_model(monkeypatch):
    called = []
    monkeypatch.setattr(
        "app.rag.generate_answer",
        lambda *_args, **_kwargs: called.append(True),
    )
    result = RagPipeline().ask("What is the capital of France?")
    assert result.answer == ABSTAIN
    assert result.sources == []
    assert called == []


def test_chat_abstains_for_unknown_question():
    response = TestClient(app).post(
        "/chat",
        json={"question": "What is the capital of France?"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["answer"] == ABSTAIN
    assert body["sources"] == []
