"""Search tool handlers — 9 tools covering all 21 OpenFDA search endpoints."""

from typing import Literal

from fda_mcp.server import mcp
from fda_mcp.openfda.client import openfda_client
from fda_mcp.openfda.summarizer import summarize_response


@mcp.tool()
async def search_adverse_events(
    product_type: Literal["drug", "device", "food"],
    search: str,
    limit: int = 10,
    skip: int = 0,
    sort: str | None = None,
) -> str:
    """Search FDA adverse event reports for drugs, devices, or foods.
    Returns safety reports including reactions, outcomes, and product details.

    Example searches:
      product_type="drug", search='patient.drug.openfda.brand_name:"ASPIRIN"'
      product_type="device", search='device.generic_name:"catheter"+AND+event_type:"Injury"'
      product_type="food", search='reactions:"NAUSEA"'
    """
    endpoint_map = {
        "drug": "drug/event",
        "device": "device/event",
        "food": "food/event",
    }
    result = await openfda_client.query(
        endpoint=endpoint_map[product_type],
        search=search,
        limit=min(limit, 100),
        skip=skip,
        sort=sort,
    )
    return summarize_response(endpoint_map[product_type], result)


@mcp.tool()
async def search_recalls(
    product_type: Literal["drug", "device", "food"],
    search: str,
    source: Literal["enforcement", "recall"] = "enforcement",
    limit: int = 10,
    skip: int = 0,
    sort: str | None = None,
) -> str:
    """Search FDA recall and enforcement reports.
    Use source="recall" (device only) for device-specific recall details.

    Example searches:
      product_type="drug", search='recalling_firm:"Pfizer"'
      product_type="device", source="recall", search='product_code:"LZS"'
      product_type="food", search='classification:"Class I"'
    """
    if source == "recall" and product_type != "device":
        source = "enforcement"

    endpoint_map = {
        ("drug", "enforcement"): "drug/enforcement",
        ("device", "enforcement"): "device/enforcement",
        ("device", "recall"): "device/recall",
        ("food", "enforcement"): "food/enforcement",
    }
    key = (product_type, source)
    endpoint = endpoint_map.get(key, f"{product_type}/enforcement")
    result = await openfda_client.query(
        endpoint=endpoint,
        search=search,
        limit=min(limit, 100),
        skip=skip,
        sort=sort,
    )
    return summarize_response(endpoint, result)


@mcp.tool()
async def search_drug_labels(
    search: str,
    limit: int = 10,
    skip: int = 0,
    sort: str | None = None,
) -> str:
    """Search FDA drug product labeling (SPL).
    Returns label sections: indications, dosage, warnings, adverse reactions.

    Example searches:
      search='openfda.brand_name:"LIPITOR"'
      search='indications_and_usage:"diabetes"+AND+openfda.manufacturer_name:"Novo+Nordisk"'
    """
    result = await openfda_client.query(
        endpoint="drug/label",
        search=search,
        limit=min(limit, 100),
        skip=skip,
        sort=sort,
    )
    return summarize_response("drug/label", result)


@mcp.tool()
async def search_drugs(
    source: Literal["approvals", "ndc"],
    search: str,
    limit: int = 10,
    skip: int = 0,
    sort: str | None = None,
) -> str:
    """Search FDA-approved drugs or the National Drug Code directory.
    source="approvals" searches Drugs@FDA; source="ndc" searches the NDC directory.

    Example searches:
      source="approvals", search='sponsor_name:"Pfizer"'
      source="ndc", search='brand_name:"ASPIRIN"'
    """
    endpoint_map = {
        "approvals": "drug/drugsfda",
        "ndc": "drug/ndc",
    }
    endpoint = endpoint_map[source]
    result = await openfda_client.query(
        endpoint=endpoint,
        search=search,
        limit=min(limit, 100),
        skip=skip,
        sort=sort,
    )
    return summarize_response(endpoint, result)


