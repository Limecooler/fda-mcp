"""search_fda tool — unified search across all 21 OpenFDA endpoints."""

from typing import Literal

from mcp.server.fastmcp.exceptions import ToolError

from fda_mcp.server import mcp
from fda_mcp.openfda.client import openfda_client
from fda_mcp.openfda.summarizer import summarize_response
from fda_mcp.tools._helpers import clamp_limit

DatasetType = Literal[
    # Drug (6)
    "drug_adverse_events", "drug_labels", "drug_ndc", "drug_approvals",
    "drug_recalls", "drug_shortages",
    # Device (9)
    "device_adverse_events", "device_510k", "device_pma",
    "device_classification", "device_recalls", "device_recall_details",
    "device_registration", "device_udi", "device_covid19_serology",
    # Food (2)
    "food_adverse_events", "food_recalls",
    # Other (4)
    "historical_documents", "substance_data", "unii", "nsde",
]

_DATASET_TO_ENDPOINT: dict[str, str] = {
    "drug_adverse_events": "drug/event",
    "drug_labels": "drug/label",
    "drug_ndc": "drug/ndc",
    "drug_approvals": "drug/drugsfda",
    "drug_recalls": "drug/enforcement",
    "drug_shortages": "drug/shortage",
    "device_adverse_events": "device/event",
    "device_510k": "device/510k",
    "device_pma": "device/pma",
    "device_classification": "device/classification",
    "device_recalls": "device/enforcement",
    "device_recall_details": "device/recall",
    "device_registration": "device/registrationlisting",
    "device_udi": "device/udi",
    "device_covid19_serology": "device/covid19serology",
    "food_adverse_events": "food/event",
    "food_recalls": "food/enforcement",
    "historical_documents": "other/historicaldocument",
    "substance_data": "other/substance",
    "unii": "other/unii",
    "nsde": "other/nsde",
}


@mcp.tool()
async def search_fda(
    dataset: DatasetType,
    search: str,
    limit: int = 10,
    skip: int = 0,
    sort: str | None = None,
) -> str:
    """Search any of the 21 OpenFDA datasets. Returns individual records.

    When to use: Finding specific records — adverse events, drug labels,
    device submissions, recalls, etc. For aggregation/statistics, use
    count_records instead. If unsure which fields to search, call
    list_searchable_fields first.

    Args:
        dataset: Which FDA dataset to search. Options by category:
            Drug: drug_adverse_events, drug_labels, drug_ndc, drug_approvals,
                  drug_recalls, drug_shortages
            Device: device_adverse_events, device_510k, device_pma,
                    device_classification, device_recalls, device_recall_details,
                    device_registration, device_udi, device_covid19_serology
            Food: food_adverse_events, food_recalls
            Other: historical_documents, substance_data, unii, nsde
        search: OpenFDA query string. Quote string values and use + for spaces.
        limit: Max results to return (default 10, max 100).
        skip: Number of results to skip for pagination.
        sort: Sort field and direction (e.g., "report_date:desc").

    Examples:
        Drug adverse events:
          dataset="drug_adverse_events", search='patient.drug.openfda.brand_name:"ASPIRIN"'
        Drug labels:
          dataset="drug_labels", search='openfda.brand_name:"LIPITOR"'
        Device 510(k):
          dataset="device_510k", search='device_name:"pulse+oximeter"'
        Food recalls:
          dataset="food_recalls", search='classification:"Class I"'
        Substance lookup:
          dataset="substance_data", search='substance_name:"ASPIRIN"'
    """
    endpoint = _DATASET_TO_ENDPOINT.get(dataset)
    if endpoint is None:
        raise ToolError(
            f"Unknown dataset '{dataset}'. "
            f"Valid datasets: {', '.join(sorted(_DATASET_TO_ENDPOINT.keys()))}"
        )

    limit, note = clamp_limit(limit, 100)

    result = await openfda_client.query(
        endpoint=endpoint,
        search=search,
        limit=limit,
        skip=skip,
        sort=sort,
    )
    response = summarize_response(endpoint, result)
    if note:
        response = note + "\n\n" + response
    return response
