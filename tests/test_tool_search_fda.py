"""Tests for the unified search_fda tool."""

import pytest
from mcp.server.fastmcp.exceptions import ToolError

from fda_mcp.tools.search import search_fda, _DATASET_TO_ENDPOINT


# -- Dataset routing: verify each dataset maps to the correct endpoint --

@pytest.mark.anyio
@pytest.mark.parametrize("dataset,expected_endpoint", list(_DATASET_TO_ENDPOINT.items()))
async def test_dataset_routes_to_correct_endpoint(mock_openfda, dataset, expected_endpoint):
    """Each dataset value routes to its correct OpenFDA endpoint."""
    result = await search_fda(dataset=dataset, search="test")
    url = str(mock_openfda.calls.last.request.url)
    assert f"/{expected_endpoint}.json" in url


# -- Content verification for key datasets --

@pytest.mark.anyio
async def test_drug_adverse_events_content(mock_openfda):
    result = await search_fda(dataset="drug_adverse_events", search='brand_name:"ASPIRIN"')
    assert "ASPIRIN" in result
    assert "Nausea" in result
    assert "Headache" in result
    assert "10001" in result


@pytest.mark.anyio
async def test_drug_labels_content(mock_openfda):
    result = await search_fda(dataset="drug_labels", search='openfda.brand_name:"LIPITOR"')
    assert "LIPITOR" in result
    assert "ATORVASTATIN CALCIUM" in result
    assert "Pfizer" in result


@pytest.mark.anyio
async def test_drug_ndc_content(mock_openfda):
    result = await search_fda(dataset="drug_ndc", search='brand_name:"LIPITOR"')
    assert "0069-1530" in result
    assert "LIPITOR" in result


@pytest.mark.anyio
async def test_drug_approvals_content(mock_openfda):
    result = await search_fda(dataset="drug_approvals", search='sponsor_name:"Pfizer"')
    assert "NDA021457" in result
    assert "Pfizer" in result


@pytest.mark.anyio
async def test_drug_recalls_content(mock_openfda):
    result = await search_fda(dataset="drug_recalls", search='recalling_firm:"Pfizer"')
    assert "D-0001-2024" in result
    assert "Test Pharma Inc" in result


@pytest.mark.anyio
async def test_drug_shortages_content(mock_openfda):
    result = await search_fda(dataset="drug_shortages", search='generic_name:"doxycycline"')
    assert "DOXYCYCLINE HYCLATE" in result
    assert "VIBRAMYCIN" in result


@pytest.mark.anyio
async def test_device_510k_content(mock_openfda):
    result = await search_fda(dataset="device_510k", search='device_name:"pulse+oximeter"')
    assert "K213456" in result
    assert "Pulse Oximeter" in result
    assert "Test Medical Inc" in result


@pytest.mark.anyio
async def test_device_pma_content(mock_openfda):
    result = await search_fda(dataset="device_pma", search='applicant:"Medtronic"')
    assert "P200001" in result
    assert "Test Cardiac Device" in result


@pytest.mark.anyio
async def test_device_classification_content(mock_openfda):
    result = await search_fda(dataset="device_classification", search='device_class:3')
    assert "DQA" in result
    assert "Oximeter" in result


@pytest.mark.anyio
async def test_device_recalls_content(mock_openfda):
    result = await search_fda(dataset="device_recalls", search='recalling_firm:"Test"')
    assert "Z-0001-2024" in result
    assert "Test Device Corp" in result


@pytest.mark.anyio
async def test_device_recall_details_content(mock_openfda):
    result = await search_fda(dataset="device_recall_details", search='product_code:"FRN"')
    assert "78901" in result
    assert "Software Bug" in result


@pytest.mark.anyio
async def test_device_registration_content(mock_openfda):
    result = await search_fda(dataset="device_registration", search='proprietary_name:"Fitbit"')
    assert "REG123456" in result
    assert "PulseCheck Pro" in result


@pytest.mark.anyio
async def test_device_udi_content(mock_openfda):
    result = await search_fda(dataset="device_udi", search='brand_name:"Freestyle"')
    assert "FreeStyle Libre 2" in result
    assert "Abbott Diabetes Care" in result


@pytest.mark.anyio
async def test_device_covid19_serology_content(mock_openfda):
    result = await search_fda(dataset="device_covid19_serology", search='manufacturer:"Abbott"')
    assert "Abbott" in result
    assert "Architect SARS-CoV-2 IgG" in result


@pytest.mark.anyio
async def test_food_adverse_events_content(mock_openfda):
    result = await search_fda(dataset="food_adverse_events", search='reactions:"NAUSEA"')
    assert "Nausea" in result
    assert "TestSupp Energy Drink" in result


@pytest.mark.anyio
async def test_food_recalls_content(mock_openfda):
    result = await search_fda(dataset="food_recalls", search='classification:"Class I"')
    assert "F-0001-2024" in result
    assert "Test Foods Inc" in result


@pytest.mark.anyio
async def test_historical_documents_content(mock_openfda):
    result = await search_fda(dataset="historical_documents", search='title:"aspirin"')
    assert "Historical FDA Guidance" in result


@pytest.mark.anyio
async def test_substance_data_content(mock_openfda):
    result = await search_fda(dataset="substance_data", search='substance_name:"ASPIRIN"')
    assert "ASPIRIN" in result
    assert "R16CO5Y76E" in result


@pytest.mark.anyio
async def test_unii_content(mock_openfda):
    result = await search_fda(dataset="unii", search='display_name:"caffeine"')
    assert "R16CO5Y76E" in result
    assert "C9H8O4" in result


@pytest.mark.anyio
async def test_nsde_content(mock_openfda):
    result = await search_fda(dataset="nsde", search='marketing_category:"NDA"')
    assert "0002-3227" in result
    assert "NDA" in result


# -- Limit clamping --

@pytest.mark.anyio
async def test_limit_clamped_to_100(mock_openfda):
    """Limit above 100 is clamped and a note is prepended."""
    result = await search_fda(dataset="drug_adverse_events", search="test", limit=200)
    url = str(mock_openfda.calls.last.request.url)
    assert "limit=100" in url
    assert "limit was reduced" in result
    assert "200" in result
    assert "100" in result


@pytest.mark.anyio
async def test_limit_within_bounds_no_note(mock_openfda):
    """Limit within bounds produces no clamping note."""
    result = await search_fda(dataset="drug_adverse_events", search="test", limit=50)
    assert "limit was reduced" not in result


# -- Parameter forwarding --

@pytest.mark.anyio
async def test_parameters_forwarded(mock_openfda):
    """Verify skip, sort, and search are forwarded to the API."""
    await search_fda(
        dataset="drug_adverse_events",
        search='patient.drug.openfda.brand_name:"ASPIRIN"',
        limit=5,
        skip=10,
        sort="receiptdate:desc",
    )
    url = str(mock_openfda.calls.last.request.url)
    assert "limit=5" in url
    assert "skip=10" in url
    assert "sort=receiptdate" in url


# -- Invalid dataset --

@pytest.mark.anyio
async def test_invalid_dataset_raises_error():
    """Invalid dataset value raises ToolError."""
    with pytest.raises(ToolError, match="Unknown dataset"):
        await search_fda(dataset="invalid_thing", search="test")  # type: ignore[arg-type]
