"""Tests for search_drugs tool."""

import pytest
from fda_mcp.tools.search import search_drugs


@pytest.mark.anyio
async def test_search_drugs_approvals(mock_openfda):
    result = await search_drugs(
        source="approvals", search='sponsor_name:"Pfizer"'
    )
    assert "NDA021457" in result
    assert "Pfizer" in result
    assert "LIPITOR" in result
    assert "ATORVASTATIN CALCIUM" in result
    assert "/drug/drugsfda.json" in str(mock_openfda.calls.last.request.url)


@pytest.mark.anyio
async def test_search_drugs_ndc(mock_openfda):
    result = await search_drugs(
        source="ndc", search='brand_name:"LIPITOR"'
    )
    assert "0069-1530" in result
    assert "LIPITOR" in result
    assert "TABLET, FILM COATED" in result
    assert "/drug/ndc.json" in str(mock_openfda.calls.last.request.url)


@pytest.mark.anyio
async def test_limit_clamping(mock_openfda):
    """Passing limit=200 should result in limit=100 in the API call."""
    await search_drugs(source="approvals", search="test", limit=200)
    url = str(mock_openfda.calls.last.request.url)
    assert "/drug/drugsfda.json" in url
    assert "limit=100" in url


@pytest.mark.anyio
async def test_parameters_forwarded(mock_openfda):
    await search_drugs(
        source="ndc",
        search='brand_name:"ASPIRIN"',
        limit=5,
        skip=20,
        sort="brand_name:asc",
    )
    url = str(mock_openfda.calls.last.request.url)
    assert "limit=5" in url
    assert "skip=20" in url
