"""PDF download and text extraction with OCR fallback."""

import os
import shutil
import tempfile

import httpx
import pdfplumber

from fda_mcp.config import config
from fda_mcp.errors import DocumentNotFoundError

_TESSERACT_AVAILABLE = shutil.which("tesseract") is not None
_PDFTOPPM_AVAILABLE = shutil.which("pdftoppm") is not None
OCR_AVAILABLE = _TESSERACT_AVAILABLE and _PDFTOPPM_AVAILABLE


def _extract_with_pdfplumber(pdf_path: str) -> tuple[str, int]:
    """Extract text using pdfplumber. Returns (text, page_count)."""
    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += (page.extract_text() or "") + "\n"
        return text, len(pdf.pages)


def _extract_with_ocr(pdf_path: str, max_pages: int = 20) -> str:
    """OCR fallback for scanned PDFs. Requires tesseract + poppler."""
    import pytesseract
    from pdf2image import convert_from_path

    images = convert_from_path(pdf_path, last_page=max_pages)
    text = ""
    for i, img in enumerate(images):
        text += f"\n--- Page {i + 1} ---\n"
        text += pytesseract.image_to_string(img)
    return text


async def fetch_and_extract_pdf(url: str, max_length: int = 8000) -> str:
    """Download a PDF from a URL and extract its text content.

    Uses pdfplumber for machine-generated PDFs, falls back to OCR
    for scanned documents (when tesseract + poppler are available).

    Args:
        url: URL to the PDF document.
        max_length: Maximum characters of text to return.

    Returns:
        Extracted text with metadata header.

    Raises:
        DocumentNotFoundError: If the PDF is not found (404).
    """
    async with httpx.AsyncClient(
        timeout=config.pdf_timeout, follow_redirects=True
    ) as client:
        response = await client.get(url)
        if response.status_code == 404:
            raise DocumentNotFoundError(url)
        response.raise_for_status()

    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
        tmp.write(response.content)
        tmp_path = tmp.name

    try:
        text, page_count = _extract_with_pdfplumber(tmp_path)

        extraction_method = "text extraction"
        if len(text.strip()) < 100 and OCR_AVAILABLE:
            text = _extract_with_ocr(tmp_path)
            extraction_method = "OCR (scanned document)"
        elif len(text.strip()) < 100 and not OCR_AVAILABLE:
            return (
                f"Source: {url}\n"
                f"Pages: {page_count}\n"
                f"This appears to be a scanned document. "
                f"Text extraction returned no content.\n"
                f"Install tesseract-ocr and poppler-utils for OCR support:\n"
                f"  macOS: brew install tesseract poppler\n"
                f"  Linux: apt install tesseract-ocr poppler-utils\n"
            )
    finally:
        os.unlink(tmp_path)

    truncated = len(text) > max_length
    text = text[:max_length]

    header = f"Source: {url}\nPages: {page_count}\nExtraction: {extraction_method}\n"
    if truncated:
        header += (
            f"[Truncated to {max_length} chars. Full document is longer. "
            f"Call again with a larger max_length to see more.]\n"
        )
    return header + "\n" + text
