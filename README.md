[中文](README.zh.md) | English | [Español](README.es.md) | [Français](README.fr.md) | [日本語](README.ja.md)

# FTIR.fun MCP Server

[![smithery badge](https://smithery.ai/badge/hlin2097/ftirfun)](https://smithery.ai/servers/hlin2097/ftirfun)
[![MCP.so](https://img.shields.io/badge/MCP.so-listed-blue)](https://mcp.so/server/ftir-spectral-search/ftir_fun)
[![PyPI](https://img.shields.io/pypi/v/ftirfun-mcp)](https://pypi.org/project/ftirfun-mcp/)

MCP server and REST API client for **[FTIR.fun](https://ftir.fun)** — gives AI assistants and code pipelines direct access to 130,000+ FTIR infrared reference spectra for material identification, peak explanation, and spectral library search.

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

## MCP Tools

The hosted MCP endpoint `https://ftir.fun/mcp` exposes seven tools.

---

### `analyze_ftir_spectrum`

Search the FTIR infrared spectral library for one unknown spectrum. Accepts peaks, a natural-language query, or a raw instrument file.

**Parameters**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `query` | string | No | Natural-language FTIR request — peak positions such as "1730, 1600, 1250 cm-1" are extracted automatically. |
| `peaks` | number[] | No | FTIR peak positions in cm⁻¹ (e.g. `[1736, 1379, 1241]`). |
| `file_base64` | string | No | Base64-encoded FTIR instrument file. Supports 28+ formats: Thermo `.spa`/`.spc`, Bruker `.opus`, PerkinElmer `.sp`, JCAMP-DX `.jdx`/`.dx`, CSV, Excel, and more. |
| `filename` | string | No | Original filename for format detection (e.g. `"sample.spa"`). |
| `top_k` | integer | No | Number of ranked candidates to return (1–50, default 15). |
| `tolerance_cm1` | integer | No | Peak matching tolerance in cm⁻¹ (1–30, default 8). |

**Returns:** Ranked candidate materials with library similarity scores, peak-by-peak evidence linked to published literature (DOI), confidence levels, and uncertainty disclosures.

**Example**
```
Identify this infrared spectrum: peaks at 2915, 1715, 1450, 1260, 1090 cm-1.
```

---

### `explain_peaks`

Explain one or more FTIR infrared peaks without requiring a full spectral library search. Useful for quick functional-group assignment and wavenumber interpretation.

**Parameters**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `query` | string | No | Natural-language peak question, e.g. `"What does 1715 cm-1 indicate in an ester?"` |
| `peaks` | number[] | No | One or more FTIR peak positions in cm⁻¹. |
| `sampling_mode` | string | No | `ATR`, `Thin Film`, `KBr Pellet`, `Nujol Mull`, etc. |

**Returns:** Structured peak explanations with functional-group assignments and uncertainty wording when available.

**Example**
```
Use FTIR.fun to explain the infrared peaks at 1715 and 3300 cm-1 in ATR mode.
```

---

### `parse_ftir_spectrum`

Parse a base64-encoded FTIR instrument file into aligned wavenumber-intensity curve points and automatically detected peak positions. Use this to extract raw spectral data before analysis.

**Parameters**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `file_base64` | string | Yes | Base64-encoded FTIR instrument file. |
| `filename` | string | Yes | Original filename (e.g. `"sample.spa"`) for format detection. |

**Returns:** Aligned `(wavenumber, intensity)` data points and a list of detected peak positions in cm⁻¹.

---

### `find_spectra`

Find FTIR library reference spectra by substance name, CAS number, spectrum number, or keywords. Returns raw spectral curve data for direct comparison.

**Parameters**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `query` | string | Yes | Substance name (e.g. `"polypropylene"`), CAS number, FTIR library `NUM`, or keywords. |
| `limit` | integer | No | Number of reference spectra to return (1–20, default 10). |

**Returns:** Matching reference spectra with `num`, names, CAS, peak markers, and library curve data.

**Example**
```
Find FTIR reference spectra for polyethylene terephthalate (PET).
```

---

### `submit_ftir_report`

Submit a base64-encoded FTIR spectrum file to the full FTIR.fun tri-axis identification workflow — the same multi-stage analysis used on the website. Returns a `task_id` and `result_num` immediately; poll with `get_ftir_report_status` for the completed report.

**Parameters**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `file_base64` | string | Yes | Base64-encoded FTIR instrument file. |
| `filename` | string | Yes | Original filename for format detection. |

**Returns:** `{ task_id, result_num }`

---

### `get_ftir_report_status`

Poll the status of a report submitted via `submit_ftir_report`. When complete, the response includes the full structured `report_view` (the same data shown on the FTIR.fun website) and a shareable `report_url`.

**Parameters**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `task_id` | string | Yes | `task_id` returned by `submit_ftir_report`. |

**Returns:** Status field plus `report_view` and `report_url` when complete.

---

### `fetch_result`

Fetch a historical FTIR.fun infrared analysis result by report number.

**Parameters**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `result_num` | string | Yes | FTIR.fun report/result number. |
| `language_code` | string | No | Display language for the stored result context (default `en`). |

**Returns:** Structured context with `report_url`, `headline`, `summary`, `report_view`, and `result_context`.

---

## REST API

Call FTIR.fun directly from any language — Python, JavaScript, R, MATLAB, Go. Ideal for LIMS integrations, batch spectral processing pipelines, or adding infrared spectrum search to your own application.

Full API reference: https://ftir.fun/api-docs/

### Health check (no key required)

```bash
curl https://ftir.fun/health
# → {"status":"ok","service":"ftirfun-api"}
```

### Identify an unknown infrared spectrum — peak list

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

Supports 28+ instrument formats: Thermo `.spa`/`.spc`, Bruker `.opus`, PerkinElmer `.sp`, JCAMP-DX `.jdx`/`.dx`, CSV, Excel, and more.

### Explain infrared peaks

```bash
curl -X POST https://ftir.fun/ftir/explain_peaks \
  -H "X-API-Key: ftir_your_key_here" \
  -H "Content-Type: application/json" \
  -d '{"peaks": [1715, 2915], "sampling_mode": "ATR"}'
```

### Search reference spectra by name or CAS

```bash
curl "https://ftir.fun/v1/search?q=polypropylene&limit=5" \
  -H "X-API-Key: ftir_your_key_here"
```

---

## MCP Client Setup

The hosted MCP endpoint requires no local install. Use `https://ftir.fun/mcp` with a `Bearer` token.

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

Open Command Palette → **MCP: List Servers** → select `ftirfun` → **Start**.

### Claude Desktop / Claude Code

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

Create or edit `~/.cursor/mcp.json`:

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

Any other MCP client that supports a remote streamable-HTTP server works: set the URL to `https://ftir.fun/mcp` and send `Authorization: Bearer <your key>`. Full tool schema: [server-card.json](https://ftir.fun/.well-known/mcp/server-card.json).

---

## Self-Hosted (Local Wrapper)

A lightweight local MCP wrapper that proxies to the hosted API. Exposes the same seven FTIR tools.

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

## About FTIR.fun

**[FTIR.fun](https://ftir.fun)** is a cloud platform for infrared spectroscopy analysis used by researchers and engineers in 52+ countries. It gives fast access to a continuously updated library of **130,000+ FTIR reference spectra** covering polymers, additives, coatings, pharmaceuticals, and industrial chemicals.

What you can do on [ftir.fun](https://ftir.fun):

- **Spectral library search** — upload an instrument file or paste peak positions; get ranked matches with similarity scores and literature DOI citations
- **AI peak explanation** — ask about any wavenumber; receive functional-group assignments backed by a chemical knowledge graph
- **Full tri-axis report** — automatic multi-stage material identification with a shareable result URL
- **Image-to-CSV extraction** — digitize a spectrum curve from a published figure
- **Formulation workbench** — multi-component deformulation and unknown-mixture analysis

Step-by-step setup guides: https://ftir.fun/ai-integration/

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
