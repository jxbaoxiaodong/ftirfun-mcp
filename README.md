# FTIR.fun MCP Server

[![smithery badge](https://smithery.ai/badge/hlin2097/ftirfun)](https://smithery.ai/servers/hlin2097/ftirfun)

MCP wrapper for the hosted FTIR.fun spectral-library API.

This repository is intentionally small and public. It does not contain the private FTIR.fun web application, spectral-library data, API keys, user data, or institutional AI-only report-review logic.

## What It Does

- Exposes one task-level MCP tool: `analyze_ftir_spectrum`
- Accepts FTIR peak lists, natural-language peak descriptions, or base64-encoded FTIR spectrum files
- Calls the hosted FTIR.fun API at `https://ftir.fun/ftir/analyze_spectrum`
- Returns ranked spectral-library candidates and evidence-oriented response fields from FTIR.fun

## Configuration

Set one API key in the runtime environment:

```bash
export FTIRFUN_API_KEY="your-ftirfun-api-key"
```

Optional settings:

```bash
export FTIRFUN_API_BASE_URL="https://ftir.fun"
export FTIRFUN_API_TIMEOUT_SECONDS="120"
```

## Run Locally

```bash
python -m venv .venv
. .venv/bin/activate
pip install .
ftirfun-mcp
```

## Run Streamable HTTP

```bash
FTIRFUN_API_KEY="your-ftirfun-api-key" \
ftirfun-mcp --transport streamable-http --host 127.0.0.1 --port 8001
```

## Docker

```bash
docker build -t ftirfun-mcp .
docker run --rm -p 8001:8001 -e FTIRFUN_API_KEY="your-ftirfun-api-key" ftirfun-mcp
```

For registry introspection, the server can start without an API key. Tool calls that require the hosted API return a structured `api_key_required` error until `FTIRFUN_API_KEY` is configured.

## Tool Boundary

Use `analyze_ftir_spectrum` for FTIR spectral-library screening only.

Do not use this MCP server for:

- non-FTIR spectroscopy
- general chemistry Q&A
- institutional AI-only review of existing third-party reports
- accredited laboratory certification

## Hosted MCP

FTIR.fun also provides a hosted MCP endpoint:

```text
https://ftir.fun/mcp
```

The hosted endpoint is the canonical production service. This public repository is the small open-source MCP wrapper used for public MCP registries and self-hosted client installs.

## Registry Links

- Smithery: https://smithery.ai/servers/hlin2097/ftirfun
