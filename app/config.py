from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


ROOT = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ROOT / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"
    openai_base_url: str = "https://api.openai.com/v1"

    ollama_base_url: str = "http://127.0.0.1:11434"
    ollama_model: str = "llama3"

    top_k: int = 4
    min_score: float = 0.08
    chunk_size: int = 900
    chunk_overlap: int = 120
    knowledge_dir: Path = ROOT / "data" / "knowledge"
    index_dir: Path = ROOT / "data" / "index"

    host: str = "127.0.0.1"
    api_port: int = 8000
    ui_port: int = 7860


settings = Settings()
