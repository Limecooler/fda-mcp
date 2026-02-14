"""list_searchable_fields tool — field discovery for any endpoint."""

from typing import Literal

from mcp.server.fastmcp.exceptions import ToolError

from fda_mcp.server import mcp
from fda_mcp.openfda.endpoints import OpenFDAEndpoint
from fda_mcp.resources.field_definitions import get_fields


@mcp.tool()
async def list_searchable_fields(
    endpoint: str,
    category: Literal["common", "all"] = "common",
) -> str:
    """List searchable fields for any OpenFDA endpoint.
    Returns field names, types, and descriptions.

    Use category="common" for the most frequently used fields (default).
    Use category="all" for the complete field listing.

    Args:
        endpoint: One of the 21 OpenFDA endpoints (e.g., "drug/event").
        category: "common" for key fields, "all" for complete listing.
    """
    valid_paths = {ep.value for ep in OpenFDAEndpoint}
    if endpoint not in valid_paths:
        raise ToolError(
            f"Unknown endpoint '{endpoint}'. "
            f"Valid endpoints: {', '.join(sorted(valid_paths))}"
        )

    fields = get_fields(endpoint, category)
    if not fields:
        return f"No field definitions available for {endpoint}."

    lines = [f"Searchable fields for {endpoint} ({category}):\n"]
    for name, info in fields.items():
        field_type = info.get("type", "string")
        desc = info.get("description", "")
        lines.append(f"  {name} ({field_type}): {desc}")

    return "\n".join(lines)
