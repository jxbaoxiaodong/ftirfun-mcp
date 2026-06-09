# FTIR.fun MCP Server

[![smithery badge](https://smithery.ai/badge/hlin2097/ftirfun)](https://smithery.ai/servers/hlin2097/ftirfun)
[![MCP.so](https://img.shields.io/badge/MCP.so-listed-blue)](https://mcp.so/server/ftir-spectral-search/ftir_fun)

MCP server for FTIR spectral-library search and material identification. Connects AI assistants to 135,000+ FTIR reference spectra with literature-backed peak assignments (DOI-cited).

## Tools

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

### `search`

Search public FTIR.fun result pages by keyword.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `query` | string | Yes | Search query string. |

**Returns:** Matching public result pages with `id`, `url`, `title`, `text`, and metadata.

### `fetch`

Fetch one public FTIR.fun result document by ID.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | string | Yes | Result ID in `result:<number>` format or bare number. |

**Returns:** Full result document with `url`, `headline`, `summary`, `report_view`, and metadata.

## Hosted MCP (Recommended)

Connect directly to the production endpoint — no local install required:

```json
{
  "mcpServers": {
    "ftirfun": {
      "url": "https://ftir.fun/mcp",
      "headers": {
        "Authorization": "Bearer <YOUR_FTIRFUN_API_KEY>"
      }
    }
  }
}
```

One-line setup for Claude Code:

```bash
claude mcp add ftirfun https://ftir.fun/mcp
```

The hosted endpoint exposes all three tools (`analyze_ftir_spectrum`, `search`, `fetch`) and is the canonical production service.

## Self-Hosted (Local Wrapper)

This repository provides a lightweight local MCP wrapper that proxies to the hosted API. The local wrapper exposes `analyze_ftir_spectrum` only.

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
