from __future__ import annotations

from functools import lru_cache

import gradio as gr

from app.bullets import SECURITY_COPILOT_BEFORE
from app.rag import RagPipeline

EXAMPLES = [
    "How should I structure an AI engineering resume?",
    "What portfolio projects actually get interviews?",
    "What does an AI engineer interview loop look like?",
    "How do I talk about RAG projects in interviews?",
    "What weekly job-search routine should I follow?",
    SECURITY_COPILOT_BEFORE,
]


@lru_cache(maxsize=1)
def get_pipeline() -> RagPipeline:
    return RagPipeline()


def respond(message: str, history: list[dict[str, str]]) -> str:
    del history
    result = get_pipeline().ask(message)
    if not result.sources:
        return result.answer
    citations = "\n".join(
        f"- {hit.title} (`{hit.source}`, score {hit.score:.3f})"
        for hit in result.sources
    )
    return f"{result.answer}\n\n**Sources**\n{citations}"


def build_ui() -> gr.Blocks:
    with gr.Blocks(title="AI Job Coach") as demo:
        gr.Markdown(
            """
            # AI Job Coach
            Ask how to land an **AI engineering** role. Answers come from the bootcamp
            knowledge base (resume, projects, interviews, search strategy), not from
            generic internet advice.
            """
        )
        gr.ChatInterface(
            fn=respond,
            examples=EXAMPLES,
        )
    return demo


def launch() -> None:
    from app.config import settings

    build_ui().launch(
        server_name=settings.host,
        server_port=settings.ui_port,
        show_error=True,
    )
