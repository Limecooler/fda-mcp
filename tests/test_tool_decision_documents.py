"""Tests for the get_decision_document tool."""

import pytest
from unittest.mock import AsyncMock, patch

from fda_mcp.tools.decision_documents import get_decision_document
from fda_mcp.errors import InvalidIdentifierError


MOCK_PDF_TEXT = "Source: https://example.com/doc.pdf\nPages: 2\nExtraction: text extraction\n\nSample document content."


@pytest.fixture
def mock_fetch():
    """Mock fetch_and_extract_pdf to avoid real HTTP calls."""
    with patch(
        "fda_mcp.tools.decision_documents.fetch_and_extract_pdf",
        new_callable=AsyncMock,
        return_value=MOCK_PDF_TEXT,
    ) as mock:
        yield mock


class TestGetDecisionDocument510k:
    @pytest.mark.anyio
    async def test_510k_summary(self, mock_fetch):
        result = await get_decision_document("510k_summary", "K213456")

        mock_fetch.assert_called_once_with(
            "https://www.accessdata.fda.gov/cdrh_docs/reviews/K213456.pdf",
            max_length=8000,
        )
        assert result == MOCK_PDF_TEXT

    @pytest.mark.anyio
    async def test_510k_invalid_number(self):
        with pytest.raises(InvalidIdentifierError):
            await get_decision_document("510k_summary", "INVALID")


class TestGetDecisionDocumentDeNovo:
    @pytest.mark.anyio
    async def test_denovo_decision(self, mock_fetch):
        result = await get_decision_document("denovo_decision", "DEN200001")

        mock_fetch.assert_called_once_with(
            "https://www.accessdata.fda.gov/cdrh_docs/reviews/DEN200001.pdf",
            max_length=8000,
        )
        assert result == MOCK_PDF_TEXT


class TestGetDecisionDocumentPMA:
    @pytest.mark.anyio
    async def test_pma_approval(self, mock_fetch):
        result = await get_decision_document("pma_approval", "P200001")

        mock_fetch.assert_called_once_with(
            "https://www.accessdata.fda.gov/cdrh_docs/pdf20/P200001A.pdf",
            max_length=8000,
        )
        assert result == MOCK_PDF_TEXT

    @pytest.mark.anyio
    async def test_pma_ssed(self, mock_fetch):
        result = await get_decision_document("pma_ssed", "P200001")

        mock_fetch.assert_called_once_with(
            "https://www.accessdata.fda.gov/cdrh_docs/pdf20/P200001B.pdf",
            max_length=8000,
        )
        assert result == MOCK_PDF_TEXT

    @pytest.mark.anyio
    async def test_pma_supplement(self, mock_fetch):
        result = await get_decision_document(
            "pma_supplement", "P200001", supplement_number="013"
        )

        mock_fetch.assert_called_once_with(
            "https://www.accessdata.fda.gov/cdrh_docs/pdf20/P200001S013A.pdf",
            max_length=8000,
        )
        assert result == MOCK_PDF_TEXT

    @pytest.mark.anyio
    async def test_pma_invalid_number(self):
        with pytest.raises(InvalidIdentifierError):
            await get_decision_document("pma_approval", "BADNUM")


class TestGetDecisionDocumentMaxLength:
    @pytest.mark.anyio
    async def test_custom_max_length(self, mock_fetch):
        await get_decision_document("510k_summary", "K213456", max_length=500)

        mock_fetch.assert_called_once_with(
            "https://www.accessdata.fda.gov/cdrh_docs/reviews/K213456.pdf",
            max_length=500,
        )

    @pytest.mark.anyio
    async def test_default_max_length(self, mock_fetch):
        """Default max_length comes from config.default_pdf_max_length."""
        await get_decision_document("510k_summary", "K213456")

        _, kwargs = mock_fetch.call_args
        assert kwargs["max_length"] == 8000
