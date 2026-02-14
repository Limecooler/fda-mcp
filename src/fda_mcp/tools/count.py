"""count_records tool — aggregation queries on any of the 21 endpoints."""

from fda_mcp.server import mcp
from fda_mcp.openfda.client import openfda_client
from fda_mcp.openfda.endpoints import OpenFDAEndpoint
from fda_mcp.openfda.summarizer import summarize_count_response


@mcp.tool()
async def count_records(
    endpoint: str,
    count_field: str,
    search: str | None = None,
    limit: int = 10,
) -> str:
    """Count/aggregate records by field across any OpenFDA endpoint.
    Returns top values with counts, percentages, and a narrative summary.

    Args:
        endpoint: One of the 21 OpenFDA endpoints (e.g., "drug/event", "device/510k").
            Use list_searchable_fields or fda://reference/endpoints for the full list.
        count_field: Field to aggregate on. Use .exact suffix for exact matching
            (e.g., "patient.reaction.reactionmeddrapt.exact").
        search: Optional search filter to narrow records before counting.
        limit: Number of top values to return (default 10, max 1000).

    Example:
        endpoint="drug/event", count_field="patient.reaction.reactionmeddrapt.exact",
        search='patient.drug.openfda.brand_name:"ASPIRIN"', limit=10
    """
    # Validate endpoint
    valid_paths = {ep.value for ep in OpenFDAEndpoint}
    if endpoint not in valid_paths:
        from mcp.server.fastmcp.exceptions import ToolError

        raise ToolError(
            f"Unknown endpoint '{endpoint}'. "
            f"Valid endpoints: {', '.join(sorted(valid_paths))}"
        )

    result = await openfda_client.query(
        endpoint=endpoint,
        search=search,
        count=count_field,
        limit=min(limit, 1000),
    )
    return summarize_count_response(result)
