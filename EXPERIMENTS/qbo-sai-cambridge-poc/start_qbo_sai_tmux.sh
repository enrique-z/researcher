#!/usr/bin/env bash
set -euo pipefail

# QBO SAI Cambridge Proof of Concept - tmux launcher
# Based on successful experiment-native-1-spectro approach

# Paths
ROOT="/Users/apple/code/Researcher"
EXP_DIR="$ROOT/EXPERIMENTS/qbo-sai-cambridge-poc"
VENV="$ROOT/.venv/bin/activate"
LOG_DIR="$EXP_DIR/logs"
OUT_DIR="$EXP_DIR/output"

# Ensure dirs and files exist
mkdir -p "$LOG_DIR" "$OUT_DIR"
touch "$OUT_DIR/qbo_sai_cambridge_paper.tex" "$OUT_DIR/qbo_sai_cambridge_review.md" "$OUT_DIR/qbo_sai_cambridge_meta.json"

# tmux session name
SESSION="qbo_sai_gpt5_run"

# Kill existing session if any
if tmux has-session -t "$SESSION" 2>/dev/null; then
  tmux kill-session -t "$SESSION"
fi

# Base command to run QBO SAI paper generation (4 hours, same as successful experiment)
RUN_CMD="source $VENV && cd $EXP_DIR && OPENAI_MODEL=gpt-5 OPENAI_REASONING_EFFORT=high OPENAI_MAX_TOKENS=32000 OPENAI_REVIEW_TOKENS=4000 OPENAI_EXPERIMENT_HOURS=4 python openai_qbo_sai_experiment.py"

# Start tmux session detached
tmux new-session -d -s "$SESSION" "bash -lc '$RUN_CMD'"

# Pane 1: live logs (most recent)
tmux split-window -t "$SESSION":0 -v "bash -lc 'cd $EXP_DIR && sleep 2 && tail -F \$(ls -1t logs/qbo_sai_generation_* 2>/dev/null | head -1 || echo /dev/null)'"

# Pane 2: paper growth
tmux split-window -t "$SESSION":0 -h "bash -lc 'cd $EXP_DIR && tail -n +1 -f output/qbo_sai_cambridge_paper.tex'"

# Pane 3: review checkpoints
tmux split-window -t "$SESSION":0 -v "bash -lc 'cd $EXP_DIR && tail -n +1 -f output/qbo_sai_cambridge_review.md'"

# Pane 4: meta/checkpoints + sizes
tmux split-window -t "$SESSION":0 -h "bash -lc 'cd $EXP_DIR && while true; do date; echo \"=== QBO SAI Cambridge Progress ===\"; ls -lh output logs | sed 1,1d; echo; echo \"=== Current Status ===\"; tail -n 10 output/qbo_sai_cambridge_meta.json; sleep 3; done'"

# Tile layout
tmux select-layout -t "$SESSION":0 tiled

# Focus first pane and attach
tmux select-pane -t "$SESSION":0.0

echo "🚀 QBO SAI Cambridge Proof of Concept Started!"
echo "📊 Session: $SESSION"
echo "⏰ Duration: 4 hours"
echo "💰 Cost: ~$5 USD (same as successful experiment)"
echo "📄 Target: 128+ page comprehensive paper"
echo "🎯 Attaching to tmux session..."

exec tmux attach -t "$SESSION"