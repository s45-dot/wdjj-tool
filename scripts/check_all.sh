#!/bin/bash
# Health checks for the Bubble Stretch Tool
# Verifies that backend and frontend are running
# Usage: ./scripts/check_all.sh

set -e

echo "========================================"
echo " Bubble Stretch Tool — Health Check"
echo "========================================"

# Backend health check
echo ""
echo "==> Checking backend (http://localhost:8000/api/health)..."
if command -v curl &> /dev/null; then
    RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/api/health 2>/dev/null || echo "000")
    if [ "$RESPONSE" = "200" ]; then
        echo "    Backend: OK (HTTP $RESPONSE)"
    else
        echo "    Backend: NOT RUNNING (HTTP $RESPONSE)"
    fi
else
    echo "    Skipped (curl not installed)"
fi

# Frontend health check
echo ""
echo "==> Checking frontend (http://localhost:5173)..."
if command -v curl &> /dev/null; then
    RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:5173 2>/dev/null || echo "000")
    if [ "$RESPONSE" != "000" ]; then
        echo "    Frontend: Responding (HTTP $RESPONSE)"
    else
        echo "    Frontend: NOT RUNNING"
    fi
else
    echo "    Skipped (curl not installed)"
fi

echo ""
echo "========================================"
echo " Check complete."
echo "========================================"
