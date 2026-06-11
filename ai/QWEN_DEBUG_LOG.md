# Qwen Code 调试记录

> 2026-06-11 | 存档，供新会话排查使用

## 当前状态

Qwen Code v0.17.1 → Carnice-Qwen3.6-MoE-35B-A3B-APEX-MTP-I-Balanced.gguf @ 192.168.1.121:11434

### 已知问题
1. **推理模式阻塞**：服务端未加 `--reasoning off`，流式输出首块 content:null
2. **SSH 不可用**：密钥失效（`Permission denied (publickey,password)`）
3. **项目扫描过重**：Qwen Code 无差别读取全部 markdown 文件

### 绕行方案
- 本地代理 `~/.hermes/scripts/14x-proxy.py`（127.0.0.1:11435 → 192.168.1.121:11434）
- 强制非流式 + SSE 包装，已多线程化
- `~/.qwen/settings.json` 已指向代理

### 需要的操作（在 14x 终端）
```bash
echo 'ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIJlcFEI2qSJK7M0vCtoBj0knfBddtLy/eBOb05jyIIBr hermes-agent' >> ~/.ssh/authorized_keys
pkill llama-server && llama-server -m ~/models/Carnice-Qwen3.6-MoE-35B-A3B-APEX-MTP-I-Balanced.gguf --host 0.0.0.0 --port 11434 -ngl 99 -c 65536 --reasoning off &
```

### 相关文件
- 代理：`~/.hermes/scripts/14x-proxy.py`
- 配置：`~/.qwen/settings.json`
- 详细报告：`~/Desktop/qwen-code-故障排查报告.md`
- Skill：`14x-llamacpp-server`
