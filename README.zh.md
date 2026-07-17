[English](README.md) | 中文 | [Español](README.es.md) | [Français](README.fr.md) | [日本語](README.ja.md)

# FTIR.fun MCP 服务器

[![smithery badge](https://smithery.ai/badge/hlin2097/ftirfun)](https://smithery.ai/servers/hlin2097/ftirfun)
[![MCP.so](https://img.shields.io/badge/MCP.so-listed-blue)](https://mcp.so/server/ftir-spectral-search/ftir_fun)
[![PyPI](https://img.shields.io/pypi/v/ftirfun-mcp)](https://pypi.org/project/ftirfun-mcp/)

**[FTIR.fun](https://ftir.fun)** 的 MCP 服务器与 REST API 客户端 —— 让 AI 助手和代码流水线直接访问 13 万+ FTIR 红外标准谱图，用于材质识别、峰位解析和光谱检索。

## 工具一览

| 工具 | 功能 |
|------|------|
| [`analyze_ftir_spectrum`](#analyze_ftir_spectrum) | 识别未知 FTIR 光谱 —— 支持峰位列表、自然语言描述或仪器文件（28+ 格式）。返回排名匹配、相似度评分和文献 DOI。 |
| [`explain_peaks`](#explain_peaks) | 解释一个或多个红外峰位 —— 无需完整检索即可获得官能团归属。 |
| [`parse_ftir_spectrum`](#parse_ftir_spectrum) | 解析原始 FTIR 仪器文件，输出波数-强度数据点和检测峰位。 |
| [`find_spectra`](#find_spectra) | 在 13 万+ 参考谱库中按物质名、CAS 号或关键词搜索，返回曲线数据可直接比对。 |
| [`submit_ftir_report`](#submit_ftir_report) | 提交光谱到三轴完整识别工作流（与网站相同的多阶段分析）。 |
| [`get_ftir_report_status`](#get_ftir_report_status) | 轮询报告进度；完成后返回完整结构化结果和可共享 URL。 |
| [`fetch_result`](#fetch_result) | 通过报告编号获取任意历史 FTIR.fun 分析结果。 |

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

## MCP 工具

托管 MCP 端点 `https://ftir.fun/mcp` 提供七个工具。

---

### `analyze_ftir_spectrum`

在 FTIR 红外光谱库中检索一个未知光谱。支持峰位列表、自然语言描述或原始仪器文件。

**参数**

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `query` | string | 否 | 自然语言 FTIR 请求 —— 峰位如 "1730, 1600, 1250 cm-1" 会被自动提取。 |
| `peaks` | number[] | 否 | FTIR 峰位，单位 cm⁻¹（如 `[1736, 1379, 1241]`）。 |
| `file_base64` | string | 否 | Base64 编码的 FTIR 仪器文件。支持 28+ 格式：Thermo `.spa`/`.spc`、Bruker `.opus`、PerkinElmer `.sp`、JCAMP-DX `.jdx`/`.dx`、CSV、Excel 等。 |
| `filename` | string | 否 | 原始文件名，用于格式检测（如 `"sample.spa"`）。 |
| `top_k` | integer | 否 | 返回排名候选数量（1–50，默认 15）。 |
| `tolerance_cm1` | integer | 否 | 峰匹配容差，单位 cm⁻¹（1–30，默认 8）。 |

**返回：** 排名候选材料、相似度评分、逐峰证据（关联文献 DOI）、置信度和不确定性说明。

**示例**
```
识别这个红外光谱：峰位 2915、1715、1450、1260、1090 cm-1。
```

---

### `explain_peaks`

解释一个或多个 FTIR 红外峰位，无需完整光谱库检索。适合快速官能团归属和波数解读。

**参数**

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `query` | string | 否 | 自然语言峰位问题，如 `"1715 cm-1 在酯中代表什么？"` |
| `peaks` | number[] | 否 | 一个或多个 FTIR 峰位，单位 cm⁻¹。 |
| `sampling_mode` | string | 否 | `ATR`、`Thin Film`、`KBr Pellet`、`Nujol Mull` 等。 |

**返回：** 结构化峰位解释，含官能团归属和不确定性提示。

**示例**
```
使用 FTIR.fun 解释 ATR 模式下 1715 和 3300 cm-1 的红外峰。
```

---

### `parse_ftir_spectrum`

解析 base64 编码的 FTIR 仪器文件，输出对齐后的波数-强度曲线点和自动检测的峰位。用于在分析之前提取原始光谱数据。

**参数**

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `file_base64` | string | 是 | Base64 编码的 FTIR 仪器文件。 |
| `filename` | string | 是 | 原始文件名（如 `"sample.spa"`），用于格式检测。 |

**返回：** 对齐后的 `(wavenumber, intensity)` 数据点和检测到的峰位列表（cm⁻¹）。

---

### `find_spectra`

按物质名、CAS 号、谱图编号或关键词查找 FTIR 参考谱图。返回原始光谱曲线数据，可直接比对。

**参数**

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `query` | string | 是 | 物质名（如 `"polypropylene"`）、CAS 号、谱库 `NUM` 或关键词。 |
| `limit` | integer | 否 | 返回结果数（1–20，默认 10）。 |

**返回：** 匹配的参考谱图，含编号、名称、CAS、峰标记和曲线数据。

**示例**
```
在 FTIR.fun 谱库中搜索 PET（聚对苯二甲酸乙二醇酯）参考谱图。
```

---

### `submit_ftir_report`

将 base64 编码的 FTIR 光谱文件提交到 FTIR.fun 三轴完整识别工作流 —— 与网站使用相同的多阶段分析。立即返回 `task_id` 和 `result_num`；用 `get_ftir_report_status` 轮询完成结果。

**参数**

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `file_base64` | string | 是 | Base64 编码的 FTIR 仪器文件。 |
| `filename` | string | 是 | 原始文件名，用于格式检测。 |

**返回：** `{ task_id, result_num }`

---

### `get_ftir_report_status`

轮询通过 `submit_ftir_report` 提交的报告状态。完成后返回完整的结构化 `report_view`（与 FTIR.fun 网站显示相同）和可共享的 `report_url`。

**参数**

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `task_id` | string | 是 | `submit_ftir_report` 返回的 `task_id`。 |

**返回：** 状态字段，完成时附带 `report_view` 和 `report_url`。

---

### `fetch_result`

通过报告编号获取 FTIR.fun 的历史红外分析结果。

**参数**

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `result_num` | string | 是 | FTIR.fun 报告/结果编号。 |
| `language_code` | string | 否 | 结果展示语言（默认 `en`）。 |

**返回：** 结构化结果上下文，含 `report_url`、`headline`、`summary`、`report_view` 和 `result_context`。

---

## REST API

支持任意语言调用 —— Python、JavaScript、R、MATLAB、Go。适合 LIMS 集成、批量光谱处理或为自有应用添加 FTIR 红外光谱检索能力。

完整 API 参考：https://ftir.fun/api-docs/

### 健康检查（无需 Key）

```bash
curl https://ftir.fun/health
# → {"status":"ok","service":"ftirfun-api"}
```

### 通过峰位识别未知红外光谱

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

### 解析红外峰位

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

## MCP 客户端配置

托管 MCP 端点无需本地安装。URL 为 `https://ftir.fun/mcp`，使用 `Bearer` Token。

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

打开命令面板 → **MCP: List Servers** → 选择 `ftirfun` → **Start**。

### Claude Desktop / Claude Code

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

创建或编辑 `~/.cursor/mcp.json`：

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

其他 MCP 客户端：只要支持远程 streamable-HTTP 服务器，设 URL 为 `https://ftir.fun/mcp`，发送 `Authorization: Bearer <your key>` 即可。完整 Schema 见 [server-card.json](https://ftir.fun/.well-known/mcp/server-card.json)。

---

## 自托管（本地代理）

轻量级本地 MCP 代理，转发至托管 API，暴露相同的七个 FTIR 工具。

```bash
export FTIRFUN_API_KEY="your-ftirfun-api-key"

python -m venv .venv && . .venv/bin/activate
pip install .
ftirfun-mcp
```

Streamable HTTP 模式：

```bash
ftirfun-mcp --transport streamable-http --host 127.0.0.1 --port 8001
```

Docker：

```bash
docker build -t ftirfun-mcp .
docker run --rm -p 8001:8001 -e FTIRFUN_API_KEY="your-ftirfun-api-key" ftirfun-mcp
```

---

## 工具边界

本 MCP 服务器仅用于 FTIR 光谱库筛查。不适用于非 FTIR 光谱、通用化学问答或认证实验室报告。

---

## 关于 FTIR.fun

**[FTIR.fun](https://ftir.fun)** 是面向研究人员和工程师的云端红外光谱分析平台，已在 52 个以上国家使用。平台提供持续更新的 **13 万+ 红外标准谱图库**，涵盖高分子材料、添加剂、涂料、药用辅料及工业化学品等领域。

平台核心功能：

- **谱库检索** — 上传仪器文件或粘贴峰位，获得带相似度评分和文献 DOI 的排名匹配
- **AI 峰位解析** — 输入任意波数，获得基于化学知识图谱的官能团归属
- **三轴完整报告** — 自动多阶段材质鉴定，生成可共享的结果链接
- **图片转 CSV** — 从论文图谱中数字化提取光谱曲线
- **配方工作台** — 多组分逆向分析与未知混合物鉴定

分步骤配置指南：https://ftir.fun/ai-integration/

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
