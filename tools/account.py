"""Account, data source, and program tools — new Merchant API."""

from __future__ import annotations

from typing import Any, Dict, Optional

from tools._common import (
    mcp,
    account_name,
    merchant_id,
    get_accounts_client,
    get_accounts_issues_client,
    get_datasources_client,
    get_programs_client,
)


# ---------------------------------------------------------------------------
# Account info & issues
# ---------------------------------------------------------------------------

@mcp.tool()
def get_account_info() -> Dict[str, Any]:
    """Get basic information about the GMC merchant account."""
    client = get_accounts_client()
    account = client.get_account(name=account_name())
    return type(account).to_dict(account)


@mcp.tool()
def get_account_issues() -> Dict[str, Any]:
    """Get all account-level issues (policy violations, suspensions, Misrepresentation).

    Returns a list of issues with severity, documentation links, and impacted destinations.
    """
    client = get_accounts_issues_client()
    from google.shopping import merchant_accounts_v1beta
    request = merchant_accounts_v1beta.ListAccountIssuesRequest(parent=account_name())
    issues = []
    for issue in client.list_account_issues(request=request):
        d = type(issue).to_dict(issue)
        issues.append(d)
    return {
        "accountName": account_name(),
        "issues": issues,
        "totalIssues": len(issues),
        "hasCriticalIssue": any(
            i.get("severity") in ("CRITICAL", "ERROR") for i in issues
        ),
    }


# ---------------------------------------------------------------------------
# Data Sources (replaces Datafeeds)
# ---------------------------------------------------------------------------

@mcp.tool()
def list_data_sources() -> Dict[str, Any]:
    """List all data sources (previously called datafeeds) for this GMC account."""
    client = get_datasources_client()
    from google.shopping import merchant_datasources_v1
    request = merchant_datasources_v1.ListDataSourcesRequest(parent=account_name())
    response = client.list_data_sources(request=request)
    sources = [type(ds).to_dict(ds) for ds in response.data_sources]
    return {
        "dataSources": sources,
        "totalReturned": len(sources),
    }


@mcp.tool()
def get_data_source(data_source_id: str) -> Dict[str, Any]:
    """Get details of a single data source.

    Args:
        data_source_id: Numeric data source ID.
    """
    client = get_datasources_client()
    from google.shopping import merchant_datasources_v1
    name = f"{account_name()}/dataSources/{data_source_id}"
    request = merchant_datasources_v1.GetDataSourceRequest(name=name)
    ds = client.get_data_source(request=request)
    return type(ds).to_dict(ds)


@mcp.tool()
def fetch_data_source(data_source_id: str) -> Dict[str, Any]:
    """Trigger an immediate manual fetch of a data source.

    Args:
        data_source_id: Numeric data source ID.
    """
    client = get_datasources_client()
    from google.shopping import merchant_datasources_v1
    name = f"{account_name()}/dataSources/{data_source_id}"
    request = merchant_datasources_v1.FetchDataSourceRequest(name=name)
    client.fetch_data_source(request=request)
    return {"triggered": True, "dataSourceName": name}


@mcp.tool()
def get_data_source_file_upload(data_source_id: str) -> Dict[str, Any]:
    """Get the latest file upload status for a data source (errors, item counts).

    Args:
        data_source_id: Numeric data source ID.
    """
    client = get_datasources_client()
    from google.shopping import merchant_datasources_v1
    # latest upload is addressed as: dataSources/{id}/fileUploads/latest
    name = f"{account_name()}/dataSources/{data_source_id}/fileUploads/latest"
    request = merchant_datasources_v1.GetFileUploadRequest(name=name)
    upload = client.get_file_upload(request=request)
    return type(upload).to_dict(upload)


# ---------------------------------------------------------------------------
# Programs (Shopping Ads & Free Listings)
# ---------------------------------------------------------------------------

@mcp.tool()
def list_programs() -> Dict[str, Any]:
    """List all programs (Shopping Ads, Free Listings, etc.) and their participation status."""
    client = get_programs_client()
    from google.shopping import merchant_accounts_v1beta
    request = merchant_accounts_v1beta.ListProgramsRequest(parent=account_name())
    programs = [type(p).to_dict(p) for p in client.list_programs(request=request)]
    return {"programs": programs, "totalReturned": len(programs)}


@mcp.tool()
def get_program(program_id: str) -> Dict[str, Any]:
    """Get the status and requirements of a specific program.

    Args:
        program_id: Program identifier, e.g. 'FREE_LISTINGS', 'SHOPPING_ADS'.
    """
    client = get_programs_client()
    from google.shopping import merchant_accounts_v1beta
    name = f"{account_name()}/programs/{program_id}"
    request = merchant_accounts_v1beta.GetProgramRequest(name=name)
    program = client.get_program(request=request)
    return type(program).to_dict(program)


@mcp.tool()
def enable_program(program_id: str) -> Dict[str, Any]:
    """Enable / request re-review for a program.

    ⚠️ This triggers a real re-review request with Google.
    Only call after resolving policy violations.

    Args:
        program_id: e.g. 'FREE_LISTINGS', 'SHOPPING_ADS'.
    """
    client = get_programs_client()
    from google.shopping import merchant_accounts_v1beta
    name = f"{account_name()}/programs/{program_id}"
    request = merchant_accounts_v1beta.EnableProgramRequest(name=name)
    program = client.enable_program(request=request)
    return type(program).to_dict(program)
