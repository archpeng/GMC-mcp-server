"""Collections — NOTE: Collections are not yet GA in the new Merchant API.

The new Merchant API does not yet have a stable Collections sub-service.
This module uses direct HTTP requests to the new REST endpoint as a fallback.
When a stable Python client is released, this module should be updated.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from tools._common import mcp, account_name, merchant_id, _get_credentials


def _collections_http_request(method: str, path: str, body: Optional[Dict] = None) -> Dict[str, Any]:
    """Make an authenticated HTTP request to the Merchant API collections endpoint."""
    import google.auth.transport.requests
    import urllib.request
    import json

    credentials = _get_credentials()
    auth_req = google.auth.transport.requests.Request()
    credentials.refresh(auth_req)

    base = f"https://merchantapi.googleapis.com/collections/v1beta/{path}"
    data = json.dumps(body).encode() if body else None
    req = urllib.request.Request(
        base,
        data=data,
        method=method,
        headers={
            "Authorization": f"Bearer {credentials.token}",
            "Content-Type": "application/json",
        },
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())


@mcp.tool()
def list_collections(page_token: Optional[str] = None) -> Dict[str, Any]:
    """List product collections for this GMC account.

    Note: Uses Merchant API v1beta REST endpoint (no stable Python client yet).
    """
    acct = account_name()
    path = f"{acct}/collections"
    if page_token:
        path += f"?pageToken={page_token}"
    result = _collections_http_request("GET", path)
    return {
        "collections": result.get("collections", []),
        "nextPageToken": result.get("nextPageToken"),
        "totalReturned": len(result.get("collections", [])),
    }


@mcp.tool()
def get_collection(collection_id: str) -> Dict[str, Any]:
    """Get details of a single collection.

    Args:
        collection_id: Collection ID.
    """
    path = f"{account_name()}/collections/{collection_id}"
    return _collections_http_request("GET", path)


@mcp.tool()
def create_collection(
    collection_id: str,
    headline: str,
    link: str,
    image_link: str,
    featured_product_ids: Optional[List[str]] = None,
    language: str = "de",
) -> Dict[str, Any]:
    """Create a product collection.

    Args:
        collection_id: Unique ID for this collection.
        headline: Collection headline (max 150 chars).
        link: URL to the collection landing page.
        image_link: URL to the hero image.
        featured_product_ids: List of offer IDs to feature.
        language: BCP 47 language code.
    """
    body: Dict[str, Any] = {
        "id": collection_id,
        "language": language,
        "headline": [headline],
        "link": link,
        "imageLink": [image_link],
    }
    if featured_product_ids:
        body["featuredProduct"] = [{"offerId": oid} for oid in featured_product_ids]
    path = f"{account_name()}/collections"
    return _collections_http_request("POST", path, body)
