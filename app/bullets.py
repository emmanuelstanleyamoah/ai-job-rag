from __future__ import annotations

import re
from dataclasses import dataclass

SECURITY_COPILOT_BEFORE = (
    "Built an AI Security Detection & Response Copilot using Python, Streamlit, "
    "FastAPI, Gemini, LangGraph, ChromaDB, Microsoft Presidio, and Guardrails AI. "
    "Implemented secure RAG pipelines, multi-agent incident investigation workflows, "
    "MITRE ATT&CK enrichment, Sigma/KQL rule generation, explainable AI, and AI "
    "governance controls to automate SOC operations and improve investigation efficiency."
)

SECURITY_COPILOT_AFTER = (
    "Built a SOC investigation copilot (Python, FastAPI, Streamlit) that retrieves "
    "detection context through a guarded RAG pipeline, maps findings to MITRE ATT&CK, "
    "and drafts Sigma/KQL rules with cited evidence. Presidio redacts sensitive fields "
    "and Guardrails checks prompts before Gemini generation; LangGraph logs triage, "
    "enrichment, and rule-draft steps so an analyst can see which chunk and tool "
    "produced the recommendation."
)

SECURITY_COPILOT_SKILLS = (
    "Python; RAG (ChromaDB, citations); agents (LangGraph); security "
    "(MITRE ATT&CK, Sigma, KQL, Presidio, Guardrails); serving (FastAPI, Streamlit); "
    "models (Gemini)."
)

METRIC_GAP = (
    "Add two measured details before you submit this: corpus or data size, and one of "
    "an eval metric, latency, cost, or a user outcome. Leave them blank until you have "
    "measured them."
)

_LEADING_VERBS = ("built", "shipped", "developed", "implemented", "created", "designed")
_KEEP_IN_BULLET = ("python", "fastapi", "streamlit", "gradio")


@dataclass(frozen=True)
class BulletRewrite:
    bullet: str
    skills: str
    metric_note: str
    example: bool


def extract_bullet(text: str) -> str | None:
    raw = " ".join(text.strip().split())
    if not raw:
        return None
    if ":" in raw:
        tail = raw.split(":", 1)[1].strip()
        if _looks_like_bullet(tail):
            return tail
    if _looks_like_bullet(raw):
        return raw
    return None


def rewrite_project_bullet(text: str) -> BulletRewrite:
    cleaned = " ".join(text.strip().split())
    if _is_security_copilot(cleaned):
        return BulletRewrite(
            bullet=SECURITY_COPILOT_AFTER,
            skills=SECURITY_COPILOT_SKILLS,
            metric_note="",
            example=True,
        )
    return _rewrite_generic(cleaned)


def format_rewrite(result: BulletRewrite) -> str:
    parts = [result.bullet, "", f"Skills: {result.skills or 'No extra libraries to move.'}"]
    if result.metric_note:
        parts.extend(["", result.metric_note])
    return "\n".join(parts)


def _looks_like_bullet(text: str) -> bool:
    if len(text) < 80 or text.endswith("?"):
        return False
    first = text.split(".", 1)[0].lower()
    if any(first.startswith(verb) for verb in _LEADING_VERBS) and " using " in f" {text.lower()} ":
        return True
    return text.lower().startswith(_LEADING_VERBS) and text.count(",") >= 3


def _is_security_copilot(text: str) -> bool:
    folded = text.lower()
    markers = ("security detection", "presidio", "guardrails", "mitre", "sigma")
    return sum(marker in folded for marker in markers) >= 3


def _rewrite_generic(text: str) -> BulletRewrite:
    sentences = re.split(r"(?<=[.!?])\s+", text)
    first = sentences[0]
    system = first
    tools: list[str] = []
    match = re.search(r"\busing\b\s+(.+?)(?:\.|$)", first, flags=re.IGNORECASE)
    if match:
        system = first[: match.start()].strip(" ,.")
        tools = _split_tools(match.group(1))
    system = re.sub(
        r"^(Built|Shipped|Developed|Implemented|Created|Designed)\s+",
        "",
        system,
        flags=re.IGNORECASE,
    ).strip()
    kept = [tool for tool in tools if _keep(tool)]
    moved = [tool for tool in tools if not _keep(tool)]
    feature = ""
    if len(sentences) > 1:
        feature = re.sub(
            r"^(Implemented|Built|Added|Developed|Created)\s+",
            "",
            sentences[1],
            flags=re.IGNORECASE,
        )
        feature = re.sub(
            r"\s+to\s+(automate|improve|enhance|streamline)\b.+$",
            "",
            feature,
            flags=re.IGNORECASE,
        ).strip(" .")
    parenthetical = f" ({', '.join(kept)})" if kept else ""
    if feature:
        clause = _lower_first(feature)
        if not clause.startswith(("retriev", "map", "draft", "log", "check", "redact")):
            clause = f"covers {_lower_first(feature)}"
        bullet = f"Built {system}{parenthetical} that {clause}."
    else:
        bullet = f"Built {system}{parenthetical}."
    has_number = bool(re.search(r"\d", text))
    metric_note = (
        "Keep only numbers you measured, and name the eval set they came from."
        if has_number
        else METRIC_GAP
    )
    skills = ", ".join(moved) + "." if moved else ""
    return BulletRewrite(bullet=bullet, skills=skills, metric_note=metric_note, example=False)


def _split_tools(raw: str) -> list[str]:
    raw = raw.replace(" and ", ", ")
    parts = [part.strip(" .") for part in raw.split(",")]
    return [part for part in parts if part]


def _keep(tool: str) -> bool:
    folded = tool.lower()
    return any(name in folded for name in _KEEP_IN_BULLET)


def _lower_first(text: str) -> str:
    if not text:
        return text
    return text[0].lower() + text[1:]
