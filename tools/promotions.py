"""Promotions tools — new Merchant API (promotions_v1)."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from tools._common import mcp, account_name, get_promotions_client


@mcp.tool()
def list_promotions() -> Dict[str, Any]:
    """List all promotions for this GMC account."""
    client = get_promotions_client()
    from google.shopping import merchant_promotions_v1
    request = merchant_promotions_v1.ListPromotionsRequest(parent=account_name())
    promotions = [type(p).to_dict(p) for p in client.list_promotions(request=request)]
    return {"promotions": promotions, "totalReturned": len(promotions)}


@mcp.tool()
def get_promotion(promotion_name: str) -> Dict[str, Any]:
    """Get details of a single promotion.

    Args:
        promotion_name: Full resource name, e.g. 'accounts/12345/promotions/promo-id'.
    """
    client = get_promotions_client()
    from google.shopping import merchant_promotions_v1
    request = merchant_promotions_v1.GetPromotionRequest(name=promotion_name)
    promo = client.get_promotion(request=request)
    return type(promo).to_dict(promo)


@mcp.tool()
def create_promotion(
    promotion_id: str,
    content_language: str,
    target_country: str,
    redemption_channel: List[str],
    attributes: Dict[str, Any],
    data_source_id: str,
) -> Dict[str, Any]:
    """Create a new GMC promotion.

    Args:
        promotion_id: Unique ID (alphanumeric + hyphens), e.g. 'summer-sale-10off'.
        content_language: BCP 47 language code, e.g. 'de'.
        target_country: ISO 3166-1 alpha-2 country code, e.g. 'DE'.
        redemption_channel: List of channels: 'ONLINE', 'IN_STORE'.
        attributes: Promotion attributes dict. Required fields:
            - promotionDisplayTimePeriod: {startTime, endTime}
            - promotionEffectiveTimePeriod: {startTime, endTime}
            - offerType: 'NO_CODE' or 'GENERIC_CODE'
            - productApplicability: 'ALL_PRODUCTS' or 'SPECIFIC_PRODUCTS'
            Optional: percentOff, moneyOffAmount, genericRedemptionCode, longTitle.
        data_source_id: Numeric data source ID to link this promotion to.
    """
    client = get_promotions_client()
    from google.shopping import merchant_promotions_v1
    data_source_name = f"{account_name()}/dataSources/{data_source_id}"
    promotion = {
        "promotionId": promotion_id,
        "contentLanguage": content_language,
        "targetCountry": target_country,
        "redemptionChannel": redemption_channel,
        "dataSource": data_source_name,
        "attributes": attributes,
    }
    request = merchant_promotions_v1.InsertPromotionRequest(
        parent=account_name(),
        promotion=promotion,
    )
    result = client.insert_promotion(request=request)
    return type(result).to_dict(result)
