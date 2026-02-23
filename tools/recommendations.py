"""Recommendations tools — get GMC optimization suggestions."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from tools._common import mcp, _get_service, _merchant_id


@mcp.tool()
def get_recommendations(
    allowed_tag: Optional[List[str]] = None,
    language_code: str = "de",
) -> Dict[str, Any]:
    """Get GMC-generated optimization recommendations for this account.

    These are the same recommendations shown in the GMC dashboard under
    "Opportunities" — e.g. missing GTINs, better titles, price suggestions.

    Args:
        allowed_tag: Filter recommendations by tag, e.g. ['DIAMONDS', 'TITLE'].
                     Pass None to get all recommendation types.
        language_code: BCP 47 language code for recommendation text.
    """
    svc = _get_service()
    params: Dict[str, Any] = {
        "merchantId": _merchant_id(),
        "languageCode": language_code,
    }
    if allowed_tag:
        params["allowedTag"] = allowed_tag
    return svc.recommendations().generate(**params).execute()
