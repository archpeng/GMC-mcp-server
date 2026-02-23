"""Collections tools — manage product collections in GMC."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from tools._common import mcp, _get_service, _merchant_id


@mcp.tool()
def list_collections(
    page_token: Optional[str] = None,
) -> Dict[str, Any]:
    """List all product collections in the GMC account."""
    svc = _get_service()
    req = svc.collections().list(
        merchantId=_merchant_id(),
        **({"pageToken": page_token} if page_token else {}),
    )
    resp = req.execute()
    return {
        "collections": resp.get("resources", []),
        "totalReturned": len(resp.get("resources", [])),
        "nextPageToken": resp.get("nextPageToken"),
    }


@mcp.tool()
def get_collection(collection_id: str) -> Dict[str, Any]:
    """Get details of a single collection.

    Args:
        collection_id: Collection ID from list_collections.
    """
    svc = _get_service()
    return svc.collections().get(
        merchantId=_merchant_id(), collectionId=collection_id
    ).execute()


@mcp.tool()
def get_collection_status(collection_id: str) -> Dict[str, Any]:
    """Get approval status of a collection.

    Args:
        collection_id: Collection ID.
    """
    svc = _get_service()
    return svc.collectionstatuses().get(
        merchantId=_merchant_id(), collectionId=collection_id
    ).execute()


@mcp.tool()
def create_collection(
    collection_id: str,
    headline: str,
    link: str,
    image_link: str,
    featured_product_ids: Optional[List[str]] = None,
    language: str = "de",
) -> Dict[str, Any]:
    """Create a product collection for Shopping showcase ads.

    Args:
        collection_id: Unique ID for this collection (alphanumeric + hyphens).
        headline: Collection headline (max 150 chars).
        link: URL to the collection page on your website.
        image_link: URL to the collection hero image.
        featured_product_ids: List of product offer IDs to feature.
        language: BCP 47 language code.
    """
    svc = _get_service()
    body: Dict[str, Any] = {
        "id": collection_id,
        "language": language,
        "headline": [headline],
        "link": link,
        "imageLink": [image_link],
    }
    if featured_product_ids:
        body["featuredProduct"] = [{"offerId": oid} for oid in featured_product_ids]
    return svc.collections().create(
        merchantId=_merchant_id(), body=body
    ).execute()
