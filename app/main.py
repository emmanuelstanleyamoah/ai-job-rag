from __future__ import annotations

import argparse
import logging

import uvicorn

from app.config import settings
from app.retriever import TfidfRetriever
from app.ui import launch


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")
    parser = argparse.ArgumentParser(description="AI Job Coach RAG chatbot")
    parser.add_argument(
        "command",
        nargs="?",
        default="ui",
        choices=["ui", "api", "ingest", "eval"],
        help="ui = Gradio chat, api = FastAPI, ingest = rebuild the index, eval = recall@k",
    )
    args = parser.parse_args()

    if args.command == "ingest":
        retriever = TfidfRetriever.build()
        print(f"Indexed {len(retriever.chunks)} chunks from {settings.knowledge_dir}")
        return
    if args.command == "eval":
        from app.evaluate import run_eval

        report = run_eval()
        if report.misses:
            raise SystemExit(1)
        return
    if args.command == "api":
        uvicorn.run(
            "app.api:app",
            host=settings.host,
            port=settings.api_port,
            reload=False,
        )
        return
    launch()


if __name__ == "__main__":
    main()
