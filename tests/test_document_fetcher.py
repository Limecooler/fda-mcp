"""Tests for PDF fetching and text extraction."""

import pytest
import httpx
import respx

from fda_mcp.documents.fetcher import fetch_and_extract_pdf
from fda_mcp.errors import DocumentNotFoundError

PDF_URL = "https://www.accessdata.fda.gov/cdrh_docs/reviews/K213456.pdf"


@pytest.fixture
def mock_pdfplumber(monkeypatch):
    """Mock pdfplumber.open to return controlled text content."""

    class FakePage:
        def __init__(self, text):
            self._text = text

        def extract_text(self):
            return self._text

    class FakePDF:
        def __init__(self, pages):
            self.pages = pages

        def __enter__(self):
            return self

        def __exit__(self, *args):
            pass

    def _factory(texts: list[str]):
        def _open(path):
            return FakePDF([FakePage(t) for t in texts])

        monkeypatch.setattr("fda_mcp.documents.fetcher.pdfplumber.open", _open)

    return _factory


class TestFetchAndExtractPdf:
    @respx.mock
    @pytest.mark.anyio
    async def test_successful_extraction(self, mock_pdfplumber):
        """Text extraction from a normal PDF."""
        respx.get(PDF_URL).mock(
            return_value=httpx.Response(200, content=b"%PDF-fake")
        )
        mock_pdfplumber(["This is page one content that is long enough to pass."] * 3)

        result = await fetch_and_extract_pdf(PDF_URL)

        assert "Source: " + PDF_URL in result
        assert "Pages: 3" in result
        assert "Extraction: text extraction" in result
        assert "This is page one content" in result

    @respx.mock
    @pytest.mark.anyio
    async def test_404_raises_document_not_found(self):
        """404 response raises DocumentNotFoundError."""
        respx.get(PDF_URL).mock(return_value=httpx.Response(404))

        with pytest.raises(DocumentNotFoundError, match="Document not found"):
            await fetch_and_extract_pdf(PDF_URL)

    @respx.mock
    @pytest.mark.anyio
    async def test_truncation_at_max_length(self, mock_pdfplumber):
        """Output is truncated when text exceeds max_length."""
        respx.get(PDF_URL).mock(
            return_value=httpx.Response(200, content=b"%PDF-fake")
        )
        long_text = "A" * 5000
        mock_pdfplumber([long_text])

        result = await fetch_and_extract_pdf(PDF_URL, max_length=200)

        assert "Truncated to 200 chars" in result
        # The body text portion should be at most 200 chars
        # (header is separate, text is truncated before header is prepended)
        body = result.split("\n\n", 1)[1]
        assert len(body) <= 200

    @respx.mock
    @pytest.mark.anyio
    async def test_ocr_fallback_when_available(self, mock_pdfplumber, monkeypatch):
        """When pdfplumber returns < 100 chars and OCR is available, OCR is used."""
        respx.get(PDF_URL).mock(
            return_value=httpx.Response(200, content=b"%PDF-fake")
        )
        mock_pdfplumber(["tiny"])  # < 100 chars triggers OCR path

        monkeypatch.setattr("fda_mcp.documents.fetcher.OCR_AVAILABLE", True)

        mock_ocr_called = False

        def fake_ocr(pdf_path, max_pages=20):
            nonlocal mock_ocr_called
            mock_ocr_called = True
            return "OCR extracted text that is long enough to be useful in tests"

        monkeypatch.setattr(
            "fda_mcp.documents.fetcher._extract_with_ocr", fake_ocr
        )

        result = await fetch_and_extract_pdf(PDF_URL)

        assert mock_ocr_called
        assert "Extraction: OCR (scanned document)" in result
        assert "OCR extracted text" in result

    @respx.mock
    @pytest.mark.anyio
    async def test_scanned_doc_no_ocr_message(self, mock_pdfplumber, monkeypatch):
        """When pdfplumber returns < 100 chars and OCR is NOT available, show install hint."""
        respx.get(PDF_URL).mock(
            return_value=httpx.Response(200, content=b"%PDF-fake")
        )
        mock_pdfplumber(["tiny"])

        monkeypatch.setattr("fda_mcp.documents.fetcher.OCR_AVAILABLE", False)

        result = await fetch_and_extract_pdf(PDF_URL)

        assert "scanned document" in result
        assert "tesseract" in result.lower()

    @respx.mock
    @pytest.mark.anyio
    async def test_no_truncation_when_within_limit(self, mock_pdfplumber):
        """No truncation message when text fits within max_length."""
        respx.get(PDF_URL).mock(
            return_value=httpx.Response(200, content=b"%PDF-fake")
        )
        mock_pdfplumber(["Short text that is long enough to not trigger OCR. " * 5])

        result = await fetch_and_extract_pdf(PDF_URL, max_length=8000)

        assert "Truncated" not in result
