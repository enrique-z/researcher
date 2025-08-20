#!/bin/bash
# Quick Start Script for QBO Phase-Locked SAI Experiment
# Complete pipeline execution with all components

echo "🚀 QBO Phase-Locked SAI Experiment - Quick Start"
echo "=============================================="

# Check if we're in the right directory
if [ ! -f "execute_qbo_sai_experiment.py" ]; then
    echo "❌ Error: Must run from /Users/apple/code/Researcher directory"
    echo "   Please cd to the correct directory and run: ./quick_start_qbo_sai.sh"
    exit 1
fi

# Activate research environment
echo "📦 Activating research environment..."
if [ -f "activate" ]; then
    source activate
    echo "✅ Environment activated"
else
    echo "⚠️ Warning: activate script not found, using current environment"
fi

# Check Python dependencies
echo "🔍 Checking dependencies..."
python -c "import json, numpy, pathlib; print('✅ Core dependencies available')" || {
    echo "❌ Missing core dependencies. Installing..."
    pip install numpy pathlib
}

# Check if ai-s-plus experiment file exists
QBO_SAI_FILE="/Users/apple/code/ai-s-plus/AI-Scientist-v2/core/ai_scientist/ideas/selected_for_execution copy.json"
if [ ! -f "$QBO_SAI_FILE" ]; then
    echo "❌ Error: QBO SAI experiment file not found at:"
    echo "   $QBO_SAI_FILE"
    echo "   Please ensure ai-s-plus is available at the expected location"
    exit 1
else
    echo "✅ QBO SAI experiment file found"
fi

# Create output directory with timestamp
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
OUTPUT_DIR="QBO_SAI_Experiment_$TIMESTAMP"
echo "📁 Output directory: $OUTPUT_DIR"

echo ""
echo "🎯 Choose execution mode:"
echo "1) Complete Pipeline (Phases 1-5, ~4-6 hours)"
echo "2) Quick Test (Validation only, ~5 minutes)"
echo "3) Oxford Search Only (~15 minutes)"  
echo "4) Phase by Phase (Interactive)"
echo "5) Exit"
echo ""
read -p "Enter choice (1-5): " CHOICE

case $CHOICE in
    1)
        echo "🚀 Starting Complete QBO SAI Pipeline..."
        echo "⏱️ Estimated time: 4-6 hours"
        echo "📋 This will execute:"
        echo "   Phase 1: Preparation (30 min)"
        echo "   Phase 2: Oxford Enhancement (45 min)"  
        echo "   Phase 3: URSA Execution (2-3 hours)"
        echo "   Phase 4: Validation (1 hour)"
        echo "   Phase 5: Paper Generation (1 hour)"
        echo ""
        read -p "Continue? (y/N): " CONFIRM
        if [[ $CONFIRM =~ ^[Yy]$ ]]; then
            python execute_qbo_sai_experiment.py --phase all --output-dir "$OUTPUT_DIR"
        else
            echo "❌ Cancelled by user"
            exit 0
        fi
        ;;
    2)
        echo "⚡ Running Quick Test (Validation Only)..."
        python execute_qbo_sai_experiment.py --validate-only --output-dir "$OUTPUT_DIR"
        ;;
    3)
        echo "📚 Running Oxford Knowledge Search..."
        python execute_qbo_sai_experiment.py --oxford-search --output-dir "$OUTPUT_DIR"
        ;;
    4)
        echo "🎯 Phase by Phase Execution"
        echo "Available phases:"
        echo "1 - Preparation (30 min)"
        echo "2 - Oxford Enhancement (45 min)"
        echo "3 - URSA Execution (2-3 hours)"
        echo "4 - Validation (1 hour)"
        echo "5 - Paper Generation (1 hour)"
        echo ""
        read -p "Enter phase number (1-5): " PHASE
        if [[ $PHASE =~ ^[1-5]$ ]]; then
            python execute_qbo_sai_experiment.py --phase "$PHASE" --output-dir "$OUTPUT_DIR"
        else
            echo "❌ Invalid phase number"
            exit 1
        fi
        ;;
    5)
        echo "👋 Goodbye!"
        exit 0
        ;;
    *)
        echo "❌ Invalid choice"
        exit 1
        ;;
esac

# Check execution results
if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 Execution completed successfully!"
    echo "📁 Results available in: $OUTPUT_DIR"
    echo ""
    echo "📋 Key deliverables:"
    echo "   📄 Main Paper: QBO_Phase_Locked_SAI_Complete_Paper.tex"
    echo "   📚 Bibliography: qbo_sai_complete_bibliography.bib"
    echo "   🔬 URSA Results: ursa_execution_results.json"
    echo "   ✅ Validation: validation_results.json"
    echo "   📖 Oxford Knowledge: oxford_search_results.json"
    echo "   📊 Final Report: QBO_SAI_Final_Report.json"
    echo ""
    echo "🔍 View results:"
    echo "   cd $OUTPUT_DIR"
    echo "   ls -la"
    echo ""
    echo "📖 Read summary:"
    echo "   cat $OUTPUT_DIR/QBO_SAI_Final_Summary.md"
else
    echo "❌ Execution failed. Check logs for details."
    exit 1
fi