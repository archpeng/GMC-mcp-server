"""Support / issue resolution tools — new Merchant API."""

from __future__ import annotations

from typing import Any, Dict

from tools._common import mcp, account_name, get_issueresolution_client


@mcp.tool()
def render_account_issues(language_code: str = "de") -> Dict[str, Any]:
    """Get human-readable account issues with actionable fix steps.

    This surfaces the same issues as the GMC UI Policy tab, including
    Misrepresentation, with step-by-step resolution instructions.

    Args:
        language_code: BCP 47 language code, e.g. 'de', 'en'.
    """
    client = get_issueresolution_client()
    from google.shopping import merchant_issueresolution_v1beta
    request = merchant_issueresolution_v1beta.RenderAccountIssuesRequest(
        parent=account_name(),
        language_code=language_code,
    )
    response = client.render_account_issues(request=request)
    return type(response).to_dict(response)


@mcp.tool()
def render_product_issues(product_name: str, language_code: str = "de") -> Dict[str, Any]:
    """Get human-readable issues for a single product with fix steps.

    Args:
        product_name: Full resource name, e.g. 'accounts/12345/products/online~de~DE~SKU'.
        language_code: BCP 47 language code.
    """
    client = get_issueresolution_client()
    from google.shopping import merchant_issueresolution_v1beta
    request = merchant_issueresolution_v1beta.RenderProductIssuesRequest(
        parent=product_name,
        language_code=language_code,
    )
    response = client.render_product_issues(request=request)
    return type(response).to_dict(response)


@mcp.tool()
def trigger_issue_action(action_id: str) -> Dict[str, Any]:
    """Trigger a predefined issue resolution action (e.g. appeal, verification).

    ⚠️ This triggers a real action on your GMC account.
    Discover available action_ids from render_account_issues() response.

    Args:
        action_id: Action ID from render_account_issues actions list.
    """
    client = get_issueresolution_client()
    from google.shopping import merchant_issueresolution_v1beta
    request = merchant_issueresolution_v1beta.TriggerActionRequest(
        parent=account_name(),
        action=merchant_issueresolution_v1beta.BuiltInUserAction(action_id=action_id),
    )
    response = client.trigger_action(request=request)
    return type(response).to_dict(response)
