"""Shipping settings tools — new Merchant API (accounts_v1beta)."""

from __future__ import annotations

from typing import Any, Dict

from tools._common import mcp, account_name, get_shipping_client


@mcp.tool()
def get_shipping_settings() -> Dict[str, Any]:
    """Get current shipping settings (services, carriers, rates) for this account."""
    client = get_shipping_client()
    from google.shopping import merchant_accounts_v1beta
    name = f"{account_name()}/shippingSettings"
    request = merchant_accounts_v1beta.GetShippingSettingsRequest(name=name)
    settings = client.get_shipping_settings(request=request)
    return type(settings).to_dict(settings)


@mcp.tool()
def update_shipping_settings(shipping_settings: Dict[str, Any]) -> Dict[str, Any]:
    """Update shipping settings for this account (full replacement).

    ⚠️ Fetch current settings with get_shipping_settings first, modify, then pass full object.

    Args:
        shipping_settings: Full ShippingSettings resource dict.
    """
    client = get_shipping_client()
    from google.shopping import merchant_accounts_v1beta
    request = merchant_accounts_v1beta.InsertShippingSettingsRequest(
        parent=account_name(),
        shipping_setting=shipping_settings,
    )
    result = client.insert_shipping_settings(request=request)
    return type(result).to_dict(result)
