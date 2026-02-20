"""Tests for error handling — API error responses and custom error classes."""

import pytest
import httpx
import respx

from fda_mcp.errors import (
    DocumentNotFoundError,
    InvalidIdentifierError,
    InvalidSearchError,
    NotFoundError,
    OpenFDAError,
    RateLimitError,
)
from fda_mcp.openfda.client import OpenFDAClient

BASE_URL = "https://api.fda.gov"


@pytest.mark.anyio
async def test_404_raises_not_found_error():
    """API 404 response raises NotFoundError with helpful message."""
    with respx.mock(assert_all_called=False) as router:
        router.get(f"{BASE_URL}/drug/event.json").mock(
            return_value=httpx.Response(404, json={"error": {"message": "No matches found!"}})
        )
        client = OpenFDAClient()
        with pytest.raises(NotFoundError) as exc_info:
            await client.query("drug/event", search="nonexistent:value")
        msg = str(exc_info.value)
        assert "No results found" in msg
        assert "list_searchable_fields" in msg
        assert "drug/event" in msg


@pytest.mark.anyio
async def test_429_raises_rate_limit_error():
    """API 429 response raises RateLimitError with retry suggestion and API key mention."""
    with respx.mock(assert_all_called=False) as router:
        router.get(f"{BASE_URL}/drug/event.json").mock(
            return_value=httpx.Response(429, json={"error": {"message": "Rate limit exceeded"}})
        )
        client = OpenFDAClient()
        with pytest.raises(RateLimitError) as exc_info:
            await client.query("drug/event", search="aspirin")
        msg = str(exc_info.value)
        assert "rate limit" in msg.lower()
        assert "Retry" in msg or "retry" in msg
        assert "API_KEY" in msg or "api_key" in msg.lower()


@pytest.mark.anyio
async def test_500_raises_openfda_error():
    """API 500 response raises OpenFDAError with server error message."""
    with respx.mock(assert_all_called=False) as router:
        router.get(f"{BASE_URL}/drug/event.json").mock(
            return_value=httpx.Response(500, text="Internal Server Error")
        )
        client = OpenFDAClient()
        with pytest.raises(OpenFDAError) as exc_info:
            await client.query("drug/event", search="aspirin")
        msg = str(exc_info.value)
        assert "server error" in msg.lower() or "500" in msg


@pytest.mark.anyio
async def test_400_raises_invalid_search_error():
    """API 400 response raises InvalidSearchError with inline syntax help."""
    with respx.mock(assert_all_called=False) as router:
        router.get(f"{BASE_URL}/drug/event.json").mock(
            return_value=httpx.Response(
                400, json={"error": {"message": "Invalid syntax in search parameter"}}
            )
        )
        client = OpenFDAClient()
        with pytest.raises(InvalidSearchError) as exc_info:
            await client.query("drug/event", search="bad[syntax")
        msg = str(exc_info.value)
        assert "Invalid search" in msg
        assert "list_searchable_fields" in msg
        assert "Quick reference" in msg


@pytest.mark.anyio
async def test_timeout_raises_openfda_error():
    """Network timeout raises OpenFDAError with timeout message."""
    with respx.mock(assert_all_called=False) as router:
        router.get(f"{BASE_URL}/drug/event.json").mock(
            side_effect=httpx.TimeoutException("Connection timed out")
        )
        client = OpenFDAClient()
        with pytest.raises(OpenFDAError) as exc_info:
            await client.query("drug/event", search="aspirin")
        msg = str(exc_info.value)
        assert "timed out" in msg.lower() or "timeout" in msg.lower()


@pytest.mark.anyio
async def test_connect_error_raises_openfda_error():
    """Network connection failure raises OpenFDAError."""
    with respx.mock(assert_all_called=False) as router:
        router.get(f"{BASE_URL}/drug/event.json").mock(
            side_effect=httpx.ConnectError("Connection refused")
        )
        client = OpenFDAClient()
        with pytest.raises(OpenFDAError) as exc_info:
            await client.query("drug/event", search="aspirin")
        assert "connect" in str(exc_info.value).lower()


def test_invalid_identifier_error_includes_expected_format():
    """InvalidIdentifierError message includes the expected format."""
    err = InvalidIdentifierError("bad-id", "K######")
    msg = str(err)
    assert "bad-id" in msg
    assert "K######" in msg
    assert "Expected format" in msg


def test_document_not_found_error_includes_url():
    """DocumentNotFoundError message includes the URL."""
    url = "https://www.accessdata.fda.gov/docs/example.pdf"
    err = DocumentNotFoundError(url)
    msg = str(err)
    assert url in msg
    assert "not found" in msg.lower() or "Document not found" in msg


def test_not_found_error_with_detail():
    """NotFoundError includes optional detail string and troubleshooting."""
    err = NotFoundError("Try different terms.")
    msg = str(err)
    assert "No results found" in msg
    assert "Try different terms" in msg
    assert "list_searchable_fields" in msg


def test_not_found_error_without_detail():
    """NotFoundError works without detail."""
    err = NotFoundError()
    msg = str(err)
    assert "No results found" in msg
    assert "list_searchable_fields" in msg


def test_not_found_error_with_endpoint():
    """NotFoundError includes endpoint when provided."""
    err = NotFoundError(endpoint="drug/event")
    msg = str(err)
    assert "drug/event" in msg
    assert "Troubleshooting" in msg


def test_invalid_search_error_includes_inline_syntax():
    """InvalidSearchError includes inline syntax quick reference."""
    err = InvalidSearchError("bad field name")
    msg = str(err)
    assert "Quick reference" in msg
    assert "bad field name" in msg
    assert "list_searchable_fields" in msg


def test_rate_limit_error_message():
    """RateLimitError has a useful default message."""
    err = RateLimitError()
    msg = str(err)
    assert "rate limit" in msg.lower()
    assert "240" in msg or "API_KEY" in msg or "api_key" in msg.lower()
