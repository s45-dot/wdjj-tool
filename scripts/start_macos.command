#!/bin/bash
cd "$(dirname "$0")/.." || exit 1
python3 scripts/start_backend.py --no-browser
echo ""
echo "按任意键关闭窗口..."
read -n 1 -s