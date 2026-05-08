"""Run the Day 22 lab scripts in sequence."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent
STEP_SCRIPTS = {
    1: "01_langsmith_rag_pipeline.py",
    2: "02_prompt_hub_ab_routing.py",
    3: "03_ragas_evaluation.py",
    4: "04_guardrails_validator.py",
}


def run_script(script_name: str) -> None:
    script_path = ROOT_DIR / script_name
    print(f"\n=== Running {script_name} ===")
    subprocess.run([sys.executable, str(script_path)], check=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the Day 22 lab scripts.")
    parser.add_argument("--step", type=int, choices=STEP_SCRIPTS.keys(), help="Run a single step only")
    args = parser.parse_args()

    if args.step:
        run_script(STEP_SCRIPTS[args.step])
        return

    for step in sorted(STEP_SCRIPTS):
        run_script(STEP_SCRIPTS[step])


if __name__ == "__main__":
    main()
