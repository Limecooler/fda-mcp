"""FastMCP server setup and tool/resource registration."""

from mcp.server.fastmcp import FastMCP

SERVER_INSTRUCTIONS = """
FDA MCP provides access to all 21 OpenFDA API endpoints plus FDA decision documents.

WORKFLOW:
1. If unsure which fields to search, call list_searchable_fields first.
2. Use search_fda to find individual records. Use count_records for aggregation/statistics.
3. For device regulatory documents (510k summaries, PMA approvals), use get_decision_document.

QUERY SYNTAX (for the "search" parameter):
- AND: field1:value1+AND+field2:value2
- OR (space = OR): field1:value1+field2:value2
- Phrases: field:"exact phrase"
- Wildcards (trailing only, min 2 chars): field:asp*
- Date ranges: field:[20200101+TO+20231231]
- Existence: _exists_:field
- Exact match (required for count_field): field.exact

COMMON MISTAKES:
- String values MUST be quoted: brand_name:"ASPIRIN" not brand_name:ASPIRIN
- Use + not spaces in queries: value1+AND+value2
- The .exact suffix is REQUIRED on count_field for text fields
- Field names are nested with dots: patient.drug.openfda.brand_name
- Dates are YYYYMMDD format, not ISO-8601

QUERY RECIPES (natural language → API query):
- De Novo grants: dataset=device_510k, search='decision_code:"DENG"'
- De Novos by division: add advisory_committee code (DE=Dental, CV=Cardiovascular, etc.)
- De Novo classifications: dataset=device_classification, search='submission_type_id:6'
- 510(k) clearances only: dataset=device_510k, search='decision_code:"SESE"'
- Class III devices: dataset=device_classification, search='device_class:3'
- PMA approvals: dataset=device_pma, search='decision_code:"APPR"'
- Drug recalls by severity: dataset=drug_recalls, search='classification:"Class I"'
- Recall status: search='status:"Ongoing"' (values: Ongoing, Terminated, Completed)
- Adverse events by drug: dataset=drug_adverse_events, search='patient.drug.openfda.brand_name:"DRUGNAME"'
"""

mcp = FastMCP("fda-mcp", instructions=SERVER_INSTRUCTIONS)

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
