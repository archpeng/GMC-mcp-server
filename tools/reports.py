"""Reports tool — query GMC performance data using the Merchant Reports API."""

from __future__ import annotations

from typing import Any, Dict, Optional

from tools._common import mcp, _get_service, _merchant_id


@mcp.tool()
def reports_search(
    query: str,
    page_size: int = 1000,
    page_token: Optional[str] = None,
) -> Dict[str, Any]:
    """Query GMC performance reports using the Merchant Query Language (similar to GAQL).

    Available tables: product_performance_view, product_view,
    price_competitiveness_product_view, price_insights_product_view,
    best_sellers_product_cluster_view, best_sellers_brand_view,
    competitive_visibility_competitor_view, competitive_visibility_top_merchant_view.

    Args:
        query: MQL query string. Examples:
            - "SELECT segments.date, metrics.clicks, metrics.impressions
               FROM product_performance_view
               WHERE segments.date BETWEEN '2026-01-01' AND '2026-02-23'"
            - "SELECT product_view.id, product_view.title, product_view.channel_exclusivity
               FROM product_view WHERE product_view.channel = 'ONLINE'"
        page_size: Max rows to return per page (max 1000).
        page_token: Pagination token.

    Returns:
        Dict with 'results' list, 'nextPageToken', and 'totalResultsCount'.
    """
    svc = _get_service()
    body: Dict[str, Any] = {"query": query, "pageSize": min(page_size, 1000)}
    if page_token:
        body["pageToken"] = page_token
    resp = svc.reports().search(merchantId=_merchant_id(), body=body).execute()
    return {
        "results": resp.get("results", []),
        "nextPageToken": resp.get("nextPageToken"),
        "totalResultsCount": resp.get("totalResultsCount"),
    }


@mcp.tool()
def get_product_performance(
    start_date: str = "2026-01-01",
    end_date: str = "2026-02-23",
    limit: int = 100,
) -> Dict[str, Any]:
    """Get click and impression performance for products. Convenience wrapper around reports_search.

    Args:
        start_date: Start date in YYYY-MM-DD format.
        end_date: End date in YYYY-MM-DD format.
        limit: Max rows to return.
    """
    query = f"""
        SELECT
            segments.date,
            segments.program,
            metrics.clicks,
            metrics.impressions,
            metrics.click_through_rate
        FROM product_performance_view
        WHERE segments.date BETWEEN '{start_date}' AND '{end_date}'
        ORDER BY metrics.clicks DESC
        LIMIT {limit}
    """
    return reports_search(query.strip(), page_size=limit)
