# Bubble Stretch Tool 启动问题排查

## Python 不存在

**症状**: 终端提示 `python3: command not found` 或 `python: command not found`

**解决方案**:
- macOS: 安装 [Python 官网下载](https://www.python.org/downloads/) 或使用 Homebrew: `brew install python`
- Windows: 从 [python.org](https://www.python.org/downloads/) 下载安装包，**记得勾选 "Add Python to PATH"**

---

## Node.js 不存在

**症状**: 前端无法启动，提示 `node: command not found`

**解决方案**:
- macOS: `brew install node`
- Windows: 从 [nodejs.org](https://nodejs.org/) 下载 LTS 版本

---

## 后端依赖缺失

**症状**: `ModuleNotFoundError` 或 `ImportError`

**解决方案**:
```bash
cd backend
pip install -r requirements.txt
```

---

## 前端依赖缺失

**症状**: `npm install` 失败或 `node_modules` 不存在

**解决方案**:
```bash
cd frontend
npm install
```

---

## 端口 8080 被占用

**症状**: `Address already in use` 或 `Port 8080 is already in use`

**解决方案**:

**macOS/Linux:**
```bash
# 查找占用端口的进程
lsof -i :8080
# 终止进程 (替换 PID 为实际进程号)
kill -9 <PID>
```

**Windows:**
```cmd
netstat -ano | findstr :8080
taskkill /PID <PID> /F
```

或修改 `backend/.env` 中的 `PORT` 为其他端口。

---

## 浏览器未自动打开

**症状**: 后端启动成功但浏览器没有反应

**解决方案**:
1. 手动打开浏览器访问: http://localhost:8080
2. 检查启动脚本是否使用了 `--no-browser` 参数
3. 确保没有防火墙阻止本地连接

---

## 手机无法访问电脑服务

**症状**: 手机浏览器无法打开电脑 IP

**解决方案**:

### 1. 确认电脑 IP 地址
```bash
# macOS/Linux
ifconfig | grep "inet " | grep -v 127.0.0.1

# Windows
ipconfig
```

### 2. 确保后端监听所有网络接口
修改 `backend/.env`:
```
HOST=0.0.0.0
```

### 3. 防火墙设置

**macOS:**
```bash
# 允许 Python 通过防火墙
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --add $(which python3)
```

**Windows:**
- 控制面板 → Windows Defender 防火墙 → 允许应用通过防火墙
- 找到 Python 并允许私有和公共网络

### 4. 检查手机和电脑是否在同一网络
- 确保连接同一个 Wi-Fi
- 检查是否使用了来宾网络或隔离网络

---

## macOS 脚本无法双击

**症状**: 双击 `.command` 文件没有反应

**解决方案**:

1. **添加执行权限**:
   ```bash
   chmod +x scripts/start_macos.command
   ```

2. **检查文件扩展名**:
   确保文件是 `.command` 而不是 `.command.txt`

3. **在终端中测试**:
   ```bash
   open scripts/start_macos.command
   ```

4. **检查终端权限**:
   - 系统偏好设置 → 安全性与隐私 → 隐私 → 终端 → 允许

---

## Windows bat 无法启动

**症状**: 双击 `.bat` 文件闪退或报错

**解决方案**:

1. **以管理员身份运行**:
   右键 → "以管理员身份运行"

2. **在 CMD 中手动运行**:
   打开命令提示符，输入:
   ```cmd
   cd [项目路径]
   scripts\start_windows.bat
   ```

3. **检查 Python 路径**:
   确保 Python 已添加到系统 PATH
   ```cmd
   python --version
   ```

4. **修改执行策略** (如果被阻止):
   ```cmd
   powershell Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```