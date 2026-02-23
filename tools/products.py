"""Product tools — new Merchant API (products_v1 + product_inputs_v1)."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from tools._common import (
    mcp,
    account_name,
    get_products_client,
    get_product_inputs_client,
)


@mcp.tool()
def list_products(
    page_size: int = 250,
    page_token: Optional[str] = None,
) -> Dict[str, Any]:
    """List products in GMC (read-only view).

    Args:
        page_size: Max products per page (max 250).
        page_token: Pagination token from a previous call.
    """
    client = get_products_client()
    from google.shopping import merchant_products_v1
    request = merchant_products_v1.ListProductsRequest(
        parent=account_name(),
        page_size=min(page_size, 250),
        **({"page_token": page_token} if page_token else {}),
    )
    response = client.list_products(request=request)
    products = []
    for p in response:
        d = type(p).to_dict(p)
        products.append({
            "name": d.get("name"),
            "productId": d.get("productId"),
            "title": d.get("title"),
            "brand": d.get("brand"),
            "availability": d.get("attributes", {}).get("availability"),
            "price": d.get("attributes", {}).get("price"),
            "link": d.get("attributes", {}).get("link"),
            "imageLink": d.get("attributes", {}).get("imageLink"),
            "channel": d.get("channel"),
            "contentLanguage": d.get("contentLanguage"),
            "feedLabel": d.get("feedLabel"),
            "offerId": d.get("offerId"),
            "productStatus": d.get("productStatus"),
        })
    return {
        "products": products,
        "totalReturned": len(products),
    }


@mcp.tool()
def get_product(product_name: str) -> Dict[str, Any]:
    """Get full details of a single product.

    Args:
        product_name: Full resource name, e.g. 'accounts/12345/products/online~de~DE~SKU-001'.
                      Use list_products to discover product names.
    """
    client = get_products_client()
    from google.shopping import merchant_products_v1
    request = merchant_products_v1.GetProductRequest(name=product_name)
    product = client.get_product(request=request)
    return type(product).to_dict(product)


@mcp.tool()
def insert_product_input(
    data_source_id: str,
    product_input: Dict[str, Any],
) -> Dict[str, Any]:
    """Create or replace a product via the ProductInputs API.

    Args:
        data_source_id: Numeric ID of the primary data source to associate with.
        product_input: Product input resource dict. Required fields:
            offerId, title, description, link, imageLink,
            contentLanguage, feedLabel, channel (ONLINE/LOCAL),
            attributes.availability, attributes.price, attributes.brand.

    Example product_input:
        {
          "offerId": "SKU-001",
          "title": "My Product",
          "description": "Description text",
          "link": "https://example.com/products/my-product",
          "imageLink": "https://cdn.example.com/image.jpg",
          "contentLanguage": "de",
          "feedLabel": "DE",
          "channel": "ONLINE",
          "attributes": {
            "availability": "in_stock",
            "price": {"amountMicros": "4999000000", "currencyCode": "EUR"},
            "brand": "MyBrand",
            "condition": "new"
          }
        }
    """
    client = get_product_inputs_client()
    from google.shopping import merchant_products_v1
    data_source_name = f"{account_name()}/dataSources/{data_source_id}"
    request = merchant_products_v1.InsertProductInputRequest(
        parent=account_name(),
        product_input=product_input,
        data_source=data_source_name,
    )
    result = client.insert_product_input(request=request)
    return type(result).to_dict(result)


@mcp.tool()
def delete_product_input(
    product_input_name: str,
    data_source_id: str,
) -> Dict[str, Any]:
    """Delete a product input from GMC.

    Args:
        product_input_name: Full resource name, e.g.
            'accounts/12345/productInputs/online~de~DE~SKU-001'.
        data_source_id: The data source ID the product belongs to.
    """
    client = get_product_inputs_client()
    from google.shopping import merchant_products_v1
    data_source_name = f"{account_name()}/dataSources/{data_source_id}"
    request = merchant_products_v1.DeleteProductInputRequest(
        name=product_input_name,
        data_source=data_source_name,
    )
    client.delete_product_input(request=request)
    return {"deleted": True, "productInputName": product_input_name}


@mcp.tool()
def count_products_by_status() -> Dict[str, Any]:
    """Summarize product counts by approval status from productStatus embedded field.

    Fetches up to 250 products and tallies statuses from their productStatus field.
    """
    client = get_products_client()
    from google.shopping import merchant_products_v1
    request = merchant_products_v1.ListProductsRequest(
        parent=account_name(), page_size=250
    )
    approved = pending = disapproved = 0
    for p in client.list_products(request=request):
        d = type(p).to_dict(p)
        status = d.get("productStatus", {})
        for ds in status.get("destinationStatuses", []):
            s = ds.get("status", "")
            if s == "APPROVED":
                approved += 1
            elif s == "DISAPPROVED":
                disapproved += 1
            elif s == "PENDING":
                pending += 1
    return {
        "approved": approved,
        "disapproved": disapproved,
        "pending": pending,
        "total": approved + disapproved + pending,
    }
