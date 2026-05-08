"""Step 2 - Prompt Hub and deterministic A/B routing."""

from __future__ import annotations

import hashlib
import os

from langchain_core.output_parsers import StrOutputParser
from langsmith import Client, traceable

from config import load_environment
from lab_utils import build_prompt_v1, build_prompt_v2, build_vectorstore, format_docs, make_llm
from qa_pairs import SAMPLE_QUESTIONS

PROMPT_V1_NAME = "day22-rag-prompt-v1"
PROMPT_V2_NAME = "day22-rag-prompt-v2"
PROMPT_V1 = build_prompt_v1()
PROMPT_V2 = build_prompt_v2()


def push_prompts_to_hub(client: Client) -> None:
    """Push both prompt versions to LangSmith Prompt Hub."""

    try:
        url = client.push_prompt(PROMPT_V1_NAME, object=PROMPT_V1, description="V1 - concise answers")
        print(f"✅ Pushed V1 → {url}")
    except Exception as exc:
        print(f"⚠️  V1 push skipped: {exc}")

    try:
        url = client.push_prompt(PROMPT_V2_NAME, object=PROMPT_V2, description="V2 - structured answers")
        print(f"✅ Pushed V2 → {url}")
    except Exception as exc:
        print(f"⚠️  V2 push skipped: {exc}")


def pull_prompts_from_hub(client: Client) -> dict[str, object]:
    """Pull both prompt versions back from LangSmith Prompt Hub."""

    prompts: dict[str, object] = {}

    try:
        prompts[PROMPT_V1_NAME] = client.pull_prompt(PROMPT_V1_NAME)
        print(f"↓ Pulled '{PROMPT_V1_NAME}' from Hub")
    except Exception:
        prompts[PROMPT_V1_NAME] = PROMPT_V1
        print(f"ℹ️  Using local fallback for '{PROMPT_V1_NAME}'")

    try:
        prompts[PROMPT_V2_NAME] = client.pull_prompt(PROMPT_V2_NAME)
        print(f"↓ Pulled '{PROMPT_V2_NAME}' from Hub")
    except Exception:
        prompts[PROMPT_V2_NAME] = PROMPT_V2
        print(f"ℹ️  Using local fallback for '{PROMPT_V2_NAME}'")

    return prompts


def get_prompt_version(request_id: str) -> str:
    """Deterministically map a request id to prompt V1 or V2."""

    hash_int = int(hashlib.md5(request_id.encode()).hexdigest(), 16)
    return PROMPT_V1_NAME if hash_int % 2 == 0 else PROMPT_V2_NAME


@traceable(name="ab-rag-query", tags=["ab-test", "step2"])
def ask_ab(retriever, llm, prompt, question: str, version: str) -> dict:
    """Run the RAG chain for one question and return the answer plus version."""

    docs = retriever.invoke(question)
    context = format_docs(docs)
    answer = (prompt | llm | StrOutputParser()).invoke({"context": context, "question": question})
    return {"question": question, "answer": answer, "version": version}


def main() -> None:
    load_environment()
    print("=" * 60)
    print("  Step 2: Prompt Hub A/B Routing")
    print("=" * 60)

    client = Client(api_key=os.environ.get("LANGCHAIN_API_KEY"))
    push_prompts_to_hub(client)
    prompts = pull_prompts_from_hub(client)

    vectorstore = build_vectorstore()
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    llm = make_llm()

    counts = {PROMPT_V1_NAME: 0, PROMPT_V2_NAME: 0}
    for index, question in enumerate(SAMPLE_QUESTIONS, 1):
        request_id = f"req-{index:04d}"
        version_key = get_prompt_version(request_id)
        version_tag = "v1" if version_key == PROMPT_V1_NAME else "v2"
        prompt = prompts[version_key]

        result = ask_ab(retriever, llm, prompt, question, version_tag)
        counts[version_key] += 1
        print(f"[{index:02d}] [prompt-{version_tag}] {result['question'][:55]}...")

    print("\nRouting summary:")
    print(f"  {PROMPT_V1_NAME}: {counts[PROMPT_V1_NAME]}")
    print(f"  {PROMPT_V2_NAME}: {counts[PROMPT_V2_NAME]}")


if __name__ == "__main__":
    main()
