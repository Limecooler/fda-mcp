"""Tests for search_drug_labels tool."""

import pytest
from fda_mcp.tools.search import search_drug_labels


@pytest.mark.anyio
async def test_search_drug_labels(mock_openfda):
    result = await search_drug_labels(
        search='openfda.brand_name:"LIPITOR"'
    )
    assert "LIPITOR" in result
    assert "ATORVASTATIN CALCIUM" in result
    assert "Pfizer" in result
    assert "elevated total cholesterol" in result
    assert "/drug/label.json" in str(mock_openfda.calls.last.request.url)


@pytest.mark.anyio
async def test_label_sections_present(mock_openfda):
    result = await search_drug_labels(search="test")
    assert "Indications And Usage" in result
    assert "Dosage And Administration" in result
    assert "Warnings" in result
    assert "Adverse Reactions" in result
    assert "Contraindications" in result
    assert "Drug Interactions" in result


@pytest.mark.anyio
async def test_limit_clamping(mock_openfda):
    """Passing limit=200 should result in limit=100 in the API call."""
    await search_drug_labels(search="test", limit=200)
    url = str(mock_openfda.calls.last.request.url)
    assert "/drug/label.json" in url
    assert "limit=100" in url


@pytest.mark.anyio
async def test_parameters_forwarded(mock_openfda):
    await search_drug_labels(
        search='openfda.brand_name:"LIPITOR"',
        limit=5,
        skip=10,
        sort="openfda.brand_name:asc",
    )
    url = str(mock_openfda.calls.last.request.url)
    assert "limit=5" in url
    assert "skip=10" in url
