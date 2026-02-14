"""Tests for the OpenFDA HTTP client."""

import os

import httpx
import pytest
import respx

from fda_mcp.openfda.client import OpenFDAClient
from fda_mcp.errors import NotFoundError, RateLimitError, InvalidSearchError, OpenFDAError

BASE_URL = "https://api.fda.gov"


@pytest.fixture
def client():
    return OpenFDAClient()


async def test_constructs_correct_url(client):
    with respx.mock:
        route = respx.get(f"{BASE_URL}/drug/event.json").mock(
            return_value=httpx.Response(200, json={"meta": {}, "results": []})
        )
        await client.query(endpoint="drug/event", search="test")
        assert route.called
        request = route.calls[0].request
        assert "search=test" in str(request.url)


async def test_includes_api_key(client, monkeypatch):
    monkeypatch.setenv("OPENFDA_API_KEY", "test-key-123")
    # Recreate client to pick up env var
    from fda_mcp.config import Config
    client._semaphore  # access to verify it exists
    monkeypatch.setattr("fda_mcp.openfda.client.config", Config())

    with respx.mock:
        route = respx.get(f"{BASE_URL}/drug/event.json").mock(
            return_value=httpx.Response(200, json={"meta": {}, "results": []})
        )
        await client.query(endpoint="drug/event", search="test")
        request = route.calls[0].request
        assert "api_key=test-key-123" in str(request.url)


async def test_omits_api_key_when_not_set(client, monkeypatch):
    monkeypatch.delenv("OPENFDA_API_KEY", raising=False)
    from fda_mcp.config import Config
    monkeypatch.setattr("fda_mcp.openfda.client.config", Config())

    with respx.mock:
        route = respx.get(f"{BASE_URL}/drug/event.json").mock(
            return_value=httpx.Response(200, json={"meta": {}, "results": []})
        )
        await client.query(endpoint="drug/event", search="test")
        request = route.calls[0].request
        assert "api_key" not in str(request.url)


async def test_builds_all_query_params(client):
    with respx.mock:
        route = respx.get(f"{BASE_URL}/drug/event.json").mock(
            return_value=httpx.Response(200, json={"meta": {}, "results": []})
        )
        await client.query(
            endpoint="drug/event",
            search="test:value",
            limit=5,
            skip=10,
            sort="receiptdate:desc",
        )
        url_str = str(route.calls[0].request.url)
        assert "search=" in url_str
        assert "limit=5" in url_str
        assert "skip=10" in url_str
        assert "sort=" in url_str


async def test_count_param(client):
    with respx.mock:
        route = respx.get(f"{BASE_URL}/drug/event.json").mock(
            return_value=httpx.Response(200, json={"results": []})
        )
        await client.query(
            endpoint="drug/event",
            count="patient.reaction.reactionmeddrapt.exact",
            limit=10,
        )
        url_str = str(route.calls[0].request.url)
        assert "count=" in url_str


async def test_handles_404(client):
    with respx.mock:
        respx.get(f"{BASE_URL}/drug/event.json").mock(
            return_value=httpx.Response(404, json={})
        )
        with pytest.raises(NotFoundError):
            await client.query(endpoint="drug/event", search="nonexistent")


async def test_handles_429(client):
    with respx.mock:
        respx.get(f"{BASE_URL}/drug/event.json").mock(
            return_value=httpx.Response(429, json={})
        )
        with pytest.raises(RateLimitError):
            await client.query(endpoint="drug/event", search="test")


async def test_handles_400(client):
    with respx.mock:
        respx.get(f"{BASE_URL}/drug/event.json").mock(
            return_value=httpx.Response(
                400,
                json={"error": {"message": "Invalid syntax"}},
            )
        )
        with pytest.raises(InvalidSearchError, match="Invalid syntax"):
            await client.query(endpoint="drug/event", search="bad[query")


async def test_handles_500(client):
    with respx.mock:
        respx.get(f"{BASE_URL}/drug/event.json").mock(
            return_value=httpx.Response(500, json={})
        )
        with pytest.raises(OpenFDAError, match="server error"):
            await client.query(endpoint="drug/event", search="test")


async def test_handles_timeout(client, monkeypatch):
    from fda_mcp.config import Config
    monkeypatch.setattr("fda_mcp.openfda.client.config", Config())

    with respx.mock:
        respx.get(f"{BASE_URL}/drug/event.json").mock(
            side_effect=httpx.TimeoutException("timeout")
        )
        with pytest.raises(OpenFDAError, match="timed out"):
            await client.query(endpoint="drug/event", search="test")
