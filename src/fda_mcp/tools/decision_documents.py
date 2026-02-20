"""get_decision_document tool — FDA regulatory decision document retrieval."""

from typing import Literal

from fda_mcp.server import mcp
from fda_mcp.documents.urls import build_document_url
from fda_mcp.documents.fetcher import fetch_and_extract_pdf
from fda_mcp.config import config


@mcp.tool()
async def get_decision_document(
    document_type: Literal[
        "510k_summary",
        "denovo_decision",
        "pma_approval",
        "pma_ssed",
        "pma_supplement",
    ],
    submission_number: str,
    supplement_number: str | None = None,
    max_length: int | None = None,
) -> str:
    """Fetch FDA regulatory decision documents (not available via OpenFDA API).
    Downloads the PDF from FDA servers and extracts text content.

    When to use: After finding a device submission via search_fda (e.g.,
    dataset="device_510k" or "device_pma"), use the submission number from
    those results to retrieve the full decision document.

    Args:
        document_type: Type of document to retrieve.
        submission_number: FDA identifier. Formats:
            510k_summary: "K" + 6 digits (e.g., "K213456")
            denovo_decision: "DEN" + 6 digits (e.g., "DEN200001")
            pma_approval/pma_ssed/pma_supplement: "P" + 6 digits (e.g., "P200001")
        supplement_number: Required for pma_supplement only (e.g., "013").
        max_length: Max text characters to return (default 8000).
            Increase for longer documents.

    Examples:
        document_type="510k_summary", submission_number="K213456"
        document_type="pma_approval", submission_number="P200001"
        document_type="pma_supplement", submission_number="P200001", supplement_number="013"
    """
    if max_length is None:
        max_length = config.default_pdf_max_length

    url = build_document_url(document_type, submission_number, supplement_number)
    return await fetch_and_extract_pdf(url, max_length=max_length)
