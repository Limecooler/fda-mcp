"""Tests for search_adverse_events tool."""

import pytest
from fda_mcp.tools.search import search_adverse_events


@pytest.mark.anyio
async def test_drug_adverse_events(mock_openfda):
    result = await search_adverse_events(
        product_type="drug", search='patient.drug.openfda.brand_name:"ASPIRIN"'
    )
    assert "ASPIRIN" in result
    assert "Nausea" in result
    assert "Headache" in result
    assert "10001" in result
    assert mock_openfda.calls.last is not None
    assert "/drug/event.json" in str(mock_openfda.calls.last.request.url)


@pytest.mark.anyio
async def test_device_adverse_events(mock_openfda):
    result = await search_adverse_events(
        product_type="device", search='device.generic_name:"catheter"'
    )
    assert "Infusion Pump" in result
    assert "Injury" in result
    assert "/device/event.json" in str(mock_openfda.calls.last.request.url)


@pytest.mark.anyio
async def test_food_adverse_events(mock_openfda):
    result = await search_adverse_events(
        product_type="food", search='reactions:"NAUSEA"'
    )
    assert "Nausea" in result
    assert "TestSupp Energy Drink" in result
    assert "/food/event.json" in str(mock_openfda.calls.last.request.url)


@pytest.mark.anyio
async def test_limit_clamping(mock_openfda):
    """Passing limit=200 should result in limit=100 in the API call."""
    await search_adverse_events(
        product_type="drug", search="test", limit=200
    )
    url = str(mock_openfda.calls.last.request.url)
    assert "/drug/event.json" in url
    assert "limit=100" in url


@pytest.mark.anyio
async def test_parameters_forwarded(mock_openfda):
    """Verify skip, sort, and search are forwarded to the API."""
    await search_adverse_events(
        product_type="drug",
        search='patient.drug.openfda.brand_name:"ASPIRIN"',
        limit=5,
        skip=10,
        sort="receiptdate:desc",
    )
    url = str(mock_openfda.calls.last.request.url)
    assert "limit=5" in url
    assert "skip=10" in url
    assert "sort=receiptdate" in url
