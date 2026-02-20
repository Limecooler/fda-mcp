"""Async HTTP client for the OpenFDA API with rate limiting."""

import asyncio

import httpx

from fda_mcp.config import config
from fda_mcp.errors import (
    InvalidSearchError,
    NotFoundError,
    OpenFDAError,
    RateLimitError,
)


class OpenFDAClient:
    """Async client for querying OpenFDA API endpoints."""

    BASE_URL = "https://api.fda.gov"

    def __init__(self) -> None:
        self._semaphore = asyncio.Semaphore(config.max_concurrent_requests)

    async def query(
        self,
        endpoint: str,
        search: str | None = None,
        count: str | None = None,
        limit: int | None = None,
        skip: int | None = None,
        sort: str | None = None,
    ) -> dict:
        """Query an OpenFDA endpoint.

        Args:
            endpoint: API path like "drug/event"
            search: OpenFDA search query string
            count: Field to count (for aggregation queries)
            limit: Max results to return (1-1000 for search, 1-1000 for count)
            skip: Number of results to skip
            sort: Sort field and direction

        Returns:
            Parsed JSON response dict with 'meta' and 'results' keys.

        Raises:
            NotFoundError: No results matched the query (HTTP 404)
            RateLimitError: Rate limit exceeded (HTTP 429)
            InvalidSearchError: Bad query syntax (HTTP 400)
            OpenFDAError: Other API errors
        """
        params: dict[str, str] = {}
        if config.api_key:
            params["api_key"] = config.api_key
        if search:
            params["search"] = search
        if count:
            params["count"] = count
        if limit is not None:
            params["limit"] = str(limit)
        if skip is not None:
            params["skip"] = str(skip)
        if sort:
            params["sort"] = sort

        url = f"{self.BASE_URL}/{endpoint}.json"

        async with self._semaphore:
            async with httpx.AsyncClient(
                timeout=config.request_timeout
            ) as client:
                try:
                    response = await client.get(url, params=params)
                except httpx.TimeoutException:
                    raise OpenFDAError(
                        f"Request timed out after {config.request_timeout}s. "
                        "Try a more specific search query or increase timeout."
                    )
                except httpx.ConnectError:
                    raise OpenFDAError(
                        "Could not connect to api.fda.gov. "
                        "Check your network connection."
                    )

                if response.status_code == 404:
                    raise NotFoundError(endpoint=endpoint)
                if response.status_code == 429:
                    raise RateLimitError()
                if response.status_code == 400:
                    body = response.json() if response.content else {}
                    detail = ""
                    if "error" in body:
                        detail = body["error"].get("message", "")
                    raise InvalidSearchError(detail)
                if response.status_code >= 500:
                    raise OpenFDAError(
                        f"OpenFDA server error (HTTP {response.status_code}). "
                        "The FDA API may be temporarily unavailable. "
                        "Try again shortly."
                    )
                response.raise_for_status()
                return response.json()


openfda_client = OpenFDAClient()
