#!/bin/bash

# Startup script for Wealthy Dashboard API

echo "🚀 Starting Wealthy Partner Dashboard..."

# Check if conda is available
if command -v conda &> /dev/null; then
    # Check if wealthy-dashboard environment exists
    if conda env list | grep -q "wealthy-dashboard"; then
        echo "🔧 Activating conda environment..."
        eval "$(conda shell.bash hook)"
        conda activate wealthy-dashboard
    else
        echo "❌ Conda environment 'wealthy-dashboard' not found"
        echo "   Please run: ./setup_conda.sh"
        exit 1
    fi
else
    # Fall back to venv if conda is not available
    echo "📦 Conda not found, using virtual environment..."
    if [ ! -d "venv" ]; then
        echo "📦 Creating virtual environment..."
        python3 -m venv venv
    fi
    
    echo "🔧 Activating virtual environment..."
    source venv/bin/activate
    
    echo "📥 Installing dependencies..."
    pip install -r requirements.txt
fi

# Check if PostgreSQL is running
echo "🔍 Checking PostgreSQL..."
if ! docker-compose ps | grep -q "wealthy_postgres.*Up"; then
    echo "🐘 Starting PostgreSQL..."
    docker-compose up -d
    echo "⏳ Waiting for PostgreSQL to be ready..."
    sleep 5
fi

# Check if data needs to be imported
echo "📊 Checking if data import is needed..."
python -c "from app.database import engine; from app.models import SIPRecord; from sqlalchemy import inspect; print('Data exists' if inspect(engine).has_table('sip_records') and engine.execute('SELECT COUNT(*) FROM sip_records').scalar() > 0 else 'No data')" 2>/dev/null || echo "No data"

echo ""
echo "✅ Setup complete!"
echo ""
echo "To import data, run:"
echo "  python scripts/import_data.py /path/to/your/data.json"
echo ""
echo "🌐 Starting FastAPI server..."
echo "   API: http://localhost:8111"
echo "   Docs: http://localhost:8111/docs"
echo ""

# Start the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8111
