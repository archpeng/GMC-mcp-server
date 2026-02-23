"""Shipping settings tools."""

from __future__ import annotations

from typing import Any, Dict

from tools._common import mcp, _get_service, _merchant_id


@mcp.tool()
def get_shipping_settings() -> Dict[str, Any]:
    """Get current shipping settings for the GMC account (services, rates, addresses)."""
    svc = _get_service()
    return svc.shippingsettings().get(
        merchantId=_merchant_id(), accountId=_merchant_id()
    ).execute()


@mcp.tool()
def update_shipping_settings(settings: Dict[str, Any]) -> Dict[str, Any]:
    """Update shipping settings for the account (full replacement).

    ⚠️ This replaces the ENTIRE shipping configuration. Fetch current settings
    with get_shipping_settings first, modify, then pass the full updated object.

    Args:
        settings: Full shipping settings resource dict.
    """
    svc = _get_service()
    return svc.shippingsettings().update(
        merchantId=_merchant_id(), accountId=_merchant_id(), body=settings
    ).execute()


@mcp.tool()
def get_supported_carriers() -> Dict[str, Any]:
    """List all shipping carriers supported by Google for this merchant's country."""
    svc = _get_service()
    return svc.shippingsettings().getsupportedcarriers(
        merchantId=_merchant_id()
    ).execute()


@mcp.tool()
def get_supported_holidays() -> Dict[str, Any]:
    """List holidays supported for carrier-calculated shipping cutoffs."""
    svc = _get_service()
    return svc.shippingsettings().getsupportedholidays(
        merchantId=_merchant_id()
    ).execute()
