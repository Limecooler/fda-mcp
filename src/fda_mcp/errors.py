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

    def __init__(self, detail: str = "") -> None:
        msg = "No results found."
        if detail:
            msg += f" {detail}"
        super().__init__(msg)


class InvalidSearchError(OpenFDAError):
    """Invalid search syntax."""

    def __init__(self, detail: str = "") -> None:
        msg = "Invalid search query syntax."
        if detail:
            msg += f" {detail}"
        msg += " Use the fda://reference/query-syntax resource for help."
        super().__init__(msg)


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
