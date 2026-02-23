"""Shared MCP instance, Merchant API client singleton, and helper functions."""

from __future__ import annotations

import logging
import os
from typing import Any, Optional

import google.auth
import googleapiclient.discovery
from mcp.server.fastmcp import FastMCP

logger = logging.getLogger(__name__)

_GMC_SCOPE = "https://www.googleapis.com/auth/content"
_API_NAME = "content"
_API_VERSION = "v2.1"

mcp = FastMCP("Google Merchant Center")

_service: Optional[Any] = None


def _require_env(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise ValueError(f"Missing required env var: {name}")
    return value


def _get_service() -> Any:
    """Return a cached Google Content API (Merchant API) service object."""
    global _service
    if _service is not None:
        return _service

    credentials, _ = google.auth.default(scopes=[_GMC_SCOPE])
    _service = googleapiclient.discovery.build(
        _API_NAME, _API_VERSION, credentials=credentials
    )
    return _service


def _merchant_id() -> str:
    """Return the configured GMC Merchant ID from env."""
    return _require_env("GMC_MERCHANT_ID")
