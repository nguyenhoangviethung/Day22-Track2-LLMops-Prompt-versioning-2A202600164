# Lab Report — Day 22: LangSmith + Prompt Versioning

Tóm tắt kết quả dựa trên log và screenshot đã chạy (ngày 2026-05-08).

## 1) Tổng quan

- Project: `day22-langsmith-lab`
- Toàn bộ 4 bước script đã chạy (`01` → `04`) — xem `log.log` và `evidence/` folder.
- LangSmith traces: 50 traces were sent and visible in the LangSmith project (screenshot in evidence).

## 2) Task status

- Task 1 — LangSmith RAG Pipeline: COMPLETED
  - 50 queries executed; traces include input, retrieved context, and LLM output.

- Task 2 — Prompt Hub & A/B Routing: COMPLETED
  - Two prompt versions pushed to LangSmith Prompt Hub (links below).
  - Routing deterministic (MD5 hash) produced distribution: V1=19, V2=31.
  - Evidence: `evidence/02_ab_routing_log.txt` and Prompt Hub screenshots.

- Task 3 — RAGAS Evaluation: COMPLETED
  - Evaluated 50 QA pairs for both prompt versions.
  - Metrics computed: `faithfulness`, `answer_relevancy`, `context_recall`, `context_precision`.
  - Report saved to `data/ragas_report.json` and copied to `evidence/03_ragas_report.json`.

- Task 4 — Guardrails Validators: COMPLETED
  - Custom PII detector and JSON formatter implemented and demonstrated.
  - Evidence logs: `evidence/04_pii_demo_log.txt`, `evidence/04_json_demo_log.txt`.

## 3) Key numeric results (from RAGAS)

- Faithfulness: V1 = 0.8403  (meets rubric ≥ 0.8) — V1 is better
- Faithfulness: V2 = 0.6243
- Answer relevancy: V1 = 0.8866  |  V2 = 0.5977
- Context recall: V1 = 0.75  |  V2 = 0.79
- Context precision: V1 = 0.9433  |  V2 = 0.9533

## 4) Evidence files included

- `evidence/01_langsmith_traces.png`  — LangSmith traces screenshot (50 traces)
- `evidence/02_ab_routing_log.txt`    — A/B routing terminal log (labels per request)
- `evidence/02_prompt_hub.png`       — (please create or confirm; rubric requires this)
- `evidence/03_ragas_scores.png`     — RAGAS comparison screenshot
- `evidence/03_ragas_report.json`    — Copy of `data/ragas_report.json`
- `evidence/04_pii_demo_log.txt`     — PII validator demo logs
- `evidence/04_json_demo_log.txt`    — JSON formatter demo logs

Note: If any of the filenames above are missing or misspelled, rename/copy them to match exactly before submission.

## 5) LangSmith / Prompt Hub links (from run)

- LangSmith project (open in browser to verify traces): https://smith.langchain.com/
- Prompt Hub V1: https://smith.langchain.com/hub/nguyenhoangviethung/day22-rag-prompt-v1/36945785?organizationId=9c3c26b3-393e-4af7-a04a-46844e7a3027&tab=0
- Prompt Hub V2: https://smith.langchain.com/hub/nguyenhoangviethung/day22-rag-prompt-v2?organizationId=9c3c26b3-393e-4af7-a04a-46844e7a3027




