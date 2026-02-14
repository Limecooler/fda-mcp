"""Tests for search_device_udi tool."""

import pytest
from fda_mcp.tools.search import search_device_udi


@pytest.mark.anyio
async def test_search_device_udi(mock_openfda):
    result = await search_device_udi(
        search='brand_name:"Freestyle"'
    )
    assert "FreeStyle Libre 2" in result
    assert "Abbott Diabetes Care" in result
    assert "Continuous Glucose Monitor" in result
    assert "00886009100121" in result
    assert "GS1" in result
    assert "/device/udi.json" in str(mock_openfda.calls.last.request.url)


@pytest.mark.anyio
async def test_limit_clamping(mock_openfda):
    """Passing limit=200 should result in limit=100 in the API call."""
    await search_device_udi(search="test", limit=200)
    url = str(mock_openfda.calls.last.request.url)
    assert "/device/udi.json" in url
    assert "limit=100" in url


@pytest.mark.anyio
async def test_parameters_forwarded(mock_openfda):
    await search_device_udi(
        search='company_name:"Abbott"',
        limit=5,
        skip=10,
        sort="brand_name:asc",
    )
    url = str(mock_openfda.calls.last.request.url)
    assert "limit=5" in url
    assert "skip=10" in url
