"""Shared helpers for the Day 22 lab scripts."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

from config import KNOWLEDGE_BASE_PATH, load_environment, get_chat_model, get_embeddings

from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter

ROOT_DIR = Path(__file__).resolve().parent


def load_knowledge_base_text() -> str:
    """Read the knowledge base text used for retrieval."""

    load_environment()
    return KNOWLEDGE_BASE_PATH.read_text(encoding="utf-8")


def build_vectorstore():
    """Chunk the knowledge base and index it in FAISS."""

    text = load_knowledge_base_text()
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_text(text)
    embeddings = get_embeddings()
    return FAISS.from_texts(chunks, embedding=embeddings)


def format_docs(docs: Iterable) -> str:
    """Join retrieved documents into a single context string."""

    return "\n\n".join(doc.page_content for doc in docs)


def build_rag_prompt() -> ChatPromptTemplate:
    """Prompt used by the base RAG chain."""

    return ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a helpful assistant. Use only the provided context to answer.\n\nContext:\n{context}",
            ),
            ("human", "{question}"),
        ]
    )


def build_prompt_v1() -> ChatPromptTemplate:
    """Concise prompt version for A/B testing."""

    return ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a helpful AI assistant. Answer using only the provided context. Keep the answer concise, ideally 2-4 sentences. If the context is insufficient, say you do not have enough information.\n\nContext:\n{context}",
            ),
            ("human", "{question}"),
        ]
    )


def build_prompt_v2() -> ChatPromptTemplate:
    """Structured prompt version for A/B testing."""

    return ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are an expert AI tutor. Read the context carefully and answer in a structured, accurate way. Use 3-5 sentences, explain the key facts clearly, and state explicitly when the context does not contain enough information.\n\nContext:\n{context}",
            ),
            ("human", "{question}"),
        ]
    )


def make_llm(temperature: float = 0.0):
    """Create the application LLM."""

    return get_chat_model(temperature=temperature)


def make_embeddings():
    """Create the embedding model used for retrieval and evaluation."""

    return get_embeddings()

