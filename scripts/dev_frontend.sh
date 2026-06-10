#!/bin/bash
# Start the Vue 3 frontend dev server
# Usage: ./scripts/dev_frontend.sh

set -e

cd "$(dirname "$0")/../frontend"

echo "==> Installing frontend dependencies..."
npm install

echo "==> Starting Vite dev server..."
npm run dev
