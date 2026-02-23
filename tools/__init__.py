"""Register all GMC MCP tools by importing each module."""

from tools._common import mcp  # noqa: F401

# --- P0: Core ---
from tools.account import (  # noqa: F401
    get_account_info,
    get_account_status,
    get_account_tax,
    list_datafeeds,
    get_datafeed_status,
    list_datafeed_statuses,
    trigger_datafeed_fetch,
    get_shopping_ads_program,
    request_shopping_ads_review,
    get_free_listings_program,
    request_free_listings_review,
    list_api_quotas,
)
from tools.products import (  # noqa: F401
    list_products,
    get_product,
    insert_product,
    update_product,
    delete_product,
    list_product_statuses,
    get_product_status,
    count_products_by_status,
)
from tools.support import (  # noqa: F401
    render_account_issues,
    render_product_issues,
    trigger_support_action,
)
from tools.reports import (  # noqa: F401
    reports_search,
    get_product_performance,
)

# --- P1: Operations ---
from tools.inventory import (  # noqa: F401
    insert_regional_inventory,
    insert_local_inventory,
)
from tools.promotions import (  # noqa: F401
    list_promotions,
    get_promotion,
    create_promotion,
)
from tools.shipping import (  # noqa: F401
    get_shipping_settings,
    update_shipping_settings,
    get_supported_carriers,
    get_supported_holidays,
)
from tools.returnpolicy import (  # noqa: F401
    list_return_policies,
    get_return_policy,
    create_return_policy,
    patch_return_policy,
    delete_return_policy,
)
from tools.collections import (  # noqa: F401
    list_collections,
    get_collection,
    get_collection_status,
    create_collection,
)
from tools.recommendations import get_recommendations  # noqa: F401
