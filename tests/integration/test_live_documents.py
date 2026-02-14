"""Live tests for FDA document fetching.

These tests download real PDFs from FDA servers.
Run with: uv run pytest -m integration
"""

import pytest

from fda_mcp.documents.urls import build_document_url
from fda_mcp.documents.fetcher import fetch_and_extract_pdf
from fda_mcp.errors import DocumentNotFoundError

pytestmark = pytest.mark.integration


async def test_live_510k_modern_pdf():
    """Fetch a known modern 510(k) summary (machine-generated PDF)."""
    url = build_document_url("510k_summary", "K213456")
    try:
        result = await fetch_and_extract_pdf(url, max_length=2000)
        assert "Source:" in result
        assert "Pages:" in result
    except DocumentNotFoundError:
        pytest.skip("Document K213456 not found on FDA servers")


async def test_live_pma_ssed():
    """Fetch a known PMA SSED document."""
    url = build_document_url("pma_ssed", "P200001")
    try:
        result = await fetch_and_extract_pdf(url, max_length=2000)
        assert "Source:" in result
    except DocumentNotFoundError:
        pytest.skip("Document P200001 SSED not found on FDA servers")


async def test_live_document_not_found():
    """Verify 404 handling for a non-existent document."""
    url = build_document_url("510k_summary", "K000001")
    with pytest.raises(DocumentNotFoundError):
        await fetch_and_extract_pdf(url)
