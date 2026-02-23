"""Account, datafeed, and program tools — expanded P0 + P1 coverage."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from tools._common import mcp, _get_service, _merchant_id


# ---------------------------------------------------------------------------
# Account info & status
# ---------------------------------------------------------------------------

@mcp.tool()
def get_account_info() -> Dict[str, Any]:
    """Get basic information about the GMC merchant account (name, website, etc.)."""
    svc = _get_service()
    return svc.accounts().get(
        merchantId=_merchant_id(), accountId=_merchant_id()
    ).execute()


@mcp.tool()
def get_account_status() -> Dict[str, Any]:
    """Get the overall GMC account status — shows suspensions, Misrepresentation issues, etc.

    Returns:
        Dict with accountLevelIssues list, websiteClaimed flag, and products summary.
    """
    svc = _get_service()
    resp = svc.accountstatuses().get(
        merchantId=_merchant_id(), accountId=_merchant_id()
    ).execute()
    issues = [
        {
            "id": i.get("id"),
            "title": i.get("title"),
            "severity": i.get("severity"),
            "country": i.get("country"),
            "documentation": i.get("documentation"),
        }
        for i in resp.get("accountLevelIssues", [])
    ]
    return {
        "accountId": resp.get("accountId"),
        "websiteClaimed": resp.get("websiteClaimed"),
        "hasMca": resp.get("hasMca"),
        "hasCriticalIssue": any(i.get("severity") == "critical" for i in issues),
        "accountLevelIssues": issues,
        "products": resp.get("products", []),
    }


@mcp.tool()
def get_account_tax() -> Dict[str, Any]:
    """Get tax settings for the GMC merchant account."""
    svc = _get_service()
    return svc.accounttax().get(
        merchantId=_merchant_id(), accountId=_merchant_id()
    ).execute()


# ---------------------------------------------------------------------------
# Datafeeds
# ---------------------------------------------------------------------------

@mcp.tool()
def list_datafeeds() -> Dict[str, Any]:
    """List all configured product data feeds (feed sources)."""
    svc = _get_service()
    resp = svc.datafeeds().list(merchantId=_merchant_id()).execute()
    feeds = [
        {
            "id": f.get("id"),
            "name": f.get("name"),
            "fileName": f.get("fileName"),
            "contentType": f.get("contentType"),
            "fetchSchedule": f.get("fetchSchedule"),
            "targets": f.get("targets", []),
        }
        for f in resp.get("resources", [])
    ]
    return {"datafeeds": feeds, "totalReturned": len(feeds)}


@mcp.tool()
def get_datafeed_status(datafeed_id: str) -> Dict[str, Any]:
    """Get the processing status and errors for a specific data feed.

    Args:
        datafeed_id: Numeric datafeed ID (from list_datafeeds).
    """
    svc = _get_service()
    return svc.datafeedstatuses().get(
        merchantId=_merchant_id(), datafeedId=datafeed_id
    ).execute()


@mcp.tool()
def list_datafeed_statuses() -> Dict[str, Any]:
    """List processing statuses of all data feeds — shows errors and item counts."""
    svc = _get_service()
    resp = svc.datafeedstatuses().list(merchantId=_merchant_id()).execute()
    return {
        "datafeedStatuses": resp.get("resources", []),
        "totalReturned": len(resp.get("resources", [])),
    }


@mcp.tool()
def trigger_datafeed_fetch(datafeed_id: str) -> Dict[str, Any]:
    """Trigger an immediate manual fetch/refresh of a data feed.

    Args:
        datafeed_id: Numeric datafeed ID.
    """
    svc = _get_service()
    return svc.datafeeds().fetchnow(
        merchantId=_merchant_id(), datafeedId=datafeed_id
    ).execute()


# ---------------------------------------------------------------------------
# Shopping Ads Program (for GMC review / re-approval)
# ---------------------------------------------------------------------------

@mcp.tool()
def get_shopping_ads_program() -> Dict[str, Any]:
    """Get status of the Shopping Ads program for this account (approved/disapproved/pending)."""
    svc = _get_service()
    return svc.shoppingadsprogram().get(merchantId=_merchant_id()).execute()


@mcp.tool()
def request_shopping_ads_review(region_code: str = "DE") -> Dict[str, Any]:
    """Request a re-review of the Shopping Ads program after fixing policy violations.

    ⚠️ This submits a REAL review request to Google. Only call after fixing issues.

    Args:
        region_code: ISO 3166-1 alpha-2 country code, e.g. 'DE', 'AT', 'CH', 'US'.
    """
    svc = _get_service()
    return svc.shoppingadsprogram().requestreview(
        merchantId=_merchant_id(),
        body={"regionCode": region_code},
    ).execute()


# ---------------------------------------------------------------------------
# Free Listings Program
# ---------------------------------------------------------------------------

@mcp.tool()
def get_free_listings_program() -> Dict[str, Any]:
    """Get status of the Free Listings (unpaid Shopping) program for this account."""
    svc = _get_service()
    return svc.freelistingsprogram().get(merchantId=_merchant_id()).execute()


@mcp.tool()
def request_free_listings_review(region_code: str = "DE") -> Dict[str, Any]:
    """Request a re-review of the Free Listings program.

    Args:
        region_code: ISO 3166-1 alpha-2 country code.
    """
    svc = _get_service()
    return svc.freelistingsprogram().requestreview(
        merchantId=_merchant_id(),
        body={"regionCode": region_code},
    ).execute()


# ---------------------------------------------------------------------------
# Quotas
# ---------------------------------------------------------------------------

@mcp.tool()
def list_api_quotas() -> Dict[str, Any]:
    """List API quota usage for this merchant account — useful for monitoring rate limits."""
    svc = _get_service()
    resp = svc.quotas().list(merchantId=_merchant_id()).execute()
    return {
        "quotas": resp.get("resources", []),
        "totalReturned": len(resp.get("resources", [])),
    }
