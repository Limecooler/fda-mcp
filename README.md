# FDA MCP Server

[![PyPI](https://img.shields.io/pypi/v/fda-mcp)](https://pypi.org/project/fda-mcp/)
[![Python](https://img.shields.io/pypi/pyversions/fda-mcp)](https://pypi.org/project/fda-mcp/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An [MCP](https://modelcontextprotocol.io/) server that provides LLM-optimized access to FDA data through the [OpenFDA API](https://open.fda.gov/) and direct FDA document retrieval. Covers all 21 OpenFDA endpoints plus regulatory decision documents (510(k) summaries, De Novo decisions, PMA approval letters).

## Quick Start

No clone or local build required. Install [uv](https://docs.astral.sh/uv/) and run directly from [PyPI](https://pypi.org/project/fda-mcp/):

```bash
uvx fda-mcp
```

That's it. The server starts on stdio and is ready for any MCP client.

## Usage with Claude Desktop

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "fda": {
      "command": "uvx",
      "args": ["fda-mcp"],
      "env": {
        "OPENFDA_API_KEY": "your-key-here"
      }
    }
  }
}
```

Config file location:
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

## Usage with Claude Code

Add directly from the command line:

```bash
claude mcp add fda -- uvx fda-mcp
```

To include an API key for higher rate limits:

```bash
claude mcp add fda -e OPENFDA_API_KEY=your-key-here -- uvx fda-mcp
```

Or add interactively within Claude Code using the `/mcp` slash command.

## API Key (Optional)

The `OPENFDA_API_KEY` environment variable is optional. Without it you get 40 requests/minute. With a free key from [open.fda.gov](https://open.fda.gov/apis/authentication/) you get 240 requests/minute.

## Features

- **4 MCP tools** — one unified search tool, count/aggregation, field discovery, and document retrieval
- **3 MCP resources** for query syntax help, endpoint reference, and field discovery
- **All 21 OpenFDA endpoints** accessible via a single `search_fda` tool with a `dataset` parameter
- **Server instructions** — query syntax and common mistakes are injected into every LLM context automatically
- **Actionable error messages** — inline syntax help, troubleshooting tips, and `.exact` suffix warnings
- **FDA decision documents** — downloads and extracts text from 510(k) summaries, De Novo decisions, PMA approvals, SSEDs, and supplements
- **OCR fallback** for scanned PDF documents (older FDA submissions)
- **Context-efficient responses** — summarized output, field discovery on demand, pagination guidance

## Tools

| Tool | Purpose |
|------|---------|
| `search_fda` | Search any of the 21 OpenFDA datasets. The `dataset` parameter selects the endpoint (e.g., `drug_adverse_events`, `device_510k`, `food_recalls`). Accepts `search`, `limit`, `skip`, and `sort`. |
| `count_records` | Aggregation queries on any endpoint. Returns counts with percentages and narrative summary. Warns when `.exact` suffix is missing on text fields. |
| `list_searchable_fields` | Returns searchable field names for any endpoint. Call before searching if unsure of field names. |
| `get_decision_document` | Fetches FDA regulatory decision PDFs and extracts text. Supports 510(k), De Novo, PMA, SSED, and supplement documents. |

### Dataset Values for `search_fda`

| Category | Datasets |
|----------|----------|
| Drug | `drug_adverse_events`, `drug_labels`, `drug_ndc`, `drug_approvals`, `drug_recalls`, `drug_shortages` |
| Device | `device_adverse_events`, `device_510k`, `device_pma`, `device_classification`, `device_recalls`, `device_recall_details`, `device_registration`, `device_udi`, `device_covid19_serology` |
| Food | `food_adverse_events`, `food_recalls` |
| Other | `historical_documents`, `substance_data`, `unii`, `nsde` |

### Resources (3)

| URI | Content |
|-----|---------|
| `fda://reference/query-syntax` | OpenFDA query syntax: AND/OR/NOT, wildcards, date ranges, exact matching |
| `fda://reference/endpoints` | All 21 endpoints with descriptions |
| `fda://reference/fields/{endpoint}` | Per-endpoint field reference |

## Example Queries

Once connected, you can ask Claude things like:

- "Search for adverse events related to OZEMPIC"
- "Find all Class I device recalls from 2024"
- "What are the most common adverse reactions reported for LIPITOR?"
- "Get the 510(k) summary for K213456"
- "Search for PMA approvals for cardiovascular devices"
- "How many drug recalls has Pfizer had? Break down by classification."
- "Find the drug label for metformin and summarize the warnings"
- "What COVID-19 serology tests has Abbott submitted?"

## Configuration

All configuration is via environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `OPENFDA_API_KEY` | *(none)* | API key for higher rate limits (240 vs 40 req/min) |
| `OPENFDA_TIMEOUT` | `30` | HTTP request timeout in seconds |
| `OPENFDA_MAX_CONCURRENT` | `4` | Max concurrent API requests |
| `FDA_PDF_TIMEOUT` | `60` | PDF download timeout in seconds |
| `FDA_PDF_MAX_LENGTH` | `8000` | Default max text characters extracted from PDFs |

## OpenFDA Query Syntax

The `search` parameter on all tools uses OpenFDA query syntax:

```
# AND
patient.drug.openfda.brand_name:"ASPIRIN"+AND+serious:1

# OR (space = OR)
brand_name:"ASPIRIN" brand_name:"IBUPROFEN"

# NOT
NOT+classification:"Class III"

# Date ranges
decision_date:[20230101+TO+20231231]

# Wildcards (trailing only, min 2 chars)
device_name:pulse*

# Exact matching (required for count queries)
patient.reaction.reactionmeddrapt.exact:"Nausea"
```

Use `list_searchable_fields` or the `fda://reference/query-syntax` resource for the full reference.

## Installation Options

### From PyPI (recommended)

```bash
# Run directly without installing
uvx fda-mcp

# Or install as a persistent tool
uv tool install fda-mcp

# Or install with pip
pip install fda-mcp
```

### From source

```bash
git clone https://github.com/Limecooler/fda-mcp.git
cd fda-mcp
uv sync
uv run fda-mcp
```

### Optional: OCR support for scanned PDFs

Many older FDA documents (pre-2010) are scanned images. To extract text from these:

```bash
# macOS
brew install tesseract poppler

# Linux (Debian/Ubuntu)
apt install tesseract-ocr poppler-utils
```

Without these, the server still works — it returns a helpful message when it encounters a scanned document it can't read.

## Development

```bash
# Install with dev dependencies
git clone https://github.com/Limecooler/fda-mcp.git
cd fda-mcp
uv sync --all-extras

# Run unit tests (187 tests, no network)
uv run pytest

# Run integration tests (hits real FDA API)
OPENFDA_TIMEOUT=60 uv run pytest -m integration

# Run a specific test file
uv run pytest tests/test_endpoints.py -v

# Start the server directly
uv run fda-mcp
```

### Project Structure

```
src/fda_mcp/
├── server.py              # FastMCP server entry point
├── config.py              # Environment-based configuration
├── errors.py              # Custom error types
├── openfda/
│   ├── endpoints.py       # Enum of all 21 endpoints
│   ├── client.py          # Async HTTP client with rate limiting
│   └── summarizer.py      # Response summarization per endpoint
├── documents/
│   ├── urls.py            # FDA document URL construction
│   └── fetcher.py         # PDF download + text extraction + OCR
├── tools/
│   ├── _helpers.py        # Shared helpers (limit clamping)
│   ├── search.py          # search_fda tool (all 21 endpoints)
│   ├── count.py           # count_records tool
│   ├── fields.py          # list_searchable_fields tool
│   └── decision_documents.py
└── resources/
    ├── query_syntax.py    # Query syntax reference
    ├── endpoints_resource.py
    └── field_definitions.py
```

## How It Works

### LLM Usability

The server is designed to be easy for LLMs to use correctly:

1. **Server instructions** — Query syntax, workflow guidance, and common mistakes are injected into every LLM context automatically via the MCP protocol (~210 tokens).

2. **Unified tool surface** — A single `search_fda` tool with a typed `dataset` parameter replaces 9 separate search tools, eliminating tool selection confusion.

3. **Actionable errors** — `InvalidSearchError` includes inline syntax quick reference. `NotFoundError` includes troubleshooting steps and the endpoint used. No more references to invisible MCP resources.

4. **Visible warnings** — Limit clamping and missing `.exact` suffix produce visible notes instead of silent fallbacks.

5. **Response summarization** — Each endpoint type has a custom summarizer that extracts key fields and flattens nested structures. Drug labels truncate sections to 2,000 chars. PDF text defaults to 8,000 chars.

6. **Field discovery via tool** — Instead of listing all searchable fields in tool descriptions (which would cost ~8,000-11,000 tokens of persistent context), the `list_searchable_fields` tool provides them on demand.

7. **Smart pagination** — Default page sizes are low (10 records). Responses include `total_results`, `showing`, and `has_more`. When results exceed 100, a tip suggests using `count_records` for aggregation.

### FDA Decision Documents

These documents are **not** available through the OpenFDA API. The server constructs URLs and fetches directly from `accessdata.fda.gov`:

| Document Type | URL Pattern |
|--------------|-------------|
| 510(k) summary | `https://www.accessdata.fda.gov/cdrh_docs/reviews/{K_NUMBER}.pdf` |
| De Novo decision | `https://www.accessdata.fda.gov/cdrh_docs/reviews/{DEN_NUMBER}.pdf` |
| PMA approval | `https://www.accessdata.fda.gov/cdrh_docs/pdf{YY}/{P_NUMBER}A.pdf` |
| PMA SSED | `https://www.accessdata.fda.gov/cdrh_docs/pdf{YY}/{P_NUMBER}B.pdf` |
| PMA supplement | `https://www.accessdata.fda.gov/cdrh_docs/pdf{YY}/{P_NUMBER}S{###}A.pdf` |

Text extraction uses `pdfplumber` for machine-generated PDFs, with automatic OCR fallback via `pytesseract` + `pdf2image` for scanned documents.

## License

MIT
