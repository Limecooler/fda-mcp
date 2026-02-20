"""Tests for the count_records tool."""

import pytest
from mcp.server.fastmcp.exceptions import ToolError

from fda_mcp.tools.count import count_records


@pytest.mark.asyncio
async def test_count_drug_event(mock_openfda_count):
    """Count query on drug/event returns percentages and narrative."""
    result = await count_records(
        endpoint="drug/event",
        count_field="patient.reaction.reactionmeddrapt.exact",
    )
    assert "NAUSEA" in result
    assert "HEADACHE" in result
    assert "FATIGUE" in result
    # Percentages should be present
    assert "50.0%" in result
    assert "30.0%" in result
    assert "20.0%" in result
    # Narrative summary
    assert "most common" in result.lower()
    assert "NAUSEA" in result
    # No .exact warning since field ends with .exact
    assert "Warning" not in result


@pytest.mark.asyncio
async def test_count_device_510k(mock_openfda_count):
    """Count query on device/510k returns expected structure."""
    result = await count_records(
        endpoint="device/510k",
        count_field="product_code.exact",
    )
    assert "NAUSEA" in result
    assert "Total across 3 categories" in result
    assert "1,000" in result


@pytest.mark.asyncio
async def test_count_food_enforcement(mock_openfda_count):
    """Count query on food/enforcement returns expected structure."""
    result = await count_records(
        endpoint="food/enforcement",
        count_field="classification.exact",
        search="status:Ongoing",
        limit=5,
    )
    assert "500" in result
    assert "300" in result
    assert "200" in result


@pytest.mark.asyncio
async def test_count_with_search_and_limit(mock_openfda_count):
    """Count query passes search and limit parameters."""
    result = await count_records(
        endpoint="drug/event",
        count_field="patient.reaction.reactionmeddrapt.exact",
        search='patient.drug.openfda.brand_name:"ASPIRIN"',
        limit=5,
    )
    assert "NAUSEA" in result
    assert "Summary:" in result


@pytest.mark.asyncio
async def test_count_invalid_endpoint():
    """Invalid endpoint raises ToolError."""
    with pytest.raises(ToolError, match="Unknown endpoint"):
        await count_records(
            endpoint="invalid/endpoint",
            count_field="some_field",
        )


@pytest.mark.asyncio
async def test_count_limit_capped_with_note(mock_openfda_count):
    """Limit above 1000 is capped and a note is prepended."""
    result = await count_records(
        endpoint="drug/event",
        count_field="serious.exact",
        limit=5000,
    )
    assert "NAUSEA" in result
    assert "limit was reduced" in result
    assert "5000" in result
    assert "1000" in result


@pytest.mark.asyncio
async def test_count_limit_within_bounds_no_note(mock_openfda_count):
    """Limit within bounds produces no clamping note."""
    result = await count_records(
        endpoint="drug/event",
        count_field="serious.exact",
        limit=500,
    )
    assert "limit was reduced" not in result


@pytest.mark.asyncio
async def test_exact_warning_when_missing_suffix(mock_openfda_count):
    """Warning when count_field doesn't end with .exact on a text field."""
    result = await count_records(
        endpoint="drug/event",
        count_field="patient.reaction.reactionmeddrapt",
    )
    assert "Warning" in result
    assert ".exact" in result
    assert "patient.reaction.reactionmeddrapt.exact" in result


@pytest.mark.asyncio
async def test_no_exact_warning_with_suffix(mock_openfda_count):
    """No warning when count_field ends with .exact."""
    result = await count_records(
        endpoint="drug/event",
        count_field="patient.reaction.reactionmeddrapt.exact",
    )
    assert "Warning" not in result


@pytest.mark.asyncio
async def test_no_exact_warning_for_known_numeric(mock_openfda_count):
    """No warning for known numeric fields like 'serious'."""
    result = await count_records(
        endpoint="drug/event",
        count_field="serious",
    )
    assert "Warning" not in result
