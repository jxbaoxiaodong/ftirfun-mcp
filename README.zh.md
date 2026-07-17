[English](README.md) | 中文 | [Español](README.es.md) | [Français](README.fr.md) | [日本語](README.ja.md)

# FTIR.fun MCP 服务器

[![smithery badge](https://smithery.ai/badge/hlin2097/ftirfun)](https://smithery.ai/servers/hlin2097/ftirfun)
[![MCP.so](https://img.shields.io/badge/MCP.so-listed-blue)](https://mcp.so/server/ftir-spectral-search/ftir_fun)
[![PyPI](https://img.shields.io/pypi/v/ftirfun-mcp)](https://pypi.org/project/ftirfun-mcp/)

**[FTIR.fun](https://ftir.fun)** 的 MCP 服务器与 REST API 客户端 —— 在线红外光谱库与材质识别平台。

---

## 什么是 FTIR.fun？

**[FTIR.fun](https://ftir.fun)** 是一个面向研究人员和工程师的云端红外光谱分析平台，已在 52 个以上国家使用。平台提供持续更新的 **13 万+ 红外标准谱图库**，涵盖高分子材料、添加剂、涂料、药用辅料及工业化学品等领域。

平台核心功能：

- **谱库检索** — 上传仪器文件或粘贴峰位，获得带相似度评分和文献 DOI 的排名匹配结果
- **AI 峰位解析** — 输入任意波数，获得基于化学知识图谱的官能团归属
- **三轴完整报告** — 自动多阶段材质鉴定，生成可共享的结果链接
- **图片转 CSV** — 从已发表图谱中数字化提取光谱曲线
- **配方工作台** — 多组分逆向分析与未知混合物鉴定

本包让你的 AI 助手（Claude、Cursor、VS Code Copilot、Gemini CLI 等）或代码流水线直接调用 FTIR.fun，无需切换浏览器。

**分步骤配置指南与在线 API 文档：** https://ftir.fun/ai-integration/

---

## 获取 API Key

1. 在 [ftir.fun](https://ftir.fun) 注册登录 —— 新账号含免费试用积分。
2. 进入 **账号 → API Keys**，点击 **生成**。
3. 立即复制密钥（以 `ftir_` 开头，仅显示一次）。

认证方式为单一请求头，无 OAuth、无浏览器跳转：

```
# MCP（托管端）
Authorization: Bearer ftir_your_key_here

# REST API
X-API-Key: ftir_your_key_here
```

---

## 托管 MCP（推荐）

直接连接生产端点，无需本地安装。托管端点提供全部七个 FTIR 工具。

### VS Code（GitHub Copilot Agent 模式）

在项目中创建 `.vscode/mcp.json`（或添加到用户级设置）：

```json
{
  "inputs": [
    {
      "type": "promptString",
      "id": "ftirfun-api-key",
      "description": "FTIR.fun API key",
      "password": true
    }
  ],
  "servers": {
    "ftirfun": {
      "type": "http",
      "url": "https://ftir.fun/mcp",
      "headers": {
        "Authorization": "Bearer ${input:ftirfun-api-key}"
      }
    }
  }
}
```

打开命令面板 → **MCP: List Servers** → 选择 `ftirfun` → **Start**。VS Code 会安全提示输入 API Key（直接粘贴原始密钥，不要加 `Bearer`）。

### Claude Desktop / Claude Code

**Claude Desktop**：设置 → 连接器 → 添加自定义连接器。

```
URL:    https://ftir.fun/mcp
Header: Authorization: Bearer ftir_your_key_here
```

**Claude Code** 一行命令：

```bash
claude mcp add --transport http ftirfun https://ftir.fun/mcp \
  --header "Authorization: Bearer ftir_your_key_here"
```

### Cursor

创建或编辑 `~/.cursor/mcp.json`（全局）或 `.cursor/mcp.json`（项目）：

```json
{
  "mcpServers": {
    "ftirfun": {
      "url": "https://ftir.fun/mcp",
      "headers": {
        "Authorization": "Bearer ftir_your_key_here"
      }
    }
  }
}
```

重载 Cursor 后在 **设置 → MCP** 确认绿色状态。

### OpenAI Codex

```toml
[mcp_servers.ftirfun]
url = "https://ftir.fun/mcp"
http_headers = { Authorization = "Bearer ftir_your_key_here" }
```

### Gemini CLI

编辑 `~/.gemini/settings.json`：

```json
{
  "mcpServers": {
    "ftirfun": {
      "httpUrl": "https://ftir.fun/mcp",
      "headers": {
        "Authorization": "Bearer ftir_your_key_here"
      }
    }
  }
}
```

运行 `/mcp` 确认 `ftirfun` 已连接。

### 其他 MCP 客户端

将 URL 设为 `https://ftir.fun/mcp`，发送 `Authorization: Bearer <your key>` 即可。完整工具 Schema 见 [server-card.json](https://ftir.fun/.well-known/mcp/server-card.json)。

### 测试提示词

```
使用 FTIR.fun 解释 1715 cm-1 的红外峰。
根据 FTIR 峰位 2915、1715、1450 cm-1 识别该聚合物。
在 FTIR.fun 谱库中搜索聚丙烯参考谱图。
```

---

## REST API

支持任意语言调用 —— Python、JavaScript、R、MATLAB、Go 等。适合 LIMS 集成、批量处理或为自有应用添加 FTIR 检索能力。

完整 API 参考：https://ftir.fun/api-docs/

### 健康检查（无需 Key）

```bash
curl https://ftir.fun/health
# → {"status":"ok","service":"ftirfun-api"}
```

### 通过峰位识别未知物质

```bash
curl -X POST https://ftir.fun/ftir/analyze_spectrum \
  -H "X-API-Key: ftir_your_key_here" \
  -H "Content-Type: application/json" \
  -d '{
    "peaks": [2915, 1715, 1450, 1260, 1090],
    "options": {"top_k": 10, "tolerance_cm1": 8}
  }'
```

```python
import requests

resp = requests.post(
    "https://ftir.fun/ftir/analyze_spectrum",
    headers={"X-API-Key": "ftir_your_key_here"},
    json={
        "peaks": [2915, 1715, 1450, 1260, 1090],
        "options": {"top_k": 10, "tolerance_cm1": 8},
    },
)
print(resp.json())
```

### 通过仪器文件识别

```python
import base64, requests

with open("sample.spa", "rb") as f:
    b64 = base64.b64encode(f.read()).decode()

resp = requests.post(
    "https://ftir.fun/ftir/analyze_spectrum",
    headers={"X-API-Key": "ftir_your_key_here"},
    json={"file_base64": b64, "filename": "sample.spa"},
)
print(resp.json())
```

支持 28+ 格式：Thermo `.spa`/`.spc`、Bruker `.opus`、PerkinElmer `.sp`、JCAMP-DX `.jdx`/`.dx`、CSV、Excel 等。

### 解析峰位

```bash
curl -X POST https://ftir.fun/ftir/explain_peaks \
  -H "X-API-Key: ftir_your_key_here" \
  -H "Content-Type: application/json" \
  -d '{"peaks": [1715, 2915], "sampling_mode": "ATR"}'
```

### 按名称或 CAS 查找参考谱图

```bash
curl "https://ftir.fun/v1/search?q=polypropylene&limit=5" \
  -H "X-API-Key: ftir_your_key_here"
```

---

## 工具列表

MCP 服务器提供七个工具：

| 工具名 | 说明 |
|--------|------|
| `parse_ftir_spectrum` | 解析 base64 编码的仪器文件，返回对齐后的曲线点和检测峰 |
| `analyze_ftir_spectrum` | 在谱库中检索未知光谱，返回排名匹配、相似度评分和文献证据 |
| `submit_ftir_report` | 提交文件至三轴完整工作流，返回 `task_id` 和 `result_num` |
| `get_ftir_report_status` | 轮询 `task_id` 状态；完成后返回 `report_view` 和 `report_url` |
| `explain_peaks` | 解释一个或多个峰位，无需完整检索 |
| `find_spectra` | 按物质名、CAS 号或关键词查找参考谱图 |
| `fetch_result` | 通过报告编号获取历史分析结果 |

---

## 自托管（本地代理）

提供轻量级本地 MCP 代理，转发至托管 API，暴露相同的七个工具。

```bash
export FTIRFUN_API_KEY="your-ftirfun-api-key"

python -m venv .venv && . .venv/bin/activate
pip install .
ftirfun-mcp
```

Docker：

```bash
docker build -t ftirfun-mcp .
docker run --rm -p 8001:8001 -e FTIRFUN_API_KEY="your-ftirfun-api-key" ftirfun-mcp
```

---

## 链接汇总

| 资源 | 地址 |
|------|------|
| 官网 | https://ftir.fun |
| 配置指南 | https://ftir.fun/ai-integration/ |
| API 文档 | https://ftir.fun/api-docs/ |
| MCP 端点 | https://ftir.fun/mcp |
| 服务器卡片 | https://ftir.fun/.well-known/mcp/server-card.json |
| Smithery | https://smithery.ai/servers/hlin2097/ftirfun |
| MCP.so | https://mcp.so/server/ftir-spectral-search/ftir_fun |
| PyPI | https://pypi.org/project/ftirfun-mcp/ |
