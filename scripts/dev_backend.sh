#!/bin/bash
# Start the FastAPI backend dev server
# Usage: ./scripts/dev_backend.sh

set -e

cd "$(dirname "$0")/../backend"

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

echo "==> Installing backend dependencies..."
pip install -r requirements.txt 2>/dev/null || true

echo "==> Starting Uvicorn dev server..."
uvicorn main:app --reload --host 0.0.0.0 --port 8000
