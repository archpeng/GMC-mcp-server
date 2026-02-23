"""Inventory tools — regional and local inventory management."""

from __future__ import annotations

from typing import Any, Dict

from tools._common import mcp, _get_service, _merchant_id


@mcp.tool()
def insert_regional_inventory(
    product_id: str,
    region_id: str,
    price: Dict[str, str],
    availability: str = "in stock",
    sale_price: Optional[Dict[str, str]] = None,
) -> Dict[str, Any]:
    """Set regional pricing/availability overrides for a product.

    Use this to set different prices for DE vs AT vs CH without modifying the base product.

    Args:
        product_id: Full REST product ID, e.g. 'online:de:DE:SKU123'.
        region_id: Region ID (from list_regions). e.g. '1234567'.
        price: Dict with 'value' and 'currency', e.g. {'value': '49.99', 'currency': 'EUR'}.
        availability: 'in stock', 'out of stock', or 'preorder'.
        sale_price: Optional sale price dict.
    """
    svc = _get_service()
    body: Dict[str, Any] = {
        "regionId": region_id,
        "price": price,
        "availability": availability,
    }
    if sale_price:
        body["salePrice"] = sale_price
    return svc.regionalinventory().insert(
        merchantId=_merchant_id(), productId=product_id, body=body
    ).execute()


@mcp.tool()
def insert_local_inventory(
    product_id: str,
    store_code: str,
    quantity: int,
    price: Dict[str, str],
    availability: str = "in stock",
) -> Dict[str, Any]:
    """Update local store inventory for a product (for local inventory ads).

    Args:
        product_id: Full REST product ID.
        store_code: Store code as configured in your GMC local inventory setup.
        quantity: Available quantity at this store.
        price: Dict with 'value' and 'currency'.
        availability: 'in stock', 'out of stock', 'limited availability'.
    """
    svc = _get_service()
    body: Dict[str, Any] = {
        "storeCode": store_code,
        "quantity": quantity,
        "price": price,
        "availability": availability,
    }
    return svc.localinventory().insert(
        merchantId=_merchant_id(), productId=product_id, body=body
    ).execute()


# Optional import needed for sale_price parameter
from typing import Optional  # noqa: E402
