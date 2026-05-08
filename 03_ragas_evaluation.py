"""Step 3 - RAGAS evaluation for both prompt versions."""

from __future__ import annotations

import json
import warnings

warnings.filterwarnings("ignore")

import numpy as np
from langchain_core.output_parsers import StrOutputParser
from langsmith import traceable
from ragas import EvaluationDataset, SingleTurnSample, evaluate
from ragas.metrics import answer_relevancy, context_precision, context_recall, faithfulness

from config import RAGAS_REPORT_PATH, load_environment
from lab_utils import build_prompt_v1, build_prompt_v2, build_vectorstore, format_docs, make_llm, make_embeddings
from qa_pairs import QA_PAIRS

PROMPTS = {"v1": build_prompt_v1(), "v2": build_prompt_v2()}


def build_ragas_dataset(rag_results: list[dict]):
    """Convert raw RAG outputs into a RAGAS EvaluationDataset."""

    samples = [
        SingleTurnSample(
            user_input=item["question"],
            response=item["answer"],
            retrieved_contexts=item["contexts"],
            reference=item["reference"],
        )
        for item in rag_results
    ]
    return EvaluationDataset(samples=samples)


@traceable(name="rag-eval-query", tags=["step3"])
def run_rag(retriever, llm, prompt, question: str) -> dict:
    """Run one RAG query and return answer plus retrieved contexts."""

    docs = retriever.invoke(question)
    contexts = [doc.page_content for doc in docs]
    context_text = format_docs(docs)
    answer = (prompt | llm | StrOutputParser()).invoke({"context": context_text, "question": question})
    return {"answer": answer, "contexts": contexts}


def collect_rag_outputs(vectorstore, prompt_version: str) -> list[dict]:
    """Run all QA pairs through a specific prompt version."""

    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    llm = make_llm()
    prompt = PROMPTS[prompt_version]

    results: list[dict] = []
    print(f"\nRunning 50 questions with prompt {prompt_version} ...")

    for index, qa in enumerate(QA_PAIRS, 1):
        output = run_rag(retriever, llm, prompt, qa["question"])
        results.append(
            {
                "question": qa["question"],
                "reference": qa["reference"],
                "answer": output["answer"],
                "contexts": output["contexts"],
            }
        )
        print(f"  [{index:02d}/50] {qa['question'][:60]}")

    return results


def _mean_metric(result, metric_name: str) -> float:
    values = result[metric_name]
    filtered = [value for value in values if value is not None]
    return float(np.mean(filtered)) if filtered else 0.0


def run_ragas_eval(rag_results: list[dict], version: str) -> dict[str, float]:
    """Evaluate one set of RAG outputs using the four required metrics."""

    print(f"\n📐 Running RAGAS evaluation for prompt {version} ...")
    dataset = build_ragas_dataset(rag_results)
    llm_eval = make_llm()
    emb_eval = make_embeddings()

    result = evaluate(
        dataset,
        metrics=[faithfulness, answer_relevancy, context_recall, context_precision],
        llm=llm_eval,
        embeddings=emb_eval,
    )

    scores = {
        "faithfulness": _mean_metric(result, "faithfulness"),
        "answer_relevancy": _mean_metric(result, "answer_relevancy"),
        "context_recall": _mean_metric(result, "context_recall"),
        "context_precision": _mean_metric(result, "context_precision"),
    }

    for key, value in scores.items():
        star = " ⭐" if key == "faithfulness" and value >= 0.8 else ""
        print(f"  {key:30s}: {value:.4f}{star}")

    return scores


def save_report(v1_scores: dict[str, float], v2_scores: dict[str, float]) -> None:
    """Persist a JSON report for later submission."""

    report = {
        "v1": v1_scores,
        "v2": v2_scores,
        "comparison": {
            metric: {"v1": v1_scores[metric], "v2": v2_scores[metric]}
            for metric in v1_scores
        },
    }
    RAGAS_REPORT_PATH.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"\n✅ Saved report to {RAGAS_REPORT_PATH}")


def main() -> None:
    load_environment()
    print("=" * 60)
    print("  Step 3: RAGAS Evaluation")
    print("=" * 60)

    vectorstore = build_vectorstore()
    v1_results = collect_rag_outputs(vectorstore, "v1")
    v2_results = collect_rag_outputs(vectorstore, "v2")

    v1_scores = run_ragas_eval(v1_results, "v1")
    v2_scores = run_ragas_eval(v2_results, "v2")

    print("\nComparison table:")
    for metric in ["faithfulness", "answer_relevancy", "context_recall", "context_precision"]:
        s1, s2 = v1_scores[metric], v2_scores[metric]
        winner = "← V1" if s1 > s2 else "← V2"
        print(f"  {metric:30s}: V1={s1:.4f}  V2={s2:.4f}  {winner}")

    best_faith = max(v1_scores["faithfulness"], v2_scores["faithfulness"])
    if best_faith >= 0.8:
        print(f"✅ Target met: faithfulness = {best_faith:.4f}")
    else:
        print(f"⚠️  Target not met yet: faithfulness = {best_faith:.4f}")

    save_report(v1_scores, v2_scores)


if __name__ == "__main__":
    main()
