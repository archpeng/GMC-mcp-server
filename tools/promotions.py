"""Promotions tools — create and list GMC promotions."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from tools._common import mcp, _get_service, _merchant_id


@mcp.tool()
def list_promotions(
    language_code: str = "de",
    country_code: str = "DE",
) -> Dict[str, Any]:
    """List all active promotions for this GMC account.

    Args:
        language_code: BCP 47 language code, e.g. 'de', 'en'.
        country_code: ISO 3166-1 alpha-2 country code, e.g. 'DE'.
    """
    svc = _get_service()
    resp = svc.promotions().list(
        merchantId=_merchant_id(),
        languageCode=language_code,
        countryCode=country_code,
    ).execute()
    return {
        "promotions": resp.get("promotions", []),
        "totalReturned": len(resp.get("promotions", [])),
    }


@mcp.tool()
def get_promotion(promotion_id: str) -> Dict[str, Any]:
    """Get details of a single promotion.

    Args:
        promotion_id: The promotion ID (from list_promotions).
    """
    svc = _get_service()
    return svc.promotions().get(
        merchantId=_merchant_id(), id=promotion_id
    ).execute()


@mcp.tool()
def create_promotion(
    promotion_id: str,
    title: str,
    product_applicability: str,
    offer_type: str,
    redemption_channel: List[str],
    promotion_effective_time_period: Dict[str, str],
    generic_redemption_code: Optional[str] = None,
    long_title: Optional[str] = None,
    percent_off: Optional[int] = None,
    money_off_amount: Optional[Dict[str, str]] = None,
    target_country: str = "DE",
    content_language: str = "de",
) -> Dict[str, Any]:
    """Create a new GMC promotion (discount).

    Args:
        promotion_id: Unique ID for this promotion (alphanumeric + hyphens).
        title: Short title shown in Shopping ads.
        product_applicability: 'ALL_PRODUCTS' or 'SPECIFIC_PRODUCTS'.
        offer_type: 'NO_CODE' or 'GENERIC_CODE'.
        redemption_channel: List of channels, e.g. ['ONLINE'] or ['ONLINE', 'IN_STORE'].
        promotion_effective_time_period: Dict with 'startTime' and 'endTime' (RFC 3339).
        generic_redemption_code: Discount code if offer_type is 'GENERIC_CODE'.
        long_title: Extended description (up to 60 chars).
        percent_off: Discount percentage (e.g. 10 for 10% off).
        money_off_amount: Dict with 'value' and 'currency' for fixed discount.
        target_country: ISO 3166-1 alpha-2 country code.
        content_language: BCP 47 language code.
    """
    svc = _get_service()
    body: Dict[str, Any] = {
        "promotionId": promotion_id,
        "title": title,
        "contentLanguage": content_language,
        "targetCountry": target_country,
        "productApplicability": product_applicability,
        "offerType": offer_type,
        "redemptionChannel": redemption_channel,
        "promotionEffectiveTimePeriod": promotion_effective_time_period,
    }
    if generic_redemption_code:
        body["genericRedemptionCode"] = generic_redemption_code
    if long_title:
        body["longTitle"] = long_title
    if percent_off is not None:
        body["percentOff"] = percent_off
    if money_off_amount:
        body["moneyOffAmount"] = money_off_amount
    return svc.promotions().create(
        merchantId=_merchant_id(), body=body
    ).execute()
