# Desktop Packaging — Bubble Stretch Tool

## Tauri 桌面壳评估

### 决策
**暂不实施**。Rust 工具链未在当前环境安装。

### 推荐路径
继续以 Web 模式为主（`bubble-st` 一键启动），Tauri 作为未来增强项。

### Tauri 收益
- 独立窗口，不依赖浏览器标签页
- macOS/Windows 原生体验
- 可打包为 .app / .exe

### 系统依赖（需预装）
- Rust: `curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh`
- macOS: Xcode Command Line Tools
- Windows: WebView2 Runtime

### 未来启动步骤
```bash
cd desktop/tauri
npm create tauri-app@latest
# 配置前端指向 localhost:8080
npm run tauri build
```

## macOS 测试包

当前无 Tauri 壳，改用 Web 模式分发：

```bash
# 用户只需：
bash ~/Desktop/bubble-stretch.sh
# 浏览器访问 http://127.0.0.1:8080
```

## Windows 测试包

```bash
# 用户只需：
scripts\start_windows.bat
# 浏览器访问 http://127.0.0.1:8080
```
