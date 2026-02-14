"""Tests for search_other tool."""

import pytest
from fda_mcp.tools.search import search_other


@pytest.mark.anyio
async def test_historical_documents(mock_openfda):
    result = await search_other(
        dataset="historical_documents", search='title:"aspirin"'
    )
    assert "Historical FDA Guidance" in result
    assert "19800101" in result
    assert "Guidance" in result
    assert "/other/historicaldocument.json" in str(
        mock_openfda.calls.last.request.url
    )


@pytest.mark.anyio
async def test_covid19_serology(mock_openfda):
    result = await search_other(
        dataset="covid19_serology", search='manufacturer:"Abbott"'
    )
    assert "Abbott" in result
    assert "Architect SARS-CoV-2 IgG" in result
    assert "99.6%" in result
    assert "99.3%" in result
    assert "/device/covid19serology.json" in str(
        mock_openfda.calls.last.request.url
    )


@pytest.mark.anyio
async def test_limit_clamping(mock_openfda):
    """Passing limit=200 should result in limit=100 in the API call."""
    await search_other(
        dataset="historical_documents", search="test", limit=200
    )
    url = str(mock_openfda.calls.last.request.url)
    assert "/other/historicaldocument.json" in url
    assert "limit=100" in url


@pytest.mark.anyio
async def test_parameters_forwarded(mock_openfda):
    await search_other(
        dataset="covid19_serology",
        search='manufacturer:"test"',
        limit=5,
        skip=10,
        sort="manufacturer:asc",
    )
    url = str(mock_openfda.calls.last.request.url)
    assert "limit=5" in url
    assert "skip=10" in url
