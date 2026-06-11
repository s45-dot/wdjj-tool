#!/bin/bash
# Bubble Stretch Tool — 桌面化验收脚本
set -e
echo "=== Bubble Stretch Tool 桌面化验收 ==="
cd "$(dirname "$0")/.."

echo ""
echo "1. 后端环境检查..."
python3 scripts/check_backend_env.py && echo "   PASS" || echo "   FAIL"

echo ""
echo "2. 端口检测..."
python3 scripts/check_port.py && echo "   PASS" || echo "   FAIL"

echo ""
echo "3. 启动脚本存在性..."
for f in scripts/start_backend.py scripts/start_macos.command scripts/start_windows.bat; do
    [ -f "$f" ] && echo "   $f: OK" || echo "   $f: MISSING"
done

echo ""
echo "4. 文档完整性..."
for f in docs/LOCAL_START_GUIDE.md docs/TROUBLESHOOTING_STARTUP.md docs/DESKTOP_PACKAGING.md; do
    [ -f "$f" ] && echo "   $f: OK" || echo "   $f: MISSING"
done

echo ""
echo "5. 前端构建..."
if [ -f backend/app/static/frontend_build/index.html ]; then
    echo "   静态前端: OK"
else
    echo "   静态前端: NOT BUILT (运行 scripts/build_frontend.sh)"
fi

echo ""
echo "=== 验收完成 ==="
