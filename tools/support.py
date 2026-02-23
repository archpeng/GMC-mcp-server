"""Merchant Support tools — render issues and trigger support actions."""

from __future__ import annotations

from typing import Any, Dict, Optional

from tools._common import mcp, _get_service, _merchant_id


@mcp.tool()
def render_account_issues(language_code: str = "de") -> Dict[str, Any]:
    """Get a human-readable list of account-level issues with fix suggestions.

    This endpoint surfaces the same issues shown in the GMC UI, including
    policy violations like Misrepresentation, with actionable resolution steps.

    Args:
        language_code: BCP 47 language code for the response, e.g. 'de', 'en'.
    """
    svc = _get_service()
    return svc.merchantsupport().renderaccountissues(
        merchantId=_merchant_id(),
        body={},
        languageCode=language_code,
    ).execute()


@mcp.tool()
def render_product_issues(product_id: str, language_code: str = "de") -> Dict[str, Any]:
    """Get a human-readable list of issues for a single product with fix suggestions.

    Args:
        product_id: Full REST product ID, e.g. 'online:de:DE:SKU123'.
        language_code: BCP 47 language code for the response.
    """
    svc = _get_service()
    return svc.merchantsupport().renderproductissues(
        merchantId=_merchant_id(),
        productId=product_id,
        body={},
        languageCode=language_code,
    ).execute()


@mcp.tool()
def trigger_support_action(action_id: str, action_context: Optional[Dict] = None) -> Dict[str, Any]:
    """Trigger a predefined support action (e.g. appeal or verification step).

    ⚠️ This triggers a REAL action on your GMC account.
    Get available action_ids from render_account_issues() → actions[].actionId.

    Args:
        action_id: The action ID returned by render_account_issues, e.g. 'verify-identity'.
        action_context: Optional context dict required by some actions.
    """
    svc = _get_service()
    body: Dict[str, Any] = {"actionId": action_id}
    if action_context:
        body["actionContext"] = action_context
    return svc.merchantsupport().triggeraction(
        merchantId=_merchant_id(), body=body
    ).execute()
