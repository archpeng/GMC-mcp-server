"""Return policy tools — new Merchant API (accounts_v1beta)."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from tools._common import mcp, account_name, get_return_policy_client, _get_credentials_and_token



@mcp.tool()
def list_return_policies() -> Dict[str, Any]:
    """List all online return policies configured in GMC."""
    client = get_return_policy_client()
    from google.shopping import merchant_accounts_v1beta
    request = merchant_accounts_v1beta.ListOnlineReturnPoliciesRequest(
        parent=account_name()
    )
    policies = [type(p).to_dict(p) for p in client.list_online_return_policies(request=request)]
    return {"returnPolicies": policies, "totalReturned": len(policies)}


@mcp.tool()
def get_return_policy(return_policy_name: str) -> Dict[str, Any]:
    """Get details of a single return policy.

    Args:
        return_policy_name: Full resource name, e.g. 'accounts/12345/onlineReturnPolicies/policy-id'.
    """
    client = get_return_policy_client()
    from google.shopping import merchant_accounts_v1beta
    request = merchant_accounts_v1beta.GetOnlineReturnPolicyRequest(name=return_policy_name)
    policy = client.get_online_return_policy(request=request)
    return type(policy).to_dict(policy)


@mcp.tool()
def create_return_policy(
    label: str,
    countries: List[str],
    return_window_days: int = 30,
    return_method: str = "BY_MAIL",
    return_shipping_fee_type: str = "CUSTOMER_PAYING_ACTUAL_FEE",
    return_label_source: str = "CUSTOMER_RESPONSIBILITY",
    process_refund_days: int = 10,
    return_policy_uri: str = "",
    item_conditions: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """Create a new online return policy in GMC via Merchant API v1beta REST.

    Args:
        label: Human-readable label, e.g. 'Loopsorbit Return Policy (EU)'.
        countries: ISO 3166-1 alpha-2 codes, e.g. ['DE', 'AT', 'CH'].
        return_window_days: Days from delivery allowed for return (default 30).
        return_method: 'BY_MAIL', 'IN_STORE', or 'AT_A_KIOSK'.
        return_shipping_fee_type: 'CUSTOMER_PAYING_ACTUAL_FEE', 'FIXED', or 'FREE'.
        return_label_source: 'CUSTOMER_RESPONSIBILITY', 'DOWNLOAD_AND_PRINT', or 'IN_THE_PACKAGE'.
        process_refund_days: Business days to process refund after receiving return (default 10).
        return_policy_uri: URL to the return/refund policy page on your store.
        item_conditions: e.g. ['NEW', 'USED']. Defaults to ['NEW'].
    """
    import requests as http
    token = _get_credentials_and_token()
    mid = account_name().split("/")[1]
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    payload: Dict[str, Any] = {
        "label": label,
        "countries": countries,
        "policy": {
            "type": "NUMBER_OF_DAYS_AFTER_DELIVERY",
            "days": return_window_days,
        },
        "returnMethods": [return_method],
        "returnShippingFee": {"type": return_shipping_fee_type},
        "itemConditions": item_conditions or ["NEW"],
        "processRefundDays": process_refund_days,
        "returnLabelSource": return_label_source,
    }
    if return_policy_uri:
        payload["returnPolicyUri"] = return_policy_uri
    r = http.post(
        f"https://merchantapi.googleapis.com/accounts/v1beta/accounts/{mid}/onlineReturnPolicies",
        headers=headers,
        json=payload,
    )
    r.raise_for_status()
    return r.json()


@mcp.tool()
def delete_return_policy(return_policy_name: str) -> Dict[str, Any]:
    """Delete a return policy from GMC.

    Args:
        return_policy_name: Full resource name, e.g. 'accounts/12345/onlineReturnPolicies/id'.
    """
    client = get_return_policy_client()
    from google.shopping import merchant_accounts_v1beta
    request = merchant_accounts_v1beta.DeleteOnlineReturnPolicyRequest(
        name=return_policy_name
    )
    client.delete_online_return_policy(request=request)
    return {"deleted": True, "returnPolicyName": return_policy_name}
