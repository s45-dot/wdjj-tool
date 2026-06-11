#!/bin/bash
# Build the Vue 3 frontend and copy the output into the backend's static directory.
# Usage: ./scripts/build_frontend.sh
#
# After this, ``backend/app/main.py`` serves the built frontend at ``/``
# (with SPA fallback when it runs on port 8080 via ``backend/run.py``).

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "==> Building frontend..."
cd "$PROJECT_DIR/frontend"
npm run build

echo "==> Copying build output to backend static directory..."
BUILD_DIR="$PROJECT_DIR/backend/app/static/frontend_build"
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
cp -r dist/* "$BUILD_DIR/"

echo "==> Done. Frontend build copied to $BUILD_DIR"
echo "    Restart the backend server to serve the new build."
