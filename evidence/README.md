# evidence/ README — Day 22 Lab

Mục đích: tệp này liệt kê evidence hiện có, chỉ ra những file cần đổi tên hoặc tạo thêm để đúng với rubric, và cung cấp các lệnh nhanh để sửa.

## 1) Files required by rubric (expected exact names)

- `evidence/01_langsmith_traces.png`  (LangSmith traces screenshot)
- `evidence/02_prompt_hub.png`       (Prompt Hub showing 2 prompt versions)
- `evidence/02_ab_routing_log.txt`   (A/B routing terminal log)
- `evidence/03_ragas_scores.png`     (Terminal screenshot comparing V1 vs V2)
- `evidence/03_ragas_report.json`    (Copy of `data/ragas_report.json`)
- `evidence/04_pii_demo_log.txt`     (PII validator demo log)
- `evidence/04_json_demo_log.txt`    (JSON repair demo log)

## 2) Current status in this repo

Found in `evidence/`:

- `01_langsmith_traces.png` ✅
- `02_ab_routing_log.txt` ✅
- `02_prompt_hub.png` ✅ 
- `02_prompt_hub_v1.png` Bonus
- `02_prompt_hub_v2.png` Bonus
- `03_ragas_report.json` ✅ 
- `03_ragas_scores.png` ✅
- `03_ragas_scores.txt` ✅
- `04_pii_demo_log.txt` ✅
- `04_json_demo_log.txt` ✅


## 3) LangSmith project URL

```
https://smith.langchain.com/o/<org-id>/projects/p/<project-id>
```

Put the real URL below so graders can verify traces:

LangSmith project URL: ___________________________

## 4) Final submission checklist (tick locally before push)

- [X] `evidence/01_langsmith_traces.png` exists and shows ≥ 50 traces
- [X] `evidence/02_prompt_hub.png` exists and displays both prompt versions
- [X] `evidence/02_ab_routing_log.txt` contains per-request labels (`[prompt-v1]`/`[prompt-v2]`)
- [X] `evidence/03_ragas_scores.png` screenshot of metrics table
- [X] `evidence/03_ragas_report.json` (copy of `data/ragas_report.json`)
- [X] `evidence/04_pii_demo_log.txt` contains PII redaction examples
- [X] `evidence/04_json_demo_log.txt` contains JSON repair examples
- [X] `.env` NOT committed; no API keys in repo
- [X] `README.md` / `GUIDE.md` updated with LangSmith URL

## Results summary (from logs & screenshots)

- LangSmith project name: `day22-langsmith-lab` (50 traces recorded)
- Prompt Hub pushed:
	- V1: https://smith.langchain.com/prompts/day22-rag-prompt-v1/36945785?organizationId=6dbcc79f-7b48-435a-9c37-fa06251b1b82
	- V2: https://smith.langchain.com/prompts/day22-rag-prompt-v2/3b75dd21?organizationId=6dbcc79f-7b48-435a-9c37-fa06251b1b82
- A/B routing summary (from run):
	- `day22-rag-prompt-v1`: 19 queries
	- `day22-rag-prompt-v2`: 31 queries

### RAGAS evaluation (summary)

Results saved to `data/ragas_report.json` and copied to `evidence/03_ragas_report.json` (if not already).

- Faithfulness: V1 = 0.8403  ✅ (meets rubric target ≥ 0.8)
- Faithfulness: V2 = 0.6243
- Answer relevancy: V1 = 0.8866, V2 = 0.5977
- Context recall: V1 = 0.75, V2 = 0.79
- Context precision: V1 = 0.9433, V2 = 0.9533

### Notes

- Target met: faithfulness = 0.8403 (V1). Save `evidence/03_ragas_report.json` as proof.
- Prompt Hub screenshots: please ensure `evidence/02_prompt_hub.png` exists (combine or rename existing prompt screenshots). This is required by rubric.
- LangSmith traces screenshot: `evidence/01_langsmith_traces.png` must clearly show project name and number of traces.


