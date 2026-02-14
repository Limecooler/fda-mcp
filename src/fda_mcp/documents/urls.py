"""URL pattern construction for FDA decision documents."""

import re

from fda_mcp.errors import InvalidIdentifierError


def build_document_url(
    document_type: str,
    submission_number: str,
    supplement_number: str | None = None,
) -> str:
    """Construct FDA document URL from type and identifier.

    Args:
        document_type: One of 510k_summary, denovo_decision,
            pma_approval, pma_ssed, pma_supplement
        submission_number: FDA identifier (K######, DEN######, P######)
        supplement_number: Supplement number for PMA supplements (e.g., "013")

    Returns:
        Full URL to the FDA document PDF.

    Raises:
        InvalidIdentifierError: If identifier format is invalid.
    """
    submission_number = submission_number.strip().upper()

    if document_type == "510k_summary":
        if not re.match(r"^K\d{6,7}$", submission_number):
            raise InvalidIdentifierError(
                submission_number, "K followed by 6-7 digits (e.g., K213456)"
            )
        return (
            f"https://www.accessdata.fda.gov/cdrh_docs/reviews/"
            f"{submission_number}.pdf"
        )

    elif document_type == "denovo_decision":
        if not re.match(r"^DEN\d{6,7}$", submission_number):
            raise InvalidIdentifierError(
                submission_number,
                "DEN followed by 6-7 digits (e.g., DEN200001)",
            )
        return (
            f"https://www.accessdata.fda.gov/cdrh_docs/reviews/"
            f"{submission_number}.pdf"
        )

    elif document_type in ("pma_approval", "pma_ssed", "pma_supplement"):
        if not re.match(r"^P\d{6,7}$", submission_number):
            raise InvalidIdentifierError(
                submission_number,
                "P followed by 6-7 digits (e.g., P200001)",
            )
        yy = _extract_pma_year(submission_number)
        base = f"https://www.accessdata.fda.gov/cdrh_docs/pdf{yy}"

        if document_type == "pma_approval":
            return f"{base}/{submission_number}A.pdf"
        elif document_type == "pma_ssed":
            return f"{base}/{submission_number}B.pdf"
        elif document_type == "pma_supplement":
            if not supplement_number:
                from mcp.server.fastmcp.exceptions import ToolError

                raise ToolError(
                    "supplement_number is required for pma_supplement documents."
                )
            supplement_number = supplement_number.strip().zfill(3)
            return f"{base}/{submission_number}S{supplement_number}A.pdf"

    raise InvalidIdentifierError(document_type, "valid document_type")


def _extract_pma_year(pma_number: str) -> str:
    """Extract 2-digit year from PMA number.

    P200001 -> "20", P990001 -> "99", P050001 -> "05"
    """
    digits = pma_number[1:]
    return digits[:2]
