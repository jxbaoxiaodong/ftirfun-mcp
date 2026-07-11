# FTIR.fun MCP Server

[![smithery badge](https://smithery.ai/badge/hlin2097/ftirfun)](https://smithery.ai/servers/hlin2097/ftirfun)
[![MCP.so](https://img.shields.io/badge/MCP.so-listed-blue)](https://mcp.so/server/ftir-spectral-search/ftir_fun)

MCP server for FTIR spectral-library work and material identification. Connects AI assistants to 135,000+ FTIR reference spectra with hosted tools for instrument-file parsing, unknown-spectrum analysis, full tri-axis reports, peak explanation, reference-spectrum lookup, and historical-result fetch.

## Tools

### `parse_ftir_spectrum`

Parse a base64-encoded FTIR instrument file into aligned curve points and detected peaks.

### `analyze_ftir_spectrum`

Search the FTIR.fun spectral library for one unknown FTIR spectrum.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `query` | string | No | Natural-language FTIR request. Peak positions (e.g. "1730, 1600, 1250 cm-1") are extracted automatically. |
| `peaks` | number[] | No | FTIR peak positions in cm⁻¹ (e.g. `[1736, 1379, 1241]`). |
| `file_base64` | string | No | Base64-encoded FTIR spectrum file (supports 28+ formats: Thermo .spa/.spc, Bruker .opus, PerkinElmer .sp, JCAMP-DX, CSV, Excel). |
| `filename` | string | No | Original filename for format detection (e.g. `"sample.spa"`). |
| `top_k` | integer | No | Number of ranked candidates to return (1–50, default 15). |
| `tolerance_cm1` | integer | No | Peak matching tolerance in cm⁻¹ (1–30, default 8). |

**Returns:** Ranked candidate materials with library similarity scores, peak-by-peak explanations linked to published literature (DOI), confidence levels, and uncertainty disclosures.

### `submit_ftir_report`

Submit a base64-encoded spectrum file to the existing full FTIR.fun tri-axis workflow. Returns `task_id` and `result_num`.

### `get_ftir_report_status`

Poll the `task_id` returned by `submit_ftir_report`. When complete, the response includes the same structured `report_view` used by the FTIR.fun website and the final `report_url`.

### `explain_peaks`

Explain one or more FTIR peaks without requiring a full library search.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `query` | string | No | Natural-language FTIR peak question, for example `"What does 1715 cm-1 indicate?"`. |
| `peaks` | number[] | No | One or more FTIR peak positions in cm⁻¹. |
| `sampling_mode` | string | No | Optional sampling mode such as `ATR`, `Thin Film`, or `KBr Pellet`. |

**Returns:** Structured peak explanations with supporting assignments and uncertainty wording when available.

### `find_spectra`

Find FTIR library reference spectra by substance name, CAS number, spectrum number, or keywords.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `query` | string | Yes | Substance name, CAS number, FTIR library `NUM`, or keywords. |
| `limit` | integer | No | Number of reference spectra to return (1–20, default 10). |

**Returns:** Matching reference spectra with `num`, names, CAS, peak markers, and library curve data.

### `fetch_result`

Fetch one historical FTIR.fun result by report number.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `result_num` | string | Yes | FTIR.fun report/result number. |
| `language_code` | string | No | Display language for the stored result context, default `en`. |

**Returns:** Structured historical result context with `report_url`, `headline`, `summary`, `report_view`, and `result_context`.

## Hosted MCP (Recommended)

Connect directly to the production endpoint — no local install required:

For VS Code, use `.vscode/mcp.json` or the user-level MCP configuration:

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

This is direct Bearer API-key authentication. FTIR.fun does not use OAuth dynamic client registration or an `/authorize` page. Do not use the nonexistent `@ftirfun/mcp-server` npm package; the hosted URL needs no local install.

One-line setup for Claude Code:

```bash
claude mcp add ftirfun https://ftir.fun/mcp
```

The hosted endpoint exposes seven FTIR tools (`parse_ftir_spectrum`, `analyze_ftir_spectrum`, `submit_ftir_report`, `get_ftir_report_status`, `explain_peaks`, `find_spectra`, `fetch_result`) and is the canonical production service.

## Self-Hosted (Local Wrapper)

This repository provides a lightweight local MCP wrapper that proxies to the hosted API. The local wrapper exposes the same seven FTIR tools as the hosted server.

### Configuration

```bash
export FTIRFUN_API_KEY="your-ftirfun-api-key"
```

Optional:

```bash
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

### Push This Repo To GitHub

This repo includes its own push helper:

```bash
bash push_github_main.sh origin main "your commit message"
```

Token resolution order:

1. `GITHUB_ENV_FILE=/path/to/env`
2. `./.env`
3. shared fallback `/home/bob/projects/ftirfun/.env`

For registry introspection, the server can start without an API key. Tool calls that require the hosted API return a structured `api_key_required` error until `FTIRFUN_API_KEY` is configured.

## Tool Boundary

Use this MCP server for FTIR spectral-library screening only.

Do not use for:
- Non-FTIR spectroscopy
- General chemistry Q&A
- Institutional AI-only review of existing third-party reports
- Accredited laboratory certification

## Registry Links

- Hosted MCP: https://ftir.fun/mcp
- Server Card: https://ftir.fun/.well-known/mcp/server-card.json
- Smithery: https://smithery.ai/servers/hlin2097/ftirfun
- MCP.so: https://mcp.so/server/ftir-spectral-search/ftir_fun
- PyPI: https://pypi.org/project/ftirfun-mcp/
- Website: https://ftir.fun
