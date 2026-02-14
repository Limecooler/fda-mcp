"""Tests for FDA document URL construction."""

import pytest
from mcp.server.fastmcp.exceptions import ToolError

from fda_mcp.documents.urls import build_document_url
from fda_mcp.errors import InvalidIdentifierError


class TestBuild510kSummaryUrl:
    def test_standard_k_number(self):
        url = build_document_url("510k_summary", "K213456")
        assert url == "https://www.accessdata.fda.gov/cdrh_docs/reviews/K213456.pdf"

    def test_case_insensitivity(self):
        url = build_document_url("510k_summary", "k213456")
        assert url == "https://www.accessdata.fda.gov/cdrh_docs/reviews/K213456.pdf"

    def test_strips_whitespace(self):
        url = build_document_url("510k_summary", "  K213456  ")
        assert url == "https://www.accessdata.fda.gov/cdrh_docs/reviews/K213456.pdf"

    def test_seven_digit_k_number(self):
        url = build_document_url("510k_summary", "K2134567")
        assert url == "https://www.accessdata.fda.gov/cdrh_docs/reviews/K2134567.pdf"

    def test_invalid_k_number_raises(self):
        with pytest.raises(InvalidIdentifierError, match="Invalid identifier"):
            build_document_url("510k_summary", "X213456")

    def test_too_few_digits_raises(self):
        with pytest.raises(InvalidIdentifierError):
            build_document_url("510k_summary", "K1234")

    def test_too_many_digits_raises(self):
        with pytest.raises(InvalidIdentifierError):
            build_document_url("510k_summary", "K12345678")


class TestBuildDenovoDecisionUrl:
    def test_standard_den_number(self):
        url = build_document_url("denovo_decision", "DEN200001")
        assert url == "https://www.accessdata.fda.gov/cdrh_docs/reviews/DEN200001.pdf"

    def test_case_insensitivity(self):
        url = build_document_url("denovo_decision", "den200001")
        assert url == "https://www.accessdata.fda.gov/cdrh_docs/reviews/DEN200001.pdf"

    def test_invalid_den_number_raises(self):
        with pytest.raises(InvalidIdentifierError):
            build_document_url("denovo_decision", "DEN12")

    def test_wrong_prefix_raises(self):
        with pytest.raises(InvalidIdentifierError):
            build_document_url("denovo_decision", "K213456")


class TestBuildPmaApprovalUrl:
    def test_year_20(self):
        url = build_document_url("pma_approval", "P200001")
        assert url == "https://www.accessdata.fda.gov/cdrh_docs/pdf20/P200001A.pdf"

    def test_year_99(self):
        url = build_document_url("pma_approval", "P990001")
        assert url == "https://www.accessdata.fda.gov/cdrh_docs/pdf99/P990001A.pdf"

    def test_year_05(self):
        url = build_document_url("pma_approval", "P050001")
        assert url == "https://www.accessdata.fda.gov/cdrh_docs/pdf05/P050001A.pdf"

    def test_case_insensitivity(self):
        url = build_document_url("pma_approval", "p200001")
        assert url == "https://www.accessdata.fda.gov/cdrh_docs/pdf20/P200001A.pdf"

    def test_invalid_pma_raises(self):
        with pytest.raises(InvalidIdentifierError):
            build_document_url("pma_approval", "PMA200001")


class TestBuildPmaSsedUrl:
    def test_standard(self):
        url = build_document_url("pma_ssed", "P200001")
        assert url == "https://www.accessdata.fda.gov/cdrh_docs/pdf20/P200001B.pdf"

    def test_year_99(self):
        url = build_document_url("pma_ssed", "P990001")
        assert url == "https://www.accessdata.fda.gov/cdrh_docs/pdf99/P990001B.pdf"


class TestBuildPmaSupplementUrl:
    def test_with_supplement_number(self):
        url = build_document_url("pma_supplement", "P200001", supplement_number="013")
        assert url == "https://www.accessdata.fda.gov/cdrh_docs/pdf20/P200001S013A.pdf"

    def test_supplement_number_zero_padded(self):
        url = build_document_url("pma_supplement", "P200001", supplement_number="5")
        assert url == "https://www.accessdata.fda.gov/cdrh_docs/pdf20/P200001S005A.pdf"

    def test_missing_supplement_number_raises_tool_error(self):
        with pytest.raises(ToolError, match="supplement_number is required"):
            build_document_url("pma_supplement", "P200001")

    def test_invalid_pma_raises(self):
        with pytest.raises(InvalidIdentifierError):
            build_document_url("pma_supplement", "INVALID", supplement_number="013")


class TestInvalidDocumentType:
    def test_unknown_type_raises(self):
        with pytest.raises(InvalidIdentifierError):
            build_document_url("unknown_type", "K213456")
