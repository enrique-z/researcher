#!/bin/bash

# Pipeline 2 Development Dashboard Launcher
# Launches the Streamlit dashboard for the ultimate research pipeline

echo "🚀 Launching Pipeline 2 Development Dashboard..."
echo "📍 Dashboard URL will be: http://localhost:8501"
echo ""

# Navigate to dashboard directory
cd "$(dirname "$0")"

# Activate virtual environment if it exists
if [ -f "../../../.venv/bin/activate" ]; then
    echo "✅ Activating Researcher virtual environment..."
    source ../../../.venv/bin/activate
elif [ -f "../../.venv/bin/activate" ]; then
    echo "✅ Activating Researcher virtual environment..."
    source ../../.venv/bin/activate
else
    echo "⚠️ Virtual environment not found - using system Python"
fi

# Install requirements if needed
echo "📦 Checking Streamlit installation..."
if ! python -c "import streamlit" 2>/dev/null; then
    echo "📥 Installing Streamlit requirements..."
    pip install -r requirements.txt
else
    echo "✅ Streamlit already installed"
fi

echo ""
echo "🎮 Starting Pipeline 2 Dashboard..."
echo "📊 Real-time progress tracking for:"
echo "   • AI-S-Plus GLENS integration"
echo "   • Oxford+RAG knowledge enhancement"
echo "   • URSA quality control"
echo "   • Gemini manual review workflow"
echo ""
echo "🔗 Access dashboard at: http://localhost:8501"
echo "⏹️  Press Ctrl+C to stop"
echo ""

# Launch Streamlit dashboard
streamlit run dashboard.py --server.port 8501 --server.address localhost