"""Reports tools — new Merchant API (reports_v1beta)."""

from __future__ import annotations

from typing import Any, Dict, Optional

from tools._common import mcp, account_name, get_reports_client


@mcp.tool()
def reports_search(
    query: str,
    page_size: int = 1000,
    page_token: Optional[str] = None,
) -> Dict[str, Any]:
    """Query GMC performance reports using the Merchant Query Language (MQL).

    Available tables: product_performance_view, product_view,
    price_competitiveness_product_view, best_sellers_product_cluster_view,
    competitive_visibility_competitor_view, non_product_performance_view.

    Args:
        query: MQL query string. Examples:
            "SELECT segments.date, metrics.clicks, metrics.impressions
             FROM product_performance_view
             WHERE segments.date BETWEEN '2026-01-01' AND '2026-02-23'"
        page_size: Max rows (max 1000).
        page_token: Pagination token.
    """
    client = get_reports_client()
    from google.shopping import merchant_reports_v1beta
    request = merchant_reports_v1beta.SearchRequest(
        parent=account_name(),
        query=query,
        page_size=min(page_size, 1000),
        **({"page_token": page_token} if page_token else {}),
    )
    response = client.search(request=request)
    results = [type(r).to_dict(r) for r in response.results]
    return {
        "results": results,
        "totalReturned": len(results),
    }


@mcp.tool()
def get_product_performance(
    start_date: str = "2026-01-01",
    end_date: str = "2026-02-23",
    limit: int = 100,
) -> Dict[str, Any]:
    """Get click and impression performance for products by date range.

    Args:
        start_date: YYYY-MM-DD format.
        end_date: YYYY-MM-DD format.
        limit: Max rows.
    """
    query = (
        f"SELECT segments.date, segments.program, metrics.clicks, "
        f"metrics.impressions, metrics.click_through_rate "
        f"FROM product_performance_view "
        f"WHERE segments.date BETWEEN '{start_date}' AND '{end_date}' "
        f"ORDER BY metrics.clicks DESC "
        f"LIMIT {limit}"
    )
    return reports_search(query, page_size=limit)
