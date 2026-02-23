# GMC MCP Server

Google Merchant Center MCP Server — **34 tools** across **9 modules**, built on Google Content API v2.1.

## Quick Start

```bash
# 1. Auth — Service Account (recommended)
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json

# 2. Install
cp .env.example .env   # fill in GMC_MERCHANT_ID
bash bootstrap.sh

# 3. Run
bash run.sh
```

## Tool Reference (34 tools)

### 🔐 Account & Programs (`account.py`)
| Tool | Description |
|---|---|
| `get_account_info` | Basic account info |
| `get_account_status` | Account suspension / Misrepresentation issues |
| `get_account_tax` | Tax settings |
| `list_datafeeds` | List all data feeds |
| `get_datafeed_status` | Feed health check (errors, item counts) |
| `list_datafeed_statuses` | All feeds health check |
| `trigger_datafeed_fetch` | ⚡ Manually trigger a feed refresh |
| `get_shopping_ads_program` | Shopping Ads program status |
| `request_shopping_ads_review` | ⚠️ Submit re-review request to Google |
| `get_free_listings_program` | Free Listings program status |
| `request_free_listings_review` | Submit Free Listings re-review |
| `list_api_quotas` | API quota usage |

### 📦 Products (`products.py`)
| Tool | Description |
|---|---|
| `list_products` | List products (paginated) |
| `get_product` | Get single product details |
| `insert_product` | Create / replace a product |
| `update_product` | Partially update a product (PATCH) |
| `delete_product` | Delete a product |
| `list_product_statuses` | Approval status + issues for all products |
| `get_product_status` | Approval status for single product |
| `count_products_by_status` | Summary: approved / disapproved / pending counts |

### 🛠️ Merchant Support (`support.py`)
| Tool | Description |
|---|---|
| `render_account_issues` | Human-readable account issues + fix steps |
| `render_product_issues` | Human-readable product issues + fix steps |
| `trigger_support_action` | ⚠️ Trigger a GMC support action (e.g. appeal) |

### 📊 Reports (`reports.py`)
| Tool | Description |
|---|---|
| `reports_search` | MQL query (clicks, impressions, price competitiveness…) |
| `get_product_performance` | Convenience: clicks/impressions by date range |

### 🗺️ Inventory (`inventory.py`)
| Tool | Description |
|---|---|
| `insert_regional_inventory` | Set regional price/availability overrides |
| `insert_local_inventory` | Update in-store inventory |

### 🏷️ Promotions (`promotions.py`)
| Tool | Description |
|---|---|
| `list_promotions` | List promotions |
| `get_promotion` | Get promotion details |
| `create_promotion` | Create a discount promotion |

### 🚚 Shipping (`shipping.py`)
| Tool | Description |
|---|---|
| `get_shipping_settings` | Get shipping services and rates |
| `update_shipping_settings` | Update shipping configuration |
| `get_supported_carriers` | List supported carriers |
| `get_supported_holidays` | List supported holiday cutoff dates |

### 🔄 Return Policy (`returnpolicy.py`)
| Tool | Description |
|---|---|
| `list_return_policies` | List all return policies |
| `get_return_policy` | Get policy details |
| `create_return_policy` | Create a new return policy |
| `patch_return_policy` | Update a return policy |
| `delete_return_policy` | Delete a return policy |

### 🗂️ Collections (`collections.py`)
| Tool | Description |
|---|---|
| `list_collections` | List product collections |
| `get_collection` | Get collection details |
| `get_collection_status` | Get collection approval status |
| `create_collection` | Create a new collection |

### 💡 Recommendations (`recommendations.py`)
| Tool | Description |
|---|---|
| `get_recommendations` | Get GMC optimization recommendations |

## Claude / Cursor Config

Add to `mcp_config.json`:
```json
{
  "mcpServers": {
    "gmc": {
      "command": "/absolute/path/to/GMC-mcp-server/run.sh"
    }
  }
}
```

## Auth Notes

| Method | Setup |
|---|---|
| Service Account JSON | `export GOOGLE_APPLICATION_CREDENTIALS=/path/sa.json` → add SA email as Admin in GMC |
| Local dev | `gcloud auth application-default login --scopes=https://www.googleapis.com/auth/content` |

No Developer Token required. No Google approval needed. Self-serve via Google Cloud Console.
