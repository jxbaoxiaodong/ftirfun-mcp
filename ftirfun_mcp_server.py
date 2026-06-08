#!/usr/bin/env python3
"""MCP wrapper for the hosted FTIR.fun spectral-library API."""

from __future__ import annotations

import argparse
import os
import re
from typing import Annotated, Any

import httpx
from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations
from pydantic import Field


API_BASE_URL_ENV = "FTIRFUN_API_BASE_URL"
API_KEY_ENV = "FTIRFUN_API_KEY"
API_KEYS_ENV = "FTIRFUN_API_KEYS"
API_TIMEOUT_ENV = "FTIRFUN_API_TIMEOUT_SECONDS"
DEFAULT_API_BASE_URL = "https://ftir.fun"
DEFAULT_API_TIMEOUT_SECONDS = 120.0
DEFAULT_TOP_K = 15
DEFAULT_TOLERANCE_CM1 = 8
PEAK_MIN_CM1 = 400
PEAK_MAX_CM1 = 4500
MAX_QUERY_PEAKS = 32


mcp = FastMCP(
    "FTIR.fun Spectral Search",
    instructions=(
        "Use this server only for FTIR spectral-library search and material screening. "
        "It accepts FTIR peak lists, natural-language peak descriptions, or base64-encoded spectrum files. "
        "Results come from the hosted FTIR.fun API and are screening candidates, not accredited lab certification."
    ),
)


READ_ONLY_ANALYSIS = ToolAnnotations(
    title="FTIR.fun read-only spectrum analysis",
    readOnlyHint=True,
    destructiveHint=False,
    idempotentHint=True,
    openWorldHint=False,
)


def _api_base_url() -> str:
    return os.environ.get(API_BASE_URL_ENV, DEFAULT_API_BASE_URL).rstrip("/")


def _api_timeout_seconds() -> float:
    raw_value = os.environ.get(API_TIMEOUT_ENV)
    if raw_value is None:
        return DEFAULT_API_TIMEOUT_SECONDS
    return float(raw_value)


def _api_key() -> str:
    direct_key = os.environ.get(API_KEY_ENV, "").strip()
    if direct_key:
        return direct_key
    keys = [item.strip() for item in os.environ.get(API_KEYS_ENV, "").split(",") if item.strip()]
    return keys[0] if keys else ""


def _parse_peak_query(query: str) -> list[int]:
    values: list[int] = []
    seen: set[int] = set()
    for match in re.finditer(r"(?<!\d)(\d{3,4}(?:\.\d+)?)(?!\d)", str(query or "")):
        peak = int(round(float(match.group(1))))
        if peak < PEAK_MIN_CM1 or peak > PEAK_MAX_CM1 or peak in seen:
            continue
        seen.add(peak)
        values.append(peak)
    values.sort(reverse=True)
    return values[:MAX_QUERY_PEAKS]


def _normalized_peaks(peaks: list[float] | None, query: str) -> list[int]:
    values: list[int] = []
    seen: set[int] = set()
    for value in peaks or []:
        peak = int(round(float(value)))
        if peak < PEAK_MIN_CM1 or peak > PEAK_MAX_CM1 or peak in seen:
            continue
        seen.add(peak)
        values.append(peak)
    if not values and query:
        values = _parse_peak_query(query)
    values.sort(reverse=True)
    return values[:MAX_QUERY_PEAKS]


