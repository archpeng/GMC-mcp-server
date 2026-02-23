"""Return policy tools — new Merchant API (accounts_v1beta)."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from tools._common import mcp, account_name, get_return_policy_client


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
    return_policy_id: str,
    label: str,
    countries: List[str],
    return_window_days: int = 30,
    return_method: str = "BY_MAIL",
    return_shipping_fee_type: str = "FREE",
    item_conditions: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """Create a new online return policy in GMC.

    Args:
        return_policy_id: Unique ID for this policy, e.g. '30-day-return-de'.
        label: Human-readable label.
        countries: List of ISO 3166-1 alpha-2 country codes, e.g. ['DE', 'AT', 'CH'].
        return_window_days: Number of days allowed for return.
        return_method: 'BY_MAIL', 'IN_STORE', or 'AT_A_KIOSK'.
        return_shipping_fee_type: 'FREE', 'PAID_BY_CUSTOMER'.
        item_conditions: e.g. ['NEW', 'USED']. Defaults to ['NEW'].
    """
    client = get_return_policy_client()
    from google.shopping import merchant_accounts_v1beta
    policy = {
        "returnPolicyId": return_policy_id,
        "label": label,
        "countries": countries,
        "policy": {
            "type": "NUMBER_OF_DAYS_AFTER_DELIVERY",
            "days": return_window_days,
        },
        "returnMethods": [return_method],
        "returnShippingFee": {"type": return_shipping_fee_type},
        "itemConditions": item_conditions or ["NEW"],
    }
    request = merchant_accounts_v1beta.CreateOnlineReturnPolicyRequest(
        parent=account_name(),
        online_return_policy=policy,
    )
    result = client.create_online_return_policy(request=request)
    return type(result).to_dict(result)


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
