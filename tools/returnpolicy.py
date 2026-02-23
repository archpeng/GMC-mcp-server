"""Return policy tools — manage online return policies in GMC."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from tools._common import mcp, _get_service, _merchant_id


@mcp.tool()
def list_return_policies() -> Dict[str, Any]:
    """List all online return policies configured in GMC."""
    svc = _get_service()
    resp = svc.returnpolicyonline().list(merchantId=_merchant_id()).execute()
    return {
        "returnPolicies": resp.get("returnPolicies", []),
        "totalReturned": len(resp.get("returnPolicies", [])),
    }


@mcp.tool()
def get_return_policy(return_policy_id: str) -> Dict[str, Any]:
    """Get details of a single return policy.

    Args:
        return_policy_id: Return policy ID from list_return_policies.
    """
    svc = _get_service()
    return svc.returnpolicyonline().get(
        merchantId=_merchant_id(), returnPolicyId=return_policy_id
    ).execute()


@mcp.tool()
def create_return_policy(
    label: str,
    countries: List[str],
    policy_type: str = "NUMBER_OF_DAYS_AFTER_DELIVERY",
    days: int = 30,
    return_method: str = "BY_MAIL",
    return_shipping_fee_type: str = "FREE",
    item_conditions: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """Create a new online return policy in GMC.

    Args:
        label: A label/name for this policy, e.g. '30-day-return-DE'.
        countries: List of ISO 3166-1 alpha-2 country codes, e.g. ['DE', 'AT', 'CH'].
        policy_type: 'NUMBER_OF_DAYS_AFTER_DELIVERY', 'NO_RETURNS', or 'LIFETIME_RETURNS'.
        days: Number of days allowed for return (when policy_type is NUMBER_OF_DAYS_AFTER_DELIVERY).
        return_method: 'BY_MAIL', 'IN_STORE', or 'AT_A_KIOSK'.
        return_shipping_fee_type: 'FREE', 'PAID_BY_CUSTOMER', or 'FEE_AMOUNT'.
        item_conditions: Which items qualify, e.g. ['NEW', 'USED']. Defaults to ['NEW'].
    """
    svc = _get_service()
    body: Dict[str, Any] = {
        "label": label,
        "countries": countries,
        "policy": {
            "type": policy_type,
            **({"days": days} if policy_type == "NUMBER_OF_DAYS_AFTER_DELIVERY" else {}),
        },
        "returnMethods": [return_method],
        "returnShippingFee": {"type": return_shipping_fee_type},
        "itemConditions": item_conditions or ["NEW"],
    }
    return svc.returnpolicyonline().create(
        merchantId=_merchant_id(), body=body
    ).execute()


@mcp.tool()
def patch_return_policy(return_policy_id: str, patch: Dict[str, Any]) -> Dict[str, Any]:
    """Partially update an existing return policy.

    Args:
        return_policy_id: Return policy ID.
        patch: Dict of fields to update (partial update — only specified fields change).
    """
    svc = _get_service()
    return svc.returnpolicyonline().patch(
        merchantId=_merchant_id(),
        returnPolicyId=return_policy_id,
        body=patch,
    ).execute()


@mcp.tool()
def delete_return_policy(return_policy_id: str) -> Dict[str, Any]:
    """Delete a return policy from GMC.

    Args:
        return_policy_id: Return policy ID.
    """
    svc = _get_service()
    svc.returnpolicyonline().delete(
        merchantId=_merchant_id(), returnPolicyId=return_policy_id
    ).execute()
    return {"deleted": True, "returnPolicyId": return_policy_id}
