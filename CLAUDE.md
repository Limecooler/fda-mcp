# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

FDA MCP — an MCP server providing access to FDA data via the OpenFDA API. Wraps all 21 OpenFDA endpoints plus FDA decision document retrieval into 12 MCP tools optimized for LLM consumption.

## Development Commands

- **Install dependencies**: `uv sync --all-extras`
- **Run server**: `uv run fda-mcp`
- **Run unit tests**: `uv run pytest`
- **Run integration tests** (hits real FDA API): `uv run pytest -m integration`
- **Run specific test file**: `uv run pytest tests/test_endpoints.py -v`

## Architecture

- **Language**: Python 3.11+, async throughout
- **MCP SDK**: `mcp` with FastMCP decorator API
- **HTTP Client**: `httpx` (async)
- **PDF Extraction**: `pdfplumber` + `pytesseract`/`pdf2image` OCR fallback
- **Transport**: stdio (standard for Claude Desktop / Claude Code)

### Source Layout

```
src/fda_mcp/
├── server.py          -- FastMCP server entry point
├── config.py          -- Environment-based configuration
├── errors.py          -- Custom error types
├── openfda/           -- OpenFDA API client layer
│   ├── endpoints.py   -- Enum of all 21 endpoints
│   ├── client.py      -- Async HTTP client with rate limiting
│   └── summarizer.py  -- Response summarization per endpoint
├── documents/         -- FDA decision document retrieval
│   ├── urls.py        -- URL pattern construction
│   └── fetcher.py     -- PDF download + text extraction
├── tools/             -- 12 MCP tool handlers
│   ├── search.py      -- 9 search tools
│   ├── count.py       -- count_records tool
│   ├── fields.py      -- list_searchable_fields tool
│   └── decision_documents.py
└── resources/         -- 3 MCP resources
    ├── query_syntax.py
    ├── endpoints_resource.py
    └── field_definitions.py
```

## Configuration

- `OPENFDA_API_KEY` — optional API key for higher rate limits (240 req/min vs 40)
- `OPENFDA_TIMEOUT` — request timeout in seconds (default: 30)
- `OPENFDA_MAX_CONCURRENT` — max concurrent API requests (default: 4)
- `FDA_PDF_TIMEOUT` — PDF download timeout in seconds (default: 60)
- `FDA_PDF_MAX_LENGTH` — default max text chars from PDFs (default: 8000)

## Code Standards

- Python 3.11+ with type hints throughout
- Async functions for all I/O operations
- Tests use pytest + pytest-asyncio + respx for HTTP mocking
