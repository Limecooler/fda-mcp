"""Environment-based configuration for the FDA MCP server."""

import os


class Config:
    """Server configuration loaded from environment variables."""

    def __init__(self) -> None:
        self.api_key: str | None = os.environ.get("OPENFDA_API_KEY")
        self.request_timeout: float = float(
            os.environ.get("OPENFDA_TIMEOUT", "30.0")
        )
        self.max_concurrent_requests: int = int(
            os.environ.get("OPENFDA_MAX_CONCURRENT", "4")
        )
        self.pdf_timeout: float = float(
            os.environ.get("FDA_PDF_TIMEOUT", "60.0")
        )
        self.default_pdf_max_length: int = int(
            os.environ.get("FDA_PDF_MAX_LENGTH", "8000")
        )


config = Config()
