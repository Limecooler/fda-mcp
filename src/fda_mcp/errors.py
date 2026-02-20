"""Custom error types for the FDA MCP server."""

from mcp.server.fastmcp.exceptions import ToolError


class OpenFDAError(ToolError):
    """Base error for OpenFDA API failures."""


class RateLimitError(OpenFDAError):
    """API rate limit exceeded."""

    def __init__(self) -> None:
        super().__init__(
            "OpenFDA API rate limit exceeded. "
            "Set OPENFDA_API_KEY for higher limits (240 req/min vs 40). "
            "Retry after a brief pause."
        )


class NotFoundError(OpenFDAError):
    """No results found for the query."""

    def __init__(self, detail: str = "", endpoint: str = "") -> None:
        lines = ["No results found."]
        if detail:
            lines.append(detail)
        lines.append("Troubleshooting:")
        lines.append("- Verify field names with list_searchable_fields")
        lines.append("- Try broader search terms or remove filters")
        lines.append("- Dates must be YYYYMMDD format (not ISO-8601)")
        if endpoint:
            lines.append(f"- Endpoint used: {endpoint}")
        super().__init__(" ".join(lines))


class InvalidSearchError(OpenFDAError):
    """Invalid search syntax."""

    def __init__(self, detail: str = "") -> None:
        lines = ["Invalid search query."]
        if detail:
            lines.append(detail)
        lines.append(
            "Quick reference: "
            'field:"value" for strings, '
            "field:[20200101+TO+20231231] for date ranges, "
            "field1:val1+AND+field2:val2 for AND, "
            "_exists_:field for existence checks."
        )
        lines.append("Use list_searchable_fields to verify field names.")
        super().__init__(" ".join(lines))


class DocumentNotFoundError(ToolError):
    """FDA decision document not found."""

    def __init__(self, url: str) -> None:
        super().__init__(
            f"Document not found at {url}. "
            "Verify the submission number is correct."
        )


class InvalidIdentifierError(ToolError):
    """Invalid FDA submission identifier format."""

    def __init__(self, identifier: str, expected_format: str) -> None:
        super().__init__(
            f"Invalid identifier '{identifier}'. Expected format: {expected_format}"
        )
