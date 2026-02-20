"""count_records tool — aggregation queries on any of the 21 endpoints."""

from fda_mcp.server import mcp
from fda_mcp.openfda.client import openfda_client
from fda_mcp.openfda.endpoints import OpenFDAEndpoint
from fda_mcp.openfda.summarizer import summarize_count_response
from fda_mcp.tools._helpers import clamp_limit


@mcp.tool()
async def count_records(
    endpoint: str,
    count_field: str,
    search: str | None = None,
    limit: int = 10,
) -> str:
    """Count/aggregate records by field across any OpenFDA endpoint.
    Returns top values with counts, percentages, and a narrative summary.

    When to use: Getting statistics, distributions, or "top N" lists.
    For individual records, use search_fda instead.

    Args:
        endpoint: One of the 21 OpenFDA endpoint paths (e.g., "drug/event",
            "device/510k"). Call list_searchable_fields to see valid endpoints.
        count_field: Field to aggregate on. IMPORTANT: You MUST add .exact
            suffix for text fields (e.g., "patient.reaction.reactionmeddrapt.exact").
            Without .exact, text fields are tokenized and counts will be wrong.
            Numeric and date fields do NOT need .exact.
        search: Optional search filter to narrow records before counting.
        limit: Number of top values to return (default 10, max 1000).

    Examples:
        Top adverse reactions for a drug:
          endpoint="drug/event", count_field="patient.reaction.reactionmeddrapt.exact",
          search='patient.drug.openfda.brand_name:"ASPIRIN"'
        Device recalls by classification:
          endpoint="device/enforcement", count_field="classification.exact"
        Food recall reasons:
          endpoint="food/enforcement", count_field="reason_for_recall.exact", limit=5
    """
    # Validate endpoint
    valid_paths = {ep.value for ep in OpenFDAEndpoint}
    if endpoint not in valid_paths:
        from mcp.server.fastmcp.exceptions import ToolError

        raise ToolError(
            f"Unknown endpoint '{endpoint}'. "
            f"Valid endpoints: {', '.join(sorted(valid_paths))}"
        )

    limit, limit_note = clamp_limit(limit, 1000)

    # Warn if count_field is missing .exact suffix on likely text fields
    exact_warning = None
    if not count_field.endswith(".exact") and not count_field.endswith((".count", ".time")):
        # Numeric-looking fields and known numeric fields don't need .exact
        known_numeric = {"serious", "device_class", "report_year"}
        field_base = count_field.split(".")[-1]
        if field_base not in known_numeric:
            exact_warning = (
                f"[Warning: count_field '{count_field}' may need .exact suffix. "
                f"Without it, text fields are tokenized and counts may be inaccurate. "
                f"Try '{count_field}.exact' if results look wrong.]"
            )

    result = await openfda_client.query(
        endpoint=endpoint,
        search=search,
        count=count_field,
        limit=limit,
    )
    response = summarize_count_response(result)

    # Prepend any warnings/notes
    prefix_parts = []
    if limit_note:
        prefix_parts.append(limit_note)
    if exact_warning:
        prefix_parts.append(exact_warning)
    if prefix_parts:
        response = "\n".join(prefix_parts) + "\n\n" + response

    return response
