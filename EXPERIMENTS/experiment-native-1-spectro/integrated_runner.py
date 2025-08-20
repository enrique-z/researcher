#!/usr/bin/env python3
"""
Integrated Runner (OpenAI backend):
- Consumes enhanced inputs in input/
- Uses GPT-5 to generate a paper
- Uses GPT-5 to produce a review/score
- Saves outputs to output/
"""
import os
import json
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

try:
    import openai
except Exception:
    raise SystemExit("Please install openai >= 1.0.0: pip install openai")

OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-5")
REASONING_EFFORT = os.getenv("OPENAI_REASONING_EFFORT", "high")
MAX_PAPER_TOKENS = int(os.getenv("OPENAI_MAX_TOKENS", "12000"))
MAX_REVIEW_TOKENS = int(os.getenv("OPENAI_REVIEW_TOKENS", "4000"))

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

BASE_DIR = os.path.dirname(__file__)
INPUT_DIR = os.path.join(BASE_DIR, "input")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)


def read_inputs():
    with open(os.path.join(INPUT_DIR, "research_topic_formatted.txt"), "r") as f:
        topic = f.read().strip()
    with open(os.path.join(INPUT_DIR, "references.bib"), "r") as f:
        references = f.read().strip()
    comp = None
    comp_path = os.path.join(INPUT_DIR, "comprehensive_results.json")
    if os.path.exists(comp_path):
        try:
            with open(comp_path, "r") as f:
                comp = json.load(f)
        except Exception:
            comp = None
    return topic, references, comp


def build_generation_prompt(topic: str, refs: str, comp: dict | None):
    sys = (
        "You are an expert research assistant. Generate a scientific paper in LaTeX with sections: "
        "Title, Abstract, Introduction, Related Work, Methods. Ground content in the provided references."
    )
    comp_block = ""
    if comp:
        areas = comp.get("research_areas", [])
        areas_preview = "\n".join(f"- {a}" for a in areas[:8])
        qa = comp.get("quality_analysis", {})
        comp_block = (
            "\n\n[Enhanced Experiment Context]\n"
            f"Quality: {qa.get('overall_score')}/10 ({qa.get('quality_level')})\n"
            f"Research areas (subset):\n{areas_preview}\n"
        )
    user = (
        f"Topic:\n{topic}\n\n"
        f"References (BibTeX):\n{refs[:120000]}\n"
        f"{comp_block}\n"
        "Task: Analyze references and context to establish motivation, novelty, and methods. "
        "Then produce LaTeX sections (Title, Abstract, Introduction, Related Work, Methods)."
    )
    return sys, user


def build_review_prompt(paper_tex: str):
    sys = (
        "You are an expert academic reviewer. Provide a thorough review with sections: "
        "Summary, Soundness, Presentation, Contribution, Strengths, Weaknesses, Suggestions, Questions, "
        "Rating (1-10) and Decision (Accept/Reject). Be concise and specific."
    )
    user = (
        "Review the following LaTeX paper draft and produce the sections with clear headings.\n\n" + paper_tex[:160000]
    )
    return sys, user


def chat(model: str, system: str, user: str, max_tokens: int):
    resp = client.chat.completions.create(
        model=model,
        messages=[{"role": "system", "content": system}, {"role": "user", "content": user}],
        max_completion_tokens=max_tokens,
        reasoning_effort=REASONING_EFFORT,
    )
    return resp.choices[0].message.content


def main():
    topic, refs, comp = read_inputs()

    # Step 1: Generate paper
    gen_sys, gen_user = build_generation_prompt(topic, refs, comp)
    print(f"Generating paper with {OPENAI_MODEL} (reasoning_effort={REASONING_EFFORT})...")
    paper = chat(OPENAI_MODEL, gen_sys, gen_user, MAX_PAPER_TOKENS)

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    base = f"paper_integrated_{ts}"
    paper_path = os.path.join(OUTPUT_DIR, base + ".tex")
    with open(paper_path, "w") as f:
        f.write(paper)

    # Step 2: Review paper
    print("Generating review...")
    rev_sys, rev_user = build_review_prompt(paper)
    review = chat(OPENAI_MODEL, rev_sys, rev_user, MAX_REVIEW_TOKENS)
    review_path = os.path.join(OUTPUT_DIR, base + "_review.md")
    with open(review_path, "w") as f:
        f.write(review)

    # Metadata
    meta = {
        "model": OPENAI_MODEL,
        "reasoning_effort": REASONING_EFFORT,
        "paper_path": os.path.basename(paper_path),
        "review_path": os.path.basename(review_path),
        "used_comprehensive_results": bool(comp),
    }
    with open(os.path.join(OUTPUT_DIR, base + ".json"), "w") as f:
        json.dump(meta, f, indent=2)

    print("Done. Files saved in output/.")


if __name__ == "__main__":
    main()




