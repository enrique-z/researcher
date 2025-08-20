#!/usr/bin/env python3
import os, json, time
from datetime import datetime, timedelta
from dotenv import load_dotenv
load_dotenv()
try:
    import openai
except Exception:
    raise SystemExit("pip install openai python-dotenv")

# Config
MODEL = os.getenv("OPENAI_MODEL", "gpt-5")
REASONING = os.getenv("OPENAI_REASONING_EFFORT", "high")
MAX_GEN = int(os.getenv("OPENAI_MAX_TOKENS", "12000"))
MAX_REV = int(os.getenv("OPENAI_REVIEW_TOKENS", "4000"))
HOURS = float(os.getenv("OPENAI_EXPERIMENT_HOURS", "4.0"))
SLEEP_S = int(os.getenv("OPENAI_SLEEP_SECONDS", "5"))

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
BASE = os.path.dirname(__file__)
INP, OUT, LOGS = [os.path.join(BASE, p) for p in ("input","output","logs")]
os.makedirs(OUT, exist_ok=True); os.makedirs(LOGS, exist_ok=True)

# IO helpers
with open(os.path.join(INP,"research_topic_formatted.txt")) as f: TOPIC = f.read().strip()
with open(os.path.join(INP,"references.bib")) as f: REFS = f.read().strip()
COMP = None
cp = os.path.join(INP,"comprehensive_results.json")
if os.path.exists(cp):
    try: COMP = json.load(open(cp))
    except: COMP = None
areas = (COMP or {}).get("research_areas", []) or ["recent advances methodology field"]

paper_path = os.path.join(OUT, "paper_gpt5_integrated.tex")
review_path = os.path.join(OUT, "paper_gpt5_integrated_review.md")
meta_path = os.path.join(OUT, "paper_gpt5_integrated_meta.json")
log_path = os.path.join(LOGS, f"openai_long_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")

# Chat helper
def chat(system, user, max_tokens):
    r = client.chat.completions.create(
        model=MODEL,
        messages=[{"role":"system","content":system},{"role":"user","content":user}],
        max_completion_tokens=max_tokens,
        reasoning_effort=REASONING,
    )
    return r.choices[0].message.content

# Prompts
def gen_prompt(area):
    sys = (
        "You are an expert researcher. Write LaTeX for a section advancing a full paper. "
        "Focus on the given research area; ground claims in provided references."
    )
    comp_blk = ""
    if COMP:
        qa = COMP.get("quality_analysis", {})
        comp_blk = f"\n[Quality {qa.get('overall_score')}/10 {qa.get('quality_level')}]\n"
    user = (
        f"Topic:{os.linesep}{TOPIC}\n\nReferences (BibTeX):\n{REFS[:90000]}\n\n"
        f"Research area: {area}\n{comp_blk}"
        "Task: Write a cohesive LaTeX section (with subsection title) integrating this area into the paper."
    )
    return sys, user

def rev_prompt(content):
    sys = (
        "You are an expert academic reviewer. Provide concise review with headings: "
        "Summary, Soundness, Presentation, Contribution, Strengths, Weaknesses, Suggestions, Questions, Rating (1-10)."
    )
    user = "Review this LaTeX content and provide the sections:\n\n" + content[-150000:]
    return sys, user

# Main loop
start, end = datetime.now(), datetime.now() + timedelta(hours=HOURS)
state = {"model": MODEL, "reasoning": REASONING, "areas_total": len(areas), "checkpoints": []}
open(paper_path, "a").close(); open(review_path, "a").close()

def log(msg):
    ts = datetime.now().strftime('%H:%M:%S'); print(msg, flush=True)
    with open(log_path,'a') as f: f.write(f"[{ts}] {msg}\n")

idx = 0
while datetime.now() < end:
    area = areas[idx % len(areas)]
    log(f"Generating section for area [{idx+1}/{max(1,len(areas))}]: {area}")
    try:
        sys, usr = gen_prompt(area)
        section = chat(sys, usr, MAX_GEN)
        with open(paper_path,'a') as f: f.write("\n\n% === AREA: "+area+" ===\n\n"+section+"\n")
        log("Section appended.")
        # Periodic review every 2 sections
        if idx % 2 == 1:
            rev_sys, rev_usr = rev_prompt(open(paper_path).read())
            review = chat(rev_sys, rev_usr, MAX_REV)
            with open(review_path,'a') as f: f.write("\n\n## Review checkpoint\n\n"+review+"\n")
            log("Review appended.")
        # checkpoint
        state["checkpoints"].append({
            "time": datetime.now().isoformat(),
            "area": area,
            "paper_bytes": os.path.getsize(paper_path),
            "review_bytes": os.path.getsize(review_path)
        })
        json.dump(state, open(meta_path,'w'), indent=2)
    except Exception as e:
        log(f"Error: {e}")
    idx += 1
    time.sleep(SLEEP_S)

log("Experiment finished.")





































