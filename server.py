#!/usr/bin/env python3
"""Google Merchant Center MCP Server — entry point.

All tool implementations live under tools/.
Run: python server.py
"""

from __future__ import annotations

import logging

logging.basicConfig(level=logging.INFO)

# Import mcp instance (triggers registration of all 34 tools via tools/__init__.py)
from tools import mcp  # noqa: F401

if __name__ == "__main__":
    mcp.run()
