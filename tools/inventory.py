"""Inventory tools — new Merchant API (inventories_v1beta)."""

from __future__ import annotations

from typing import Any, Dict, Optional

from tools._common import (
    mcp,
    account_name,
    get_local_inventory_client,
    get_regional_inventory_client,
)


@mcp.tool()
def insert_local_inventory(
    product_name: str,
    store_code: str,
    quantity: int,
    price_amount_micros: str,
    price_currency: str = "EUR",
    availability: str = "IN_STOCK",
) -> Dict[str, Any]:
    """Set or update local store inventory for a product.

    Args:
        product_name: Full product resource name, e.g. 'accounts/12345/products/online~de~DE~SKU'.
        store_code: Your GMC store code.
        quantity: Available quantity at this store.
        price_amount_micros: Price in micros (e.g. '4999000000' = 49.99 EUR).
        price_currency: ISO 4217 currency code, e.g. 'EUR'.
        availability: 'IN_STOCK', 'OUT_OF_STOCK', or 'LIMITED_AVAILABILITY'.
    """
    client = get_local_inventory_client()
    from google.shopping import merchant_inventories_v1beta
    local_inventory = {
        "storeCode": store_code,
        "availability": availability,
        "quantity": quantity,
        "price": {
            "amountMicros": price_amount_micros,
            "currencyCode": price_currency,
        },
    }
    request = merchant_inventories_v1beta.InsertLocalInventoryRequest(
        parent=product_name,
        local_inventory=local_inventory,
    )
    result = client.insert_local_inventory(request=request)
    return type(result).to_dict(result)


@mcp.tool()
def insert_regional_inventory(
    product_name: str,
    region: str,
    price_amount_micros: str,
    price_currency: str = "EUR",
    availability: str = "IN_STOCK",
    sale_price_amount_micros: Optional[str] = None,
) -> Dict[str, Any]:
    """Set regional price/availability override for a product.

    Use this to offer different prices per region (e.g. DE vs AT vs CH).

    Args:
        product_name: Full product resource name.
        region: Region resource name, e.g. 'accounts/12345/regions/region-id'.
        price_amount_micros: Price in micros.
        price_currency: ISO 4217 currency code.
        availability: 'IN_STOCK', 'OUT_OF_STOCK'.
        sale_price_amount_micros: Optional sale price in micros.
    """
    client = get_regional_inventory_client()
    from google.shopping import merchant_inventories_v1beta
    regional_inventory: Dict[str, Any] = {
        "region": region,
        "availability": availability,
        "price": {
            "amountMicros": price_amount_micros,
            "currencyCode": price_currency,
        },
    }
    if sale_price_amount_micros:
        regional_inventory["salePrice"] = {
            "amountMicros": sale_price_amount_micros,
            "currencyCode": price_currency,
        }
    request = merchant_inventories_v1beta.InsertRegionalInventoryRequest(
        parent=product_name,
        regional_inventory=regional_inventory,
    )
    result = client.insert_regional_inventory(request=request)
    return type(result).to_dict(result)
