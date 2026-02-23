"""Product CRUD and status tools."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from tools._common import mcp, _get_service, _merchant_id


@mcp.tool()
def list_products(
    max_results: int = 50,
    page_token: Optional[str] = None,
) -> Dict[str, Any]:
    """List products in GMC with pagination.

    Args:
        max_results: Max products to return (1–250).
        page_token: Pagination token from a previous call.
    """
    svc = _get_service()
    req = svc.products().list(
        merchantId=_merchant_id(),
        maxResults=min(max_results, 250),
        **({"pageToken": page_token} if page_token else {}),
    )
    resp = req.execute()
    items = [
        {
            "id": p.get("id"),
            "title": p.get("title"),
            "brand": p.get("brand"),
            "availability": p.get("availability"),
            "price": p.get("price"),
            "link": p.get("link"),
            "imageLink": p.get("imageLink"),
            "condition": p.get("condition"),
            "channel": p.get("channel"),
            "targetCountry": p.get("targetCountry"),
            "contentLanguage": p.get("contentLanguage"),
            "offerId": p.get("offerId"),
        }
        for p in resp.get("resources", [])
    ]
    return {
        "products": items,
        "totalReturned": len(items),
        "nextPageToken": resp.get("nextPageToken"),
    }


@mcp.tool()
def get_product(product_id: str) -> Dict[str, Any]:
    """Get full details of a single GMC product.

    Args:
        product_id: Full REST product ID, e.g. 'online:de:DE:SKU123'.
    """
    svc = _get_service()
    return svc.products().get(
        merchantId=_merchant_id(), productId=product_id
    ).execute()


@mcp.tool()
def insert_product(product: Dict[str, Any]) -> Dict[str, Any]:
    """Insert (create or replace) a product in GMC.

    Args:
        product: Full product dict following the GMC Product resource schema.
                 Required fields: offerId, title, description, link, imageLink,
                 contentLanguage, targetCountry, channel, availability, price,
                 brand, condition, googleProductCategory.

    Example:
        {
          "offerId": "SKU-001",
          "title": "Loop Isolierbecher 10-seitig",
          "description": "Doppelwandiger Isolierbecher aus 304 Edelstahl...",
          "link": "https://example.com/products/my-product",
          "imageLink": "https://cdn.shopify.com/...",
          "contentLanguage": "de",
          "targetCountry": "DE",
          "channel": "online",
          "availability": "in stock",
          "price": {"value": "49.99", "currency": "EUR"},
          "brand": "Loopsorbit",
          "condition": "new"
        }
    """
    svc = _get_service()
    return svc.products().insert(
        merchantId=_merchant_id(), body=product
    ).execute()


@mcp.tool()
def update_product(product_id: str, update_mask: str, product: Dict[str, Any]) -> Dict[str, Any]:
    """Partially update a GMC product (PATCH — only specified fields are changed).

    Args:
        product_id: Full REST product ID, e.g. 'online:de:DE:SKU123'.
        update_mask: Comma-separated field paths to update, e.g. 'title,price,availability'.
        product: Dict with only the fields to update.
    """
    svc = _get_service()
    return svc.products().update(
        merchantId=_merchant_id(),
        productId=product_id,
        updateMask=update_mask,
        body=product,
    ).execute()


@mcp.tool()
def delete_product(product_id: str) -> Dict[str, Any]:
    """Delete a product from GMC permanently.

    Args:
        product_id: Full REST product ID, e.g. 'online:de:DE:SKU123'.
    """
    svc = _get_service()
    svc.products().delete(
        merchantId=_merchant_id(), productId=product_id
    ).execute()
    return {"deleted": True, "productId": product_id}


@mcp.tool()
def list_product_statuses(
    max_results: int = 50,
    page_token: Optional[str] = None,
) -> Dict[str, Any]:
    """List approval status of all products — shows approved, pending, and disapproved items.

    Args:
        max_results: Max products to return (1–250).
        page_token: Pagination token.
    """
    svc = _get_service()
    resp = svc.productstatuses().list(
        merchantId=_merchant_id(),
        maxResults=min(max_results, 250),
        **({"pageToken": page_token} if page_token else {}),
    ).execute()
    rows = [
        {
            "productId": s.get("productId"),
            "title": s.get("title"),
            "creationDate": s.get("creationDate"),
            "lastUpdateDate": s.get("lastUpdateDate"),
            "googleExpirationDate": s.get("googleExpirationDate"),
            "destinationStatuses": s.get("destinationStatuses", []),
            "issueCount": len(s.get("itemLevelIssues", [])),
            "issues": [
                {
                    "code": i.get("code"),
                    "servability": i.get("servability"),
                    "resolution": i.get("resolution"),
                    "description": i.get("description"),
                    "attribute": i.get("attribute"),
                }
                for i in s.get("itemLevelIssues", [])
            ],
        }
        for s in resp.get("resources", [])
    ]
    return {
        "statuses": rows,
        "totalReturned": len(rows),
        "nextPageToken": resp.get("nextPageToken"),
    }


@mcp.tool()
def get_product_status(product_id: str) -> Dict[str, Any]:
    """Get the GMC approval status and all issues for a single product.

    Args:
        product_id: Full REST product ID, e.g. 'online:de:DE:SKU123'.
    """
    svc = _get_service()
    return svc.productstatuses().get(
        merchantId=_merchant_id(), productId=product_id
    ).execute()


@mcp.tool()
def count_products_by_status() -> Dict[str, Any]:
    """Summarise product counts by approval status (approved / disapproved / pending).

    Fetches up to 250 product statuses and tallies them.
    For larger catalogs, call list_product_statuses with pagination.
    """
    svc = _get_service()
    resp = svc.productstatuses().list(
        merchantId=_merchant_id(), maxResults=250
    ).execute()
    approved = pending = disapproved = 0
    for s in resp.get("resources", []):
        for ds in s.get("destinationStatuses", []):
            status = ds.get("status", "")
            if status == "approved":
                approved += 1
            elif status == "disapproved":
                disapproved += 1
            elif status == "pending":
                pending += 1
    return {
        "approved": approved,
        "disapproved": disapproved,
        "pending": pending,
        "total": approved + disapproved + pending,
    }
