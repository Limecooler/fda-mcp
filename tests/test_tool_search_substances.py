"""Tests for search_substances tool."""

import pytest
from fda_mcp.tools.search import search_substances


@pytest.mark.anyio
async def test_substance_source(mock_openfda):
    result = await search_substances(
        source="substance", search='substance_name:"ASPIRIN"'
    )
    assert "ASPIRIN" in result
    assert "R16CO5Y76E" in result
    assert "50-78-2" in result
    assert "CAS" in result
    assert "/other/substance.json" in str(mock_openfda.calls.last.request.url)


@pytest.mark.anyio
async def test_unii_source(mock_openfda):
    result = await search_substances(
        source="unii", search='display_name:"caffeine"'
    )
    assert "R16CO5Y76E" in result
    assert "ASPIRIN" in result
    assert "C9H8O4" in result
    assert "/other/unii.json" in str(mock_openfda.calls.last.request.url)


@pytest.mark.anyio
async def test_nsde_source(mock_openfda):
    result = await search_substances(
        source="nsde", search='marketing_category:"NDA"'
    )
    assert "0002-3227" in result
    assert "NDA" in result
    assert "abc-123" in result
    assert "/other/nsde.json" in str(mock_openfda.calls.last.request.url)


@pytest.mark.anyio
async def test_limit_clamping(mock_openfda):
    """Passing limit=200 should result in limit=100 in the API call."""
    await search_substances(
        source="substance", search="test", limit=200
    )
    url = str(mock_openfda.calls.last.request.url)
    assert "/other/substance.json" in url
    assert "limit=100" in url


@pytest.mark.anyio
async def test_parameters_forwarded(mock_openfda):
    await search_substances(
        source="unii",
        search='display_name:"test"',
        limit=5,
        skip=10,
        sort="display_name:asc",
    )
    url = str(mock_openfda.calls.last.request.url)
    assert "limit=5" in url
    assert "skip=10" in url
