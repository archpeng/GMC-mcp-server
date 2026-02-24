"""Shared client factories for the new Google Merchant API.

Each sub-service has its own typed gRPC-backed client.
All resources are addressed as: accounts/{merchant_id}/...
"""

from __future__ import annotations

import os
from typing import Any

import google.auth

_MERCHANT_SCOPE = "https://www.googleapis.com/auth/content"


# ---------------------------------------------------------------------------
# Config helpers
# ---------------------------------------------------------------------------

def _require_env(name: str) -> str:
    val = os.environ.get(name, "").strip()
    if not val:
        raise RuntimeError(f"Environment variable {name!r} is not set. "
                           f"Copy .env.example to .env and fill it in.")
    return val


def merchant_id() -> str:
    """Return the GMC numeric Merchant ID from env."""
    return _require_env("GMC_MERCHANT_ID")


def account_name() -> str:
    """Return the fully-qualified account resource name accounts/{id}."""
    return f"accounts/{merchant_id()}"


def _get_credentials() -> Any:
    credentials, _ = google.auth.default(scopes=[_MERCHANT_SCOPE])
    return credentials


def _get_credentials_and_token() -> str:
    """Return a fresh OAuth2 Bearer token string for REST requests."""
    import google.auth.transport.requests
    from google.oauth2 import service_account
    import os
    sa_file = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    if sa_file:
        creds = service_account.Credentials.from_service_account_file(
            sa_file, scopes=[_MERCHANT_SCOPE]
        )
    else:
        creds, _ = google.auth.default(scopes=[_MERCHANT_SCOPE])
    creds.refresh(google.auth.transport.requests.Request())
    return creds.token


# ---------------------------------------------------------------------------
# Per-sub-service client singletons
# ---------------------------------------------------------------------------

_clients: dict[str, Any] = {}


def _get_client(key: str, factory_fn) -> Any:
    if key not in _clients:
        _clients[key] = factory_fn(_get_credentials())
    return _clients[key]


def get_products_client():
    """Products read client (ProductsServiceClient)."""
    from google.shopping import merchant_products_v1
    return _get_client(
        "products",
        lambda creds: merchant_products_v1.ProductsServiceClient(credentials=creds),
    )


def get_product_inputs_client():
    """Product inputs write client (ProductInputsServiceClient)."""
    from google.shopping import merchant_products_v1
    return _get_client(
        "product_inputs",
        lambda creds: merchant_products_v1.ProductInputsServiceClient(credentials=creds),
    )


def get_datasources_client():
    """Data sources client (DataSourcesServiceClient)."""
    from google.shopping import merchant_datasources_v1
    return _get_client(
        "datasources",
        lambda creds: merchant_datasources_v1.DataSourcesServiceClient(credentials=creds),
    )


def get_reports_client():
    """Reports client (ReportServiceClient)."""
    from google.shopping import merchant_reports_v1beta
    return _get_client(
        "reports",
        lambda creds: merchant_reports_v1beta.ReportServiceClient(credentials=creds),
    )


def get_accounts_client():
    """Accounts client (AccountsServiceClient)."""
    from google.shopping import merchant_accounts_v1beta
    return _get_client(
        "accounts",
        lambda creds: merchant_accounts_v1beta.AccountsServiceClient(credentials=creds),
    )


def get_accounts_issues_client():
    """Account issues client (AccountIssueServiceClient)."""
    from google.shopping import merchant_accounts_v1beta
    return _get_client(
        "account_issues",
        lambda creds: merchant_accounts_v1beta.AccountIssueServiceClient(credentials=creds),
    )


def get_programs_client():
    """Programs client (ProgramsServiceClient) — Shopping Ads, Free Listings."""
    from google.shopping import merchant_accounts_v1beta
    return _get_client(
        "programs",
        lambda creds: merchant_accounts_v1beta.ProgramsServiceClient(credentials=creds),
    )


def get_shipping_client():
    """Shipping settings client."""
    from google.shopping import merchant_accounts_v1beta
    return _get_client(
        "shipping",
        lambda creds: merchant_accounts_v1beta.ShippingSettingsServiceClient(credentials=creds),
    )


def get_return_policy_client():
    """Online return policy client."""
    from google.shopping import merchant_accounts_v1beta
    return _get_client(
        "return_policy",
        lambda creds: merchant_accounts_v1beta.OnlineReturnPolicyServiceClient(credentials=creds),
    )


def get_local_inventory_client():
    """Local inventory client."""
    from google.shopping import merchant_inventories_v1beta
    return _get_client(
        "local_inventory",
        lambda creds: merchant_inventories_v1beta.LocalInventoryServiceClient(credentials=creds),
    )


def get_regional_inventory_client():
    """Regional inventory client."""
    from google.shopping import merchant_inventories_v1beta
    return _get_client(
        "regional_inventory",
        lambda creds: merchant_inventories_v1beta.RegionalInventoryServiceClient(credentials=creds),
    )


def get_promotions_client():
    """Promotions client."""
    from google.shopping import merchant_promotions_v1
    return _get_client(
        "promotions",
        lambda creds: merchant_promotions_v1.PromotionsServiceClient(credentials=creds),
    )


def get_issueresolution_client():
    """Issue resolution client (render issues + trigger actions)."""
    from google.shopping import merchant_issueresolution_v1beta
    return _get_client(
        "issueresolution",
        lambda creds: merchant_issueresolution_v1beta.IssueResolutionServiceClient(credentials=creds),
    )


# ---------------------------------------------------------------------------
# MCP instance (shared across all tool modules)
# ---------------------------------------------------------------------------

from mcp.server.fastmcp import FastMCP  # noqa: E402

mcp = FastMCP("Google Merchant Center")
