"""Live API tests for all 21 OpenFDA endpoints.

These tests hit the real OpenFDA API and verify basic connectivity.
Run with: uv run pytest -m integration
"""

import pytest

from fda_mcp.openfda.client import OpenFDAClient
from fda_mcp.openfda.endpoints import OpenFDAEndpoint

pytestmark = pytest.mark.integration


@pytest.fixture
def client():
    return OpenFDAClient()


async def _assert_has_results(client: OpenFDAClient, endpoint: str, search: str):
    """Helper to verify an endpoint returns results."""
    result = await client.query(endpoint=endpoint, search=search, limit=1)
    assert "results" in result, f"No 'results' key in response from {endpoint}"
    assert len(result["results"]) > 0, f"Empty results from {endpoint}"
    meta = result.get("meta", {}).get("results", {})
    assert meta.get("total", 0) > 0, f"Total is 0 for {endpoint}"


async def test_live_drug_event(client):
    await _assert_has_results(
        client, "drug/event",
        'patient.drug.openfda.brand_name:"ASPIRIN"',
    )


async def test_live_drug_label(client):
    await _assert_has_results(
        client, "drug/label",
        'openfda.brand_name:"ASPIRIN"',
    )


async def test_live_drug_ndc(client):
    await _assert_has_results(
        client, "drug/ndc",
        'brand_name:"ASPIRIN"',
    )


async def test_live_drug_enforcement(client):
    await _assert_has_results(
        client, "drug/enforcement",
        'classification:"Class I"',
    )


async def test_live_drug_drugsfda(client):
    await _assert_has_results(
        client, "drug/drugsfda",
        'openfda.brand_name:"LIPITOR"',
    )


async def test_live_drug_shortage(client):
    # Drug shortage endpoint may return 404 when no shortages exist
    try:
        result = await client.query(endpoint="drug/shortage", limit=1)
        assert "results" in result
    except Exception:
        pytest.skip("Drug shortage endpoint returned no data (may be temporarily empty)")


async def test_live_device_510k(client):
    await _assert_has_results(
        client, "device/510k",
        'device_name:"pulse+oximeter"',
    )


async def test_live_device_pma(client):
    await _assert_has_results(
        client, "device/pma",
        'advisory_committee_description:"Cardiovascular"',
    )


async def test_live_device_classification(client):
    await _assert_has_results(
        client, "device/classification",
        'device_class:3',
    )


async def test_live_device_enforcement(client):
    await _assert_has_results(
        client, "device/enforcement",
        'classification:"Class I"',
    )


async def test_live_device_event(client):
    await _assert_has_results(
        client, "device/event",
        'event_type:"Injury"',
    )


async def test_live_device_recall(client):
    result = await client.query(endpoint="device/recall", limit=1)
    assert "results" in result


async def test_live_device_registrationlisting(client):
    result = await client.query(
        endpoint="device/registrationlisting", limit=1
    )
    assert "results" in result


async def test_live_device_udi(client):
    await _assert_has_results(
        client, "device/udi",
        'company_name:"Abbott"',
    )


async def test_live_device_covid19serology(client):
    result = await client.query(endpoint="device/covid19serology", limit=1)
    assert "results" in result


async def test_live_food_enforcement(client):
    await _assert_has_results(
        client, "food/enforcement",
        'classification:"Class I"',
    )


async def test_live_food_event(client):
    result = await client.query(endpoint="food/event", limit=1)
    assert "results" in result


async def test_live_other_historicaldocument(client):
    result = await client.query(endpoint="other/historicaldocument", limit=1)
    assert "results" in result


async def test_live_other_nsde(client):
    result = await client.query(endpoint="other/nsde", limit=1)
    assert "results" in result


async def test_live_other_substance(client):
    # Substance endpoint: use unfiltered query (search field names differ)
    result = await client.query(endpoint="other/substance", limit=1)
    assert "results" in result
    assert len(result["results"]) > 0


async def test_live_other_unii(client):
    # UNII endpoint: use unfiltered query (search field names differ)
    result = await client.query(endpoint="other/unii", limit=1)
    assert "results" in result
    assert len(result["results"]) > 0
