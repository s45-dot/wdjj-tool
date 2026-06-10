# 气泡图片九宫格拉伸工具 (Bubble Stretch Tool)

## 项目目标

Bubble Stretch Tool 是一个气泡图片九宫格拉伸工具，用于将图片智能分割为九宫格（3x3 网格），并对每个网格应用拉伸算法，实现气泡效果的视觉变换。

## Phase 1 目标

Phase 1 旨在验证核心算法：
- 图片分割为九宫格
- 基础拉伸算法实现
- 前后端 API 通信验证
- 基本视觉测试

## 项目结构

```
.
├── frontend/       # Vue 3 + TypeScript + Vite 前端
├── backend/        # FastAPI + Pillow 后端
├── scripts/        # 开发脚本
├── docs/           # 文档
└── tests/          # 测试文件
```

## 快速开始

1. 安装依赖
2. 启动前端开发服务器
3. 启动后端 API 服务
4. 运行视觉测试

## 技术栈

- **前端**: Vue 3, TypeScript, Vite, Canvas API
- **后端**: FastAPI, Uvicorn, Pillow
- **图像处理**: Pillow, Canvas
- **AI 编排**: Hermes + QwenCode + Gemini + CodeWhale

## 许可证

MIT