def _error(
    error_code: str,
    error_message: str,
    *,
    recovery_suggestions: list[str],
    retryable: bool,
    details: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return {
        "success": False,
        "error_code": error_code,
        "error_message": error_message,
        "recovery_suggestions": recovery_suggestions,
        "retryable": retryable,
        "details": details or {},
    }


@mcp.tool(
    annotations=READ_ONLY_ANALYSIS,
)
def analyze_ftir_spectrum(
    query: Annotated[
        str,
        Field(
            default="",
            description="Natural-language FTIR request. Peak positions such as 1730, 1600, 1250 cm-1 can be extracted automatically.",
        ),
    ] = "",
    peaks: Annotated[
        list[float] | None,
        Field(default=None, description="FTIR peak positions in cm-1."),
    ] = None,
    file_base64: Annotated[
        str | None,
        Field(default=None, description="Optional base64-encoded FTIR spectrum file."),
    ] = None,
    filename: Annotated[
        str,
        Field(default="spectrum.0", description="Original filename for FTIR format detection."),
    ] = "spectrum.0",
    top_k: Annotated[
        int,
        Field(default=DEFAULT_TOP_K, ge=1, le=50, description="Number of ranked library candidates to return."),
    ] = DEFAULT_TOP_K,
    tolerance_cm1: Annotated[
        int,
        Field(default=DEFAULT_TOLERANCE_CM1, ge=1, le=30, description="Peak-only search tolerance in cm-1."),
    ] = DEFAULT_TOLERANCE_CM1,
) -> dict[str, Any]:
    """
    Search the FTIR.fun spectral library for one unknown FTIR spectrum in one call.

    Use when the user provides an FTIR peak list, a natural-language description containing peaks,
    or a base64-encoded FTIR instrument file and wants ranked material candidates.
    Do not use for general chemistry Q&A, non-FTIR spectra, or institutional report review.
    """
    normalized_peaks = _normalized_peaks(peaks, query)
    if not file_base64 and not normalized_peaks:
        return _error(
            "missing_spectrum_input",
            "Provide FTIR peak positions or a base64-encoded FTIR spectrum file.",
            recovery_suggestions=[
                "Ask the user for FTIR peak positions in cm-1.",
                "If the user has an instrument file, pass it as file_base64 with the original filename.",
            ],
            retryable=False,
        )

    api_key = _api_key()
    if not api_key:
        return _error(
            "api_key_required",
            f"Set {API_KEY_ENV} or {API_KEYS_ENV} before calling the hosted FTIR.fun API.",
            recovery_suggestions=[
                f"Set {API_KEY_ENV} in the MCP server environment.",
                "Use the hosted FTIR.fun MCP endpoint if you already have a managed FTIR.fun integration.",
            ],
            retryable=False,
        )

    body = {
        "spectrum": {
            "type": "ftir",
            "x_unit": "cm-1",
            "y_unit": "absorbance",
            "peaks": normalized_peaks or None,
        },
        "task_context": {
            "goal": "identification",
            "sample_type": "unknown",
        },
        "options": {
            "top_k": top_k,
            "tolerance_cm1": tolerance_cm1,
        },
        "file_base64": file_base64,
        "filename": filename,
    }
    headers = {"X-API-Key": api_key, "X-FTIRFUN-Client": "ftirfun-mcp-public-wrapper"}

    try:
        response = httpx.post(
            f"{_api_base_url()}/ftir/analyze_spectrum",
            json=body,
            headers=headers,
            timeout=_api_timeout_seconds(),
        )
    except httpx.TimeoutException:
        return _error(
            "upstream_timeout",
            "The hosted FTIR.fun API did not respond before the configured timeout.",
            recovery_suggestions=["Retry later.", f"Increase {API_TIMEOUT_ENV} for large spectrum files."],
            retryable=True,
        )
    except httpx.HTTPError as exc:
        return _error(
            "upstream_http_error",
            "The MCP wrapper could not reach the hosted FTIR.fun API.",
            recovery_suggestions=["Check network access to https://ftir.fun.", "Retry later."],
            retryable=True,
            details={"exception": exc.__class__.__name__},
        )

    if response.status_code == 429:
        return _error(
            "rate_limit_exceeded",
            "The hosted FTIR.fun API returned HTTP 429.",
            recovery_suggestions=[
                "Wait before retrying.",
                f"Retry-After: {response.headers.get('Retry-After', 'not provided')}",
            ],
            retryable=True,
        )

    try:
        payload = response.json()
    except ValueError:
        return _error(
            "invalid_upstream_response",
            "The hosted FTIR.fun API returned a non-JSON response.",
            recovery_suggestions=["Retry later.", "Contact FTIR.fun support if this repeats."],
            retryable=True,
            details={"status_code": response.status_code},
        )

    if response.status_code >= 400:
        return _error(
            "upstream_error",
            "The hosted FTIR.fun API rejected the request.",
            recovery_suggestions=payload.get("recovery_suggestions")
            or ["Check the API key and input spectrum.", "Retry later if the response was a server error."],
            retryable=bool(payload.get("retryable", response.status_code >= 500)),
            details={"status_code": response.status_code, "upstream": payload},
        )

    payload["source"] = {
        "service": "FTIR.fun",
        "api_base_url": _api_base_url(),
        "mcp_wrapper": "jxbaoxiaodong/ftirfun-mcp",
    }
    return payload


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the FTIR.fun MCP wrapper.")
    parser.add_argument("--transport", default=os.environ.get("FTIRFUN_MCP_TRANSPORT", "stdio"))
    parser.add_argument("--host", default=os.environ.get("FTIRFUN_MCP_HOST", "127.0.0.1"))
    parser.add_argument("--port", type=int, default=int(os.environ.get("FTIRFUN_MCP_PORT", "8001")))
    args = parser.parse_args()

    if args.transport != "stdio":
        mcp.settings.host = args.host
        mcp.settings.port = args.port
    mcp.run(transport=args.transport)


if __name__ == "__main__":
    main()
