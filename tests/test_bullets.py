from app.bullets import (
    SECURITY_COPILOT_BEFORE,
    extract_bullet,
    rewrite_project_bullet,
)


def test_security_copilot_bullet_is_rewritten_without_invented_metrics():
    result = rewrite_project_bullet(SECURITY_COPILOT_BEFORE)
    assert "SOC investigation copilot" in result.bullet
    assert "Presidio" in result.bullet
    assert "Sigma/KQL" in result.bullet
    assert result.example is True
    assert "31%" not in result.bullet
    assert not any(char.isdigit() for char in result.bullet)
    assert "ChromaDB" in result.skills
    assert result.metric_note == ""


def test_generic_tool_list_moves_libraries_to_skills():
    result = rewrite_project_bullet(
        "Built a chatbot using LangChain, OpenAI, and Pinecone. "
        "Implemented chat history to improve user experience."
    )
    assert result.example is False
    assert "LangChain" not in result.bullet
    assert "LangChain" in result.skills
    assert "covers chat history" in result.bullet


def test_extracts_bullet_after_a_label():
    bullet = extract_bullet(f"Please fix this bullet: {SECURITY_COPILOT_BEFORE}")
    assert bullet is not None
    assert bullet.startswith("Built an AI Security")
