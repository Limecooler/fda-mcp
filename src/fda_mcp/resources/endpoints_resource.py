"""Endpoints reference resource — list of all 21 OpenFDA endpoints."""

from fda_mcp.server import mcp
from fda_mcp.openfda.endpoints import OpenFDAEndpoint


@mcp.resource("fda://reference/endpoints")
async def get_endpoints() -> str:
    """List of all 21 OpenFDA API endpoints with descriptions."""
    lines = ["# OpenFDA API Endpoints\n"]
    current_category = None

    for ep in OpenFDAEndpoint:
        if ep.category != current_category:
            current_category = ep.category
            lines.append(f"\n## {current_category.title()}\n")
        lines.append(f"- **{ep.value}**: {ep.description}")

    return "\n".join(lines)
