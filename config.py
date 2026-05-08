"""Shared configuration helpers for the Day 22 lab."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

try:
    from dotenv import load_dotenv
except Exception:  # pragma: no cover - optional during syntax checks
    load_dotenv = None

ROOT_DIR = Path(__file__).resolve().parent
DATA_DIR = ROOT_DIR / "data"
EVIDENCE_DIR = ROOT_DIR / "evidence"
KNOWLEDGE_BASE_PATH = DATA_DIR / "knowledge_base.txt"
RAGAS_REPORT_PATH = DATA_DIR / "ragas_report.json"
ENV_PATH = ROOT_DIR / ".env"

DEFAULT_LANGCHAIN_PROJECT = os.getenv("LANGCHAIN_PROJECT", "day22-langsmith-lab")
DEFAULT_LLM_MODEL = os.getenv("OPENAI_MODEL", "gpt-5.4-mini")
DEFAULT_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")


def ensure_directories() -> None:
    """Create standard lab folders if they do not already exist."""

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)


def load_environment() -> None:
    """Load .env values and apply the defaults required for tracing."""

    ensure_directories()
    if load_dotenv is not None and ENV_PATH.exists():
        load_dotenv(ENV_PATH, override=False)

    os.environ.setdefault("LANGCHAIN_TRACING_V2", "true")
    os.environ.setdefault("LANGCHAIN_PROJECT", DEFAULT_LANGCHAIN_PROJECT)
    os.environ.setdefault("LANGCHAIN_ENDPOINT", "https://api.smith.langchain.com")


def get_setting(name: str, default: str = "") -> str:
    """Read an environment value with a fallback."""

    value = os.getenv(name, default)
    return value or default


def _build_openai_kwargs(model: str) -> dict[str, Any]:
    kwargs: dict[str, Any] = {"model": model}
    api_key = os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("OPENAI_BASE_URL")

    if api_key:
        kwargs["api_key"] = api_key
    if base_url:
        kwargs["base_url"] = base_url
    return kwargs


def get_chat_model(model: str | None = None, temperature: float = 0.0):
    """Create a ChatOpenAI model configured from the environment."""

    from langchain_openai import ChatOpenAI

    return ChatOpenAI(temperature=temperature, **_build_openai_kwargs(model or DEFAULT_LLM_MODEL))


def get_embeddings(model: str | None = None):
    """Create an OpenAIEmbeddings instance configured from the environment."""

    from langchain_openai import OpenAIEmbeddings

    return OpenAIEmbeddings(**_build_openai_kwargs(model or DEFAULT_EMBEDDING_MODEL))


def print_config() -> None:
    """Print a short configuration summary for quick verification."""

    load_environment()
    print("✅ Config loaded successfully")
    print(f"   LangSmith project : {os.getenv('LANGCHAIN_PROJECT', DEFAULT_LANGCHAIN_PROJECT)}")
    print(f"   OpenAI endpoint   : {os.getenv('OPENAI_BASE_URL', 'https://api.openai.com/v1')}")
    print(f"   Default LLM model : {os.getenv('OPENAI_MODEL', DEFAULT_LLM_MODEL)}")
    print(f"   Embedding model   : {os.getenv('OPENAI_EMBEDDING_MODEL', DEFAULT_EMBEDDING_MODEL)}")


if __name__ == "__main__":
    print_config()
