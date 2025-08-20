#!/usr/bin/env bash
set -euo pipefail

# Paths
ROOT="/Users/apple/code/Researcher"
EXP_DIR="$ROOT/EXPERIMENTS/experiment-native-1-spectro"
VENV="$ROOT/.venv/bin/activate"
LOG_DIR="$EXP_DIR/logs"
OUT_DIR="$EXP_DIR/output"

# Ensure dirs and files exist
mkdir -p "$LOG_DIR" "$OUT_DIR"
touch "$OUT_DIR/paper_gpt5_integrated.tex" "$OUT_DIR/paper_gpt5_integrated_review.md" "$OUT_DIR/paper_gpt5_integrated_meta.json"

# tmux session name
SESSION="gpt5_long_run"

# Kill existing session if any
if tmux has-session -t "$SESSION" 2>/dev/null; then
  tmux kill-session -t "$SESSION"
fi

# Base command to run orchestrator (4 hours)
RUN_CMD="source $VENV && cd $EXP_DIR && OPENAI_MODEL=gpt-5 OPENAI_REASONING_EFFORT=high OPENAI_MAX_TOKENS=12000 OPENAI_REVIEW_TOKENS=4000 OPENAI_EXPERIMENT_HOURS=4 python openai_long_experiment.py"

# Start tmux session detached
tmux new-session -d -s "$SESSION" "bash -lc '$RUN_CMD'"

# Pane 1: live logs (most recent)
tmux split-window -t "$SESSION":0 -v "bash -lc 'cd $EXP_DIR && sleep 2 && tail -F \$(ls -1t logs/openai_long_* 2>/dev/null | head -1 || echo /dev/null)'"

# Pane 2: paper growth
tmux split-window -t "$SESSION":0 -h "bash -lc 'cd $EXP_DIR && tail -n +1 -f output/paper_gpt5_integrated.tex'"

# Pane 3: review checkpoints
tmux split-window -t "$SESSION":0 -v "bash -lc 'cd $EXP_DIR && tail -n +1 -f output/paper_gpt5_integrated_review.md'"

# Pane 4: meta/checkpoints + sizes
tmux split-window -t "$SESSION":0 -h "bash -lc 'cd $EXP_DIR && while true; do date; ls -lh output logs | sed 1,1d; echo; tail -n 10 output/paper_gpt5_integrated_meta.json; sleep 2; done'"

# Tile layout
tmux select-layout -t "$SESSION":0 tiled

# Focus first pane and attach
tmux select-pane -t "$SESSION":0.0

echo "Attached to tmux session: $SESSION"
exec tmux attach -t "$SESSION"





































