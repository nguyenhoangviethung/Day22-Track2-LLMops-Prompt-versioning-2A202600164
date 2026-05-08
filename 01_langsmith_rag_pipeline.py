"""Step 1 - LangSmith-instrumented RAG pipeline."""

from __future__ import annotations

import os

from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langsmith import traceable

from config import load_environment
from lab_utils import build_rag_prompt, build_vectorstore, format_docs, make_llm
from qa_pairs import SAMPLE_QUESTIONS


def build_rag_chain(vectorstore):
    """Build the retriever -> prompt -> LLM -> parser chain."""

    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    prompt = build_rag_prompt()
    llm = make_llm()

    chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    return chain, retriever


@traceable(name="rag-query", tags=["rag", "step1"])
def ask(chain, question: str) -> str:
    """Run one traced RAG query."""

    return chain.invoke(question)


def main() -> None:
    load_environment()
    print("=" * 60)
    print("  Step 1: LangSmith RAG Pipeline")
    print("=" * 60)

    vectorstore = build_vectorstore()
    chain, _ = build_rag_chain(vectorstore)

    for index, question in enumerate(SAMPLE_QUESTIONS, 1):
        answer = ask(chain, question)
        print(f"[{index:02d}/{len(SAMPLE_QUESTIONS)}] Q: {question[:60]}")
        print(f"       A: {answer[:120]}\n")

    print(f"✅ {len(SAMPLE_QUESTIONS)} traces sent to LangSmith project '{os.environ.get('LANGCHAIN_PROJECT')}'")
    print("   Open https://smith.langchain.com to view traces.")


if __name__ == "__main__":
    main()
