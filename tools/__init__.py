"""Register all GMC MCP tools — new Merchant API architecture."""

from tools._common import mcp  # noqa: F401

# --- P0: Core ---
from tools.account import (  # noqa: F401
    get_account_info,
    get_account_issues,
    list_data_sources,
    get_data_source,
    fetch_data_source,
    get_data_source_file_upload,
    list_programs,
    get_program,
    enable_program,
)
from tools.products import (  # noqa: F401
    list_products,
    get_product,
    insert_product_input,
    delete_product_input,
    count_products_by_status,
)
from tools.support import (  # noqa: F401
    render_account_issues,
    render_product_issues,
    trigger_issue_action,
)
from tools.reports import (  # noqa: F401
    reports_search,
    get_product_performance,
)

# --- P1: Operations ---
from tools.inventory import (  # noqa: F401
    insert_local_inventory,
    insert_regional_inventory,
)
from tools.promotions import (  # noqa: F401
    list_promotions,
    get_promotion,
    create_promotion,
)
from tools.shipping import (  # noqa: F401
    get_shipping_settings,
    update_shipping_settings,
)
from tools.returnpolicy import (  # noqa: F401
    list_return_policies,
    get_return_policy,
    create_return_policy,
    delete_return_policy,
)
from tools.collections import (  # noqa: F401
    list_collections,
    get_collection,
    create_collection,
)
from tools.recommendations import get_recommendations  # noqa: F401
