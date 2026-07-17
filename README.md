[中文](README.zh.md) | English | [Español](README.es.md) | [Français](README.fr.md) | [日本語](README.ja.md)

# FTIR.fun MCP Server

[![smithery badge](https://smithery.ai/badge/hlin2097/ftirfun)](https://smithery.ai/servers/hlin2097/ftirfun)
[![MCP.so](https://img.shields.io/badge/MCP.so-listed-blue)](https://mcp.so/server/ftir-spectral-search/ftir_fun)
[![PyPI](https://img.shields.io/pypi/v/ftirfun-mcp)](https://pypi.org/project/ftirfun-mcp/)

MCP server and REST API client for **[FTIR.fun](https://ftir.fun)** — the online infrared spectral library and material-identification platform.

---

## What is FTIR.fun?

**[FTIR.fun](https://ftir.fun)** is a cloud platform for infrared spectroscopy analysis used by researchers and engineers in 52+ countries. It gives fast access to a continuously updated library of **130,000+ FTIR reference spectra** covering polymers, additives, coatings, pharmaceuticals, and industrial chemicals.

What you can do on [ftir.fun](https://ftir.fun):

- **Spectral library search** — upload an instrument file or paste peak positions; get ranked matches with similarity scores and literature DOI citations
- **AI peak explanation** — ask about any wavenumber; receive functional-group assignments backed by a chemical knowledge graph
- **Full tri-axis report** — automatic multi-stage material identification with a shareable result URL
- **Image-to-CSV extraction** — digitize a spectrum curve from a published figure
- **Formulation workbench** — multi-component deformulation and unknown-mixture analysis

This package lets your AI assistant (Claude, Cursor, VS Code Copilot, Gemini CLI…) or your own code call FTIR.fun directly, without switching to the browser.

**Step-by-step setup guides and live API docs:** https://ftir.fun/ai-integration/

---

## Get an API Key

1. Sign in at [ftir.fun](https://ftir.fun) — new accounts include free trial credits.
2. Go to **Account → API Keys** and click **Generate**.
3. Copy the key immediately (starts with `ftir_`; shown only once).

Authentication uses a single header — no OAuth, no browser redirect:

```
# For MCP (hosted)
Authorization: Bearer ftir_your_key_here

# For REST API
X-API-Key: ftir_your_key_here
```

---

## Hosted MCP (Recommended)

Connect directly to the production endpoint — no local install required. The hosted endpoint exposes all seven FTIR tools and is the canonical production service.

### VS Code (GitHub Copilot Agent mode)

Create `.vscode/mcp.json` in your project (or add to user-level settings):

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

Open Command Palette → **MCP: List Servers** → select `ftirfun` → **Start**. VS Code will prompt for your API key securely (paste the raw key, not `Bearer ...`).

### Claude Desktop / Claude Code

In **Claude Desktop**: Settings → Connectors → Add custom connector.

```
URL:    https://ftir.fun/mcp
Header: Authorization: Bearer ftir_your_key_here
```

One-line setup for **Claude Code**:

```bash
claude mcp add --transport http ftirfun https://ftir.fun/mcp \
  --header "Authorization: Bearer ftir_your_key_here"
```

### Cursor

Create or edit `~/.cursor/mcp.json` (global) or `.cursor/mcp.json` (project):

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

Reload Cursor and check **Settings → MCP** for the green status indicator.

### OpenAI Codex

```toml
[mcp_servers.ftirfun]
url = "https://ftir.fun/mcp"
http_headers = { Authorization = "Bearer ftir_your_key_here" }
```

### Gemini CLI

Edit `~/.gemini/settings.json`:

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

Run `/mcp` to confirm `ftirfun` is connected.

### Any other MCP client

Set the URL to `https://ftir.fun/mcp` and send `Authorization: Bearer <your key>`. The server uses streamable HTTP; see the public server card for the full tool schema: [server-card.json](https://ftir.fun/.well-known/mcp/server-card.json).

### Test prompts to try

```
Use FTIR.fun to explain the FTIR peak at 1715 cm-1.
Identify this polymer from its FTIR peaks: 2915, 1715, 1450 cm-1.
Search the FTIR.fun library for polypropylene reference spectra.
```

---

## REST API

Call FTIR.fun from any language — Python, JavaScript, R, MATLAB, Go. Ideal for LIMS integrations, batch pipelines, or adding FTIR search to your own app.

Full API reference: https://ftir.fun/api-docs/

### Health check (no key required)

```bash
curl https://ftir.fun/health
# → {"status":"ok","service":"ftirfun-api"}
```

### Identify an unknown spectrum — peaks

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

### Identify from an instrument file

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

Supports 28+ formats: Thermo `.spa`/`.spc`, Bruker `.opus`, PerkinElmer `.sp`, JCAMP-DX `.jdx`/`.dx`, CSV, Excel, and more.

### Explain peaks

```bash
curl -X POST https://ftir.fun/ftir/explain_peaks \
  -H "X-API-Key: ftir_your_key_here" \
  -H "Content-Type: application/json" \
  -d '{"peaks": [1715, 2915], "sampling_mode": "ATR"}'
```

### Find reference spectra by name or CAS

```bash
curl "https://ftir.fun/v1/search?q=polypropylene&limit=5" \
  -H "X-API-Key: ftir_your_key_here"
```

---

## Tools

The MCP server exposes seven tools:

### `parse_ftir_spectrum`

Parse a base64-encoded FTIR instrument file into aligned curve points and detected peaks.

### `analyze_ftir_spectrum`

Search the FTIR.fun spectral library for one unknown FTIR spectrum.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `query` | string | No | Natural-language FTIR request — peak positions are extracted automatically. |
| `peaks` | number[] | No | FTIR peak positions in cm⁻¹ (e.g. `[1736, 1379, 1241]`). |
| `file_base64` | string | No | Base64-encoded FTIR instrument file (28+ formats supported). |
| `filename` | string | No | Original filename for format detection (e.g. `"sample.spa"`). |
| `top_k` | integer | No | Number of ranked candidates to return (1–50, default 15). |
| `tolerance_cm1` | integer | No | Peak matching tolerance in cm⁻¹ (1–30, default 8). |

**Returns:** Ranked candidate materials with similarity scores, peak-by-peak evidence linked to literature DOI, and confidence levels.

### `submit_ftir_report`

Submit a spectrum file to the full FTIR.fun tri-axis workflow. Returns `task_id` and `result_num`.

### `get_ftir_report_status`

Poll `task_id` from `submit_ftir_report`. When complete, returns `report_view` and `report_url`.

### `explain_peaks`

Explain one or more FTIR peaks without a full library search.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `query` | string | No | Natural-language peak question, e.g. `"What does 1715 cm-1 indicate?"` |
| `peaks` | number[] | No | One or more peak positions in cm⁻¹. |
| `sampling_mode` | string | No | `ATR`, `Thin Film`, `KBr Pellet`, etc. |

### `find_spectra`

Find library reference spectra by substance name, CAS number, or keywords.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `query` | string | Yes | Substance name, CAS, spectrum `NUM`, or keywords. |
| `limit` | integer | No | Number of results to return (1–20, default 10). |

### `fetch_result`

Fetch a historical FTIR.fun result by report number.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `result_num` | string | Yes | FTIR.fun report number. |
| `language_code` | string | No | Display language (default `en`). |

---

## Self-Hosted (Local Wrapper)

A lightweight local MCP wrapper that proxies to the hosted API. Exposes the same seven tools.

### Configuration

```bash
export FTIRFUN_API_KEY="your-ftirfun-api-key"
# Optional:
export FTIRFUN_API_BASE_URL="https://ftir.fun"
export FTIRFUN_API_TIMEOUT_SECONDS="120"
```

### Run Locally (stdio)

```bash
python -m venv .venv
. .venv/bin/activate
pip install .
ftirfun-mcp
```

### Run Streamable HTTP

```bash
FTIRFUN_API_KEY="your-ftirfun-api-key" \
ftirfun-mcp --transport streamable-http --host 127.0.0.1 --port 8001
```

### Docker

```bash
docker build -t ftirfun-mcp .
docker run --rm -p 8001:8001 -e FTIRFUN_API_KEY="your-ftirfun-api-key" ftirfun-mcp
```

---

## Tool Boundary

Use this MCP server for FTIR spectral-library screening only. Do not use for non-FTIR spectroscopy, general chemistry Q&A, or accredited laboratory certification.

---

## Registry & Links

| Resource | URL |
|----------|-----|
| Website | https://ftir.fun |
| Setup guide | https://ftir.fun/ai-integration/ |
| API docs | https://ftir.fun/api-docs/ |
| Hosted MCP endpoint | https://ftir.fun/mcp |
| Server card | https://ftir.fun/.well-known/mcp/server-card.json |
| Smithery | https://smithery.ai/servers/hlin2097/ftirfun |
| MCP.so | https://mcp.so/server/ftir-spectral-search/ftir_fun |
| PyPI | https://pypi.org/project/ftirfun-mcp/ |
