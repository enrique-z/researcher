#!/bin/bash

# Long-Duration AI Research Paper Generation Experiment
# experiment-native-1-spectro: SAI Active Spectroscopy Framework

echo "🌟 Starting Long-Duration AI Research Experiment"
echo "📊 experiment-native-1-spectro: SAI Active Spectroscopy Framework"
echo "⏱️  Expected Duration: 4-5 hours"
echo ""

# Navigate to project root and activate environment
cd /Users/apple/code/Researcher
source activate

# Navigate to experiment directory
cd EXPERIMENTS/experiment-native-1-spectro

# Set up environment variables for optimal performance
export CUDA_VISIBLE_DEVICES=0
export PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:512

# Create output directories if they don't exist
mkdir -p output logs checkpoints analysis

# Start the experiment
echo "🚀 Launching experiment runner..."
python experiment_runner.py 2>&1 | tee logs/experiment_console_$(date +%Y%m%d_%H%M%S).log

# Display completion status
if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 EXPERIMENT COMPLETED SUCCESSFULLY!"
    echo "📁 Check output/ directory for generated papers"
    echo "📋 Check logs/ directory for detailed logs"
    echo "💾 Check checkpoints/ directory for progress snapshots"
else
    echo ""
    echo "⚠️  EXPERIMENT ENCOUNTERED ERRORS"
    echo "📋 Check logs for details"
    echo "💾 Checkpoints preserved for analysis"
fi