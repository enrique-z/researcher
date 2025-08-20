#!/usr/bin/env python3
"""
OpenAI Runner: Generate research paper(s) using OpenAI models instead of vLLM/Westlake local models.
Reads from input/ (topic + references) and writes outputs to output/.
Also enriches the prompt with input/comprehensive_results.json if available.
"""
import os
import json
from datetime import datetime

from dotenv import load_dotenv
load_dotenv()

try:
    import openai  # openai>=1.0.0 SDK
except Exception:
    raise SystemExit("Please install openai >= 1.0.0: pip install openai")

OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-5")
NUM_PAPERS = int(os.getenv("OPENAI_NUM_PAPERS", "1"))
MAX_TOKENS = int(os.getenv("OPENAI_MAX_TOKENS", "12000"))
REASONING_EFFORT = os.getenv("OPENAI_REASONING_EFFORT", "high")

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

EXPERIMENT_DIR = os.path.dirname(__file__)
INPUT_DIR = os.path.join(EXPERIMENT_DIR, "input")
OUTPUT_DIR = os.path.join(EXPERIMENT_DIR, "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)


def read_inputs():
    with open(os.path.join(INPUT_DIR, "research_topic_formatted.txt"), "r") as f:
        topic = f.read().strip()
    with open(os.path.join(INPUT_DIR, "references.bib"), "r") as f:
        references = f.read().strip()
    # optional comprehensive results
    comp_path = os.path.join(INPUT_DIR, "comprehensive_results.json")
    comp = None
    if os.path.exists(comp_path):
        try:
            with open(comp_path, "r") as f:
                comp = json.load(f)
        except Exception:
            comp = None
    return topic, references, comp


def build_prompts(topic: str, references: str, comp: dict | None):
    system_prompt = (
        "You are an expert research assistant generating a scientific paper from provided literature. "
        "Write in LaTeX with sections: Title, Abstract, Introduction, Related Work, Methods. "
        "Ground content in the provided references when possible."
    )
    # Include enriched context from comprehensive_results.json if present
    comp_block = ""
    if comp:
        areas = comp.get("research_areas", [])
        areas_preview = "\n".join(f"- {a}" for a in areas[:8])
        qa = comp.get("quality_analysis", {})
        overall = qa.get("overall_score")
        qlevel = qa.get("quality_level")
        comp_block = (
            "\n\n[Enhanced Experiment Context]\n"
            f"Quality: {overall}/10 ({qlevel})\n"
            f"Research areas (subset):\n{areas_preview}\n"
        )
    user_prompt = (
        f"Topic:\n{topic}\n\n"
        f"References (BibTeX):\n{references[:120000]}\n"
        f"{comp_block}\n"
        "Task: Analyze references and enhanced context to establish motivation and novelty. "
        "Then produce the paper sections in LaTeX (Title, Abstract, Introduction, Related Work, Methods)."
    )
    return system_prompt, user_prompt


def generate_paper(system_prompt: str, user_prompt: str):
    resp = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}],
        max_completion_tokens=MAX_TOKENS,
        reasoning_effort=REASONING_EFFORT,
    )
    return resp.choices[0].message.content


def main():
    topic, references, comp = read_inputs()
    sys_prompt, usr_prompt = build_prompts(topic, references, comp)

    papers = []
    for i in range(NUM_PAPERS):
        print(f"Generating paper {i+1}/{NUM_PAPERS} with {OPENAI_MODEL} (reasoning_effort={REASONING_EFFORT})...")
        content = generate_paper(sys_prompt, usr_prompt)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        base = f"paper_openai_{ts}_{i+1}"
        # Save raw content (Markdown/LaTeX-like)
        with open(os.path.join(OUTPUT_DIR, base + ".tex"), "w") as f:
            f.write(content)
        # Save minimal metadata
        meta = {
            "model": OPENAI_MODEL,
            "timestamp": ts,
            "tokens": MAX_TOKENS,
            "reasoning_effort": REASONING_EFFORT,
            "topic_preview": topic[:200],
            "used_comprehensive_results": bool(comp),
        }
        with open(os.path.join(OUTPUT_DIR, base + ".json"), "w") as f:
            json.dump(meta, f, indent=2)
        papers.append({"path": base + ".tex", "meta": meta})

    # Summary index
    summary = {"papers": papers, "count": len(papers)}
    with open(os.path.join(OUTPUT_DIR, "openai_generation_summary.json"), "w") as f:
        json.dump(summary, f, indent=2)
    print("Done. Files saved in output/.")


if __name__ == "__main__":
    main()
