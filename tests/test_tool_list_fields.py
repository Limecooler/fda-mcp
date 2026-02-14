"""Tests for the list_searchable_fields tool."""

import pytest
from mcp.server.fastmcp.exceptions import ToolError

from fda_mcp.tools.fields import list_searchable_fields


@pytest.mark.asyncio
async def test_fields_drug_event_common():
    """Common fields for drug/event returns expected field names."""
    result = await list_searchable_fields(
        endpoint="drug/event",
        category="common",
    )
    assert "drug/event" in result
    assert "common" in result
    assert "patient.drug.openfda.brand_name" in result
    assert "patient.reaction.reactionmeddrapt" in result
    assert "serious" in result
    assert "receiptdate" in result


@pytest.mark.asyncio
async def test_fields_device_510k_common():
    """Common fields for device/510k returns expected field names."""
    result = await list_searchable_fields(
        endpoint="device/510k",
        category="common",
    )
    assert "device/510k" in result
    assert "k_number" in result
    assert "device_name" in result
    assert "applicant" in result
    assert "decision_description" in result
    assert "product_code" in result


@pytest.mark.asyncio
async def test_fields_all_returns_more_than_common():
    """Category 'all' returns more fields than 'common' for drug/event."""
    common_result = await list_searchable_fields(
        endpoint="drug/event",
        category="common",
    )
    all_result = await list_searchable_fields(
        endpoint="drug/event",
        category="all",
    )
    # "all" should include common fields plus extra ones
    assert "patient.drug.openfda.brand_name" in all_result
    assert "safetyreportid" in all_result
    assert "patient.patientsex" in all_result
    assert "occurcountry" in all_result
    # "all" text should be longer since it has more fields
    assert len(all_result) > len(common_result)


@pytest.mark.asyncio
async def test_fields_device_510k_all():
    """Category 'all' for device/510k includes additional fields."""
    result = await list_searchable_fields(
        endpoint="device/510k",
        category="all",
    )
    # Common fields present
    assert "k_number" in result
    # Additional fields present
    assert "review_panel" in result
    assert "clearance_type" in result
    assert "third_party_flag" in result


@pytest.mark.asyncio
async def test_fields_includes_type_and_description():
    """Field listing includes type annotations and descriptions."""
    result = await list_searchable_fields(
        endpoint="drug/event",
        category="common",
    )
    assert "(string)" in result
    assert "(date)" in result
    assert "Drug brand name" in result
    assert "Date report received" in result


@pytest.mark.asyncio
async def test_fields_unknown_endpoint():
    """Unknown endpoint raises ToolError."""
    with pytest.raises(ToolError, match="Unknown endpoint"):
        await list_searchable_fields(
            endpoint="invalid/endpoint",
            category="common",
        )
