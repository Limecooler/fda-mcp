"""Tests for search_recalls tool."""

import pytest
from fda_mcp.tools.search import search_recalls


@pytest.mark.anyio
async def test_drug_enforcement(mock_openfda):
    result = await search_recalls(
        product_type="drug", search='recalling_firm:"Pfizer"'
    )
    assert "D-0001-2024" in result
    assert "Test Pharma Inc" in result
    assert "Failed dissolution testing" in result
    assert "/drug/enforcement.json" in str(mock_openfda.calls.last.request.url)


@pytest.mark.anyio
async def test_device_enforcement(mock_openfda):
    result = await search_recalls(
        product_type="device",
        source="enforcement",
        search='recalling_firm:"Test"',
    )
    assert "Z-0001-2024" in result
    assert "Test Device Corp" in result
    assert "Software defect" in result
    assert "/device/enforcement.json" in str(mock_openfda.calls.last.request.url)


@pytest.mark.anyio
async def test_device_recall(mock_openfda):
    result = await search_recalls(
        product_type="device",
        source="recall",
        search='product_code:"FRN"',
    )
    assert "78901" in result
    assert "Software Bug" in result
    assert "/device/recall.json" in str(mock_openfda.calls.last.request.url)


@pytest.mark.anyio
async def test_food_enforcement(mock_openfda):
    result = await search_recalls(
        product_type="food", search='classification:"Class I"'
    )
    assert "F-0001-2024" in result
    assert "Test Foods Inc" in result
    assert "Undeclared allergen" in result
    assert "/food/enforcement.json" in str(mock_openfda.calls.last.request.url)


@pytest.mark.anyio
async def test_recall_source_fallback_for_non_device(mock_openfda):
    """source='recall' with product_type != 'device' falls back to enforcement."""
    result = await search_recalls(
        product_type="drug", source="recall", search="test"
    )
    assert "/drug/enforcement.json" in str(mock_openfda.calls.last.request.url)
    assert "D-0001-2024" in result


@pytest.mark.anyio
async def test_food_recall_source_fallback(mock_openfda):
    """source='recall' with product_type='food' falls back to enforcement."""
    result = await search_recalls(
        product_type="food", source="recall", search="test"
    )
    assert "/food/enforcement.json" in str(mock_openfda.calls.last.request.url)
    assert "F-0001-2024" in result


@pytest.mark.anyio
async def test_limit_clamping(mock_openfda):
    """Passing limit=200 should result in limit=100 in the API call."""
    await search_recalls(
        product_type="drug", search="test", limit=200
    )
    url = str(mock_openfda.calls.last.request.url)
    assert "/drug/enforcement.json" in url
    assert "limit=100" in url
