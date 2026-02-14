"""FastMCP server setup and tool/resource registration."""

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("fda-mcp")

# Tool and resource modules are imported here to trigger @mcp.tool()
# and @mcp.resource() decorator registration. The imports must happen
# after `mcp` is defined above.
import fda_mcp.tools.search  # noqa: E402, F401
import fda_mcp.tools.count  # noqa: E402, F401
import fda_mcp.tools.fields  # noqa: E402, F401
import fda_mcp.tools.decision_documents  # noqa: E402, F401
import fda_mcp.resources.query_syntax  # noqa: E402, F401
import fda_mcp.resources.endpoints_resource  # noqa: E402, F401
import fda_mcp.resources.field_definitions  # noqa: E402, F401


def main() -> None:
    """Run the MCP server on stdio transport."""
    mcp.run(transport="stdio")