@mcp.tool()
async def search_drug_shortages(
    search: str,
    limit: int = 10,
    skip: int = 0,
    sort: str | None = None,
) -> str:
    """Search FDA drug shortage reports.

    Example searches:
      search='generic_name:"doxycycline"'
      search='status:"Resolved"'
    """
    result = await openfda_client.query(
        endpoint="drug/shortage",
        search=search,
        limit=min(limit, 100),
        skip=skip,
        sort=sort,
    )
    return summarize_response("drug/shortage", result)


@mcp.tool()
async def search_device_submissions(
    submission_type: Literal["510k", "pma", "classification", "registration"],
    search: str,
    limit: int = 10,
    skip: int = 0,
    sort: str | None = None,
) -> str:
    """Search FDA device premarket submissions and classifications.
    Covers 510(k), PMA, device classification, and registration/listing data.

    Example searches:
      submission_type="510k", search='device_name:"pulse+oximeter"'
      submission_type="pma", search='applicant:"Medtronic"'
      submission_type="classification", search='device_class:3'
      submission_type="registration", search='proprietary_name:"Fitbit"'
    """
    endpoint_map = {
        "510k": "device/510k",
        "pma": "device/pma",
        "classification": "device/classification",
        "registration": "device/registrationlisting",
    }
    endpoint = endpoint_map[submission_type]
    result = await openfda_client.query(
        endpoint=endpoint,
        search=search,
        limit=min(limit, 100),
        skip=skip,
        sort=sort,
    )
    return summarize_response(endpoint, result)


@mcp.tool()
async def search_device_udi(
    search: str,
    limit: int = 10,
    skip: int = 0,
    sort: str | None = None,
) -> str:
    """Search the FDA Unique Device Identifier (UDI) database.
    Returns device identifiers, brand names, and manufacturer info.

    Example searches:
      search='brand_name:"Freestyle"'
      search='company_name:"Abbott"'
    """
    result = await openfda_client.query(
        endpoint="device/udi",
        search=search,
        limit=min(limit, 100),
        skip=skip,
        sort=sort,
    )
    return summarize_response("device/udi", result)


@mcp.tool()
async def search_substances(
    source: Literal["substance", "unii", "nsde"],
    search: str,
    limit: int = 10,
    skip: int = 0,
    sort: str | None = None,
) -> str:
    """Search FDA substance, UNII, or NDC/SPL data elements databases.
    source="substance" for substance registrations, "unii" for ingredient IDs,
    "nsde" for NDC/SPL data elements.

    Example searches:
      source="substance", search='substance_name:"ASPIRIN"'
      source="unii", search='display_name:"caffeine"'
      source="nsde", search='marketing_category:"NDA"'
    """
    endpoint_map = {
        "substance": "other/substance",
        "unii": "other/unii",
        "nsde": "other/nsde",
    }
    endpoint = endpoint_map[source]
    result = await openfda_client.query(
        endpoint=endpoint,
        search=search,
        limit=min(limit, 100),
        skip=skip,
        sort=sort,
    )
    return summarize_response(endpoint, result)


@mcp.tool()
async def search_other(
    dataset: Literal["historical_documents", "covid19_serology"],
    search: str,
    limit: int = 10,
    skip: int = 0,
    sort: str | None = None,
) -> str:
    """Search other FDA datasets: historical documents or COVID-19 serology tests.

    Example searches:
      dataset="historical_documents", search='title:"aspirin"'
      dataset="covid19_serology", search='manufacturer:"Abbott"'
    """
    endpoint_map = {
        "historical_documents": "other/historicaldocument",
        "covid19_serology": "device/covid19serology",
    }
    endpoint = endpoint_map[dataset]
    result = await openfda_client.query(
        endpoint=endpoint,
        search=search,
        limit=min(limit, 100),
        skip=skip,
        sort=sort,
    )
    return summarize_response(endpoint, result)
