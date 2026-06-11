# Bubble Stretch Tool — 本地启动指南

## 环境要求

- Python >= 3.9
- Node.js >= 18
- npm（随 Node.js 安装）

## 开发模式启动

```bash
# 终端1：后端
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --host 0.0.0.0 --port 8080

# 终端2：前端
cd frontend
npm install
npm run dev
```

访问 http://localhost:5173

## 生产模式启动（后端托管前端）

```bash
# 1. 构建前端
cd frontend && npm run build

# 2. 复制到后端静态目录
cp -r dist/* ../backend/app/static/frontend_build/

# 3. 启动后端
cd ../backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8080
```

访问 http://127.0.0.1:8080

## 一键启动

```bash
bash ~/Desktop/bubble-stretch.sh
# 或：bubble-st（需 source ~/.zshrc）
```

## 启动流程

```
1. 检查 Python 可用性
2. 检查后端依赖（fastapi/uvicorn/pillow）
3. 检查 Node.js 可用性
4. 检查端口 8080 是否空闲
5. 启动 FastAPI 后端
6. 启动 Vite 前端开发服务器
7. 获取局域网地址（手机可访问）
8. 自动打开浏览器
```

## 常见问题

| 问题 | 解决 |
|------|------|
| Python 未安装 | 安装 Python 3.9+ |
| Node.js 未安装 | 安装 Node.js 18+ |
| 端口 8080 被占用 | `lsof -i :8080` 查看占用进程 |
| 依赖缺失 | `pip install -r backend/requirements.txt` |
| 前端 node_modules 缺失 | `cd frontend && npm install` |
| 手机无法访问 | 确保手机和电脑在同一 Wi-Fi |
