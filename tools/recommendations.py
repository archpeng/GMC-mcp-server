"""Recommendations — Merchant API (productstudio / recommendations alpha).

Note: The new Merchant API recommendations endpoint is in alpha and may change.
This module uses direct HTTP REST calls until a stable client is available.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from tools._common import mcp, account_name, _get_credentials


@mcp.tool()
def get_recommendations(
    allowed_tag: Optional[List[str]] = None,
    language_code: str = "de",
) -> Dict[str, Any]:
    """Get GMC-generated optimization recommendations (same as GMC Opportunities tab).

    Examples include: missing GTINs, title improvements, price competitiveness.

    Args:
        allowed_tag: Filter by recommendation type tags. None returns all types.
        language_code: BCP 47 language code for recommendation text.
    """
    import google.auth.transport.requests
    import urllib.request
    import urllib.parse
    import json

    credentials = _get_credentials()
    auth_req = google.auth.transport.requests.Request()
    credentials.refresh(auth_req)

    params: Dict[str, Any] = {"languageCode": language_code}
    if allowed_tag:
        params["allowedTag"] = allowed_tag

    query_string = urllib.parse.urlencode(params, doseq=True)
    url = (
        f"https://merchantapi.googleapis.com/recommendations/v1beta/"
        f"{account_name()}/recommendations:generate?{query_string}"
    )
    req = urllib.request.Request(
        url,
        headers={"Authorization": f"Bearer {credentials.token}"},
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())
