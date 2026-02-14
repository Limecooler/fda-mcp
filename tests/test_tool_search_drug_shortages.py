"""Tests for search_drug_shortages tool."""

import pytest
from fda_mcp.tools.search import search_drug_shortages


@pytest.mark.anyio
async def test_search_drug_shortages(mock_openfda):
    result = await search_drug_shortages(
        search='generic_name:"doxycycline"'
    )
    assert "DOXYCYCLINE HYCLATE" in result
    assert "VIBRAMYCIN" in result
    assert "Currently in Shortage" in result
    assert "Pfizer" in result
    assert "/drug/shortage.json" in str(mock_openfda.calls.last.request.url)


@pytest.mark.anyio
async def test_limit_clamping(mock_openfda):
    """Passing limit=200 should result in limit=100 in the API call."""
    await search_drug_shortages(search="test", limit=200)
    url = str(mock_openfda.calls.last.request.url)
    assert "/drug/shortage.json" in url
    assert "limit=100" in url


@pytest.mark.anyio
async def test_parameters_forwarded(mock_openfda):
    await search_drug_shortages(
        search='status:"Resolved"',
        limit=5,
        skip=10,
        sort="generic_name:asc",
    )
    url = str(mock_openfda.calls.last.request.url)
    assert "limit=5" in url
    assert "skip=10" in url
