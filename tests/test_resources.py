"""Tests for MCP resource functions — query syntax, endpoints, and field definitions."""

import pytest

from fda_mcp.resources.query_syntax import get_query_syntax
from fda_mcp.resources.endpoints_resource import get_endpoints
from fda_mcp.resources.field_definitions import get_fields_resource, get_fields_text


@pytest.mark.anyio
async def test_query_syntax_contains_operators():
    """Query syntax reference includes AND, OR, NOT operators."""
    text = await get_query_syntax()
    assert "AND" in text
    assert "OR" in text
    assert "NOT" in text


@pytest.mark.anyio
async def test_query_syntax_contains_wildcards():
    """Query syntax reference covers wildcard usage."""
    text = await get_query_syntax()
    assert "*" in text
    assert "wildcard" in text.lower() or "Wildcard" in text


@pytest.mark.anyio
async def test_query_syntax_contains_date_ranges():
    """Query syntax reference covers date range syntax."""
    text = await get_query_syntax()
    assert "Date Range" in text or "date" in text.lower()
    assert "[" in text and "TO" in text


@pytest.mark.anyio
async def test_query_syntax_contains_examples():
    """Query syntax reference includes practical examples."""
    text = await get_query_syntax()
    assert "Example" in text or "example" in text
    assert "search=" in text or "ASPIRIN" in text


@pytest.mark.anyio
async def test_endpoints_lists_all_21():
    """Endpoints resource mentions all 21 OpenFDA API endpoints."""
    text = await get_endpoints()

    expected_endpoints = [
        "drug/event",
        "drug/label",
        "drug/ndc",
        "drug/enforcement",
        "drug/drugsfda",
        "drug/shortage",
        "device/510k",
        "device/pma",
        "device/classification",
        "device/enforcement",
        "device/event",
        "device/recall",
        "device/registrationlisting",
        "device/udi",
        "device/covid19serology",
        "food/enforcement",
        "food/event",
        "other/historicaldocument",
        "other/nsde",
        "other/substance",
        "other/unii",
    ]

    for ep in expected_endpoints:
        assert ep in text, f"Endpoint '{ep}' not found in endpoints resource"


@pytest.mark.anyio
async def test_endpoints_has_category_sections():
    """Endpoints resource organizes endpoints by category."""
    text = await get_endpoints()
    assert "Drug" in text or "drug" in text
    assert "Device" in text or "device" in text
    assert "Food" in text or "food" in text
    assert "Other" in text or "other" in text


@pytest.mark.anyio
async def test_fields_resource_drug_event():
    """Field definitions resource returns fields for drug/event."""
    text = await get_fields_resource("drug/event")
    assert "drug/event" in text
    assert "patient.drug.openfda.brand_name" in text
    assert "patient.reaction.reactionmeddrapt" in text
    assert "serious" in text


@pytest.mark.anyio
async def test_fields_resource_device_510k():
    """Field definitions resource returns fields for device/510k."""
    text = await get_fields_resource("device/510k")
    assert "device/510k" in text
    assert "k_number" in text
    assert "device_name" in text


@pytest.mark.anyio
async def test_fields_resource_unknown_endpoint():
    """Field definitions resource returns a helpful message for unknown endpoints."""
    text = await get_fields_resource("unknown/endpoint")
    assert "No field definitions" in text


@pytest.mark.anyio
async def test_fields_text_includes_type_and_description():
    """get_fields_text includes field type and description."""
    text = get_fields_text("drug/event")
    assert "(string)" in text or "(date)" in text
    assert "Drug brand name" in text
