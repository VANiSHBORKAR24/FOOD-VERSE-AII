#!/usr/bin/env bash
# Food-Verse AI - Setup and Launch Script

set -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd "$DIR"

echo "=========================================================="
echo "🥑 Launching Food-Verse AI (Google Cloud GenAI Project)..."
echo "=========================================================="

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating Python virtual environment (venv)..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Install requirements
echo "📥 Checking and installing required packages..."
pip install -q -r requirements.txt

# Launch Streamlit app
echo "🚀 Starting Streamlit Web App on http://localhost:8501 ..."
streamlit run app.py
