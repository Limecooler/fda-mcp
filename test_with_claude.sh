#!/usr/bin/env bash
#
# test_with_claude.sh — Diagnostic test script for FDA MCP server
#
# Runs 5 targeted prompts through the Claude CLI to verify the MCP server
# starts correctly and tools return expected output.
#
# IMPORTANT: Run from a regular terminal, NOT from within Claude Code.
#
# Usage: ./test_with_claude.sh
# Cost:  ~$0.15-0.30 total (5 Sonnet calls)

set -euo pipefail

# --- Detect nested Claude Code session ---
if [ -n "${CLAUDECODE:-}" ]; then
    echo "WARNING: Running inside a Claude Code session." >&2
    echo "MCP servers cannot spawn from nested sessions." >&2
    echo "Run this script from a regular terminal instead." >&2
    exit 1
fi

# --- Portable timeout (macOS lacks GNU timeout) ---
if command -v gtimeout &>/dev/null; then
    TIMEOUT_CMD="gtimeout"
elif command -v timeout &>/dev/null; then
    TIMEOUT_CMD="timeout"
else
    TIMEOUT_CMD=""
fi

run_with_timeout() {
    local secs=$1
    shift
    if [ -n "$TIMEOUT_CMD" ]; then
        "$TIMEOUT_CMD" "$secs" "$@"
    else
        "$@"
    fi
}

# --- Color output (disable if not a terminal) ---
if [ -t 1 ]; then
    GREEN='\033[0;32m'
    RED='\033[0;31m'
    BOLD='\033[1m'
    RESET='\033[0m'
else
    GREEN='' RED='' BOLD='' RESET=''
fi

# --- Prerequisites ---
check_prereq() {
    if ! command -v "$1" &>/dev/null; then
        echo -e "${RED}Error: '$1' is not installed or not in PATH.${RESET}" >&2
        exit 1
    fi
}
check_prereq claude
check_prereq jq
check_prereq uvx

echo -e "${BOLD}FDA MCP Server — Claude CLI Diagnostic Tests${RESET}"
echo "============================================="
if [ -z "$TIMEOUT_CMD" ]; then
    echo "(No timeout command found — install coreutils for timeouts)"
fi
echo ""

# --- Temp MCP config ---
CONFIG_FILE=$(mktemp /tmp/fda-mcp-test-XXXXXX)
mv "$CONFIG_FILE" "${CONFIG_FILE}.json"
CONFIG_FILE="${CONFIG_FILE}.json"
cat > "$CONFIG_FILE" <<'EOF'
{
  "mcpServers": {
    "fda": {
      "command": "uvx",
      "args": ["fda-mcp"]
    }
  }
}
EOF
trap 'rm -f "$CONFIG_FILE"' EXIT

PASSED=0
FAILED=0
TOTAL=5
TOTAL_COST=0

# --- Test runner ---
# Usage: run_test "Test Name" "prompt" "expected1" "expected2" ...
run_test() {
    local test_name="$1"
    local prompt="$2"
    shift 2
    local expected=("$@")

    echo -e "${BOLD}[$((PASSED + FAILED + 1))/$TOTAL] $test_name${RESET}"
    echo "  Prompt: ${prompt:0:100}..."

    local raw_output
    if ! raw_output=$(run_with_timeout 120 claude -p "$prompt" \
        --mcp-config "$CONFIG_FILE" \
        --strict-mcp-config \
        --output-format json \
        --allowedTools "mcp__fda__*" \
        --dangerously-skip-permissions \
        --model sonnet 2>/dev/null); then
        echo -e "  ${RED}FAIL${RESET} — claude command failed or timed out"
        FAILED=$((FAILED + 1))
        echo ""
        return
    fi

    # Extract fields from JSON output
    local result cost turns
    result=$(echo "$raw_output" | jq -r '.result // empty' 2>/dev/null)
    cost=$(echo "$raw_output" | jq -r '.total_cost_usd // empty' 2>/dev/null)
    turns=$(echo "$raw_output" | jq -r '.num_turns // empty' 2>/dev/null)

    if [ -z "$result" ]; then
        if [ "${turns:-0}" -ge 2 ] 2>/dev/null; then
            echo -e "  ${RED}FAIL${RESET} — tool was called (${turns} turns) but Claude returned empty text"
        else
            echo -e "  ${RED}FAIL${RESET} — could not extract .result from JSON output"
        fi
        echo "  Raw output (first 300 chars): ${raw_output:0:300}"
        FAILED=$((FAILED + 1))
        echo ""
        return
    fi
    echo ""
    echo "  --- Response (first 500 chars) ---"
    echo "$result" | head -c 500 | sed 's/^/  | /'
    echo ""
    echo "  ---"
    if [ -n "$cost" ] || [ -n "$turns" ]; then
        echo "  (${turns:-?} turn(s), \$${cost:-?})"
        if [ -n "$cost" ]; then
            TOTAL_COST=$(echo "$TOTAL_COST + $cost" | bc 2>/dev/null || echo "$TOTAL_COST")
        fi
    fi
    echo ""

    # Check each expected string (case-insensitive)
    local all_passed=true
    for exp in "${expected[@]}"; do
        if echo "$result" | grep -qi "$exp"; then
            echo -e "  ${GREEN}OK${RESET} — found: \"$exp\""
        else
            echo -e "  ${RED}MISSING${RESET} — expected: \"$exp\""
            all_passed=false
        fi
    done

    if $all_passed; then
        echo -e "  ${GREEN}PASS${RESET}"
        PASSED=$((PASSED + 1))
    else
        echo -e "  ${RED}FAIL${RESET}"
        FAILED=$((FAILED + 1))
    fi
    echo ""
}

# --- Test 1: Drug label search ---
run_test "Drug label search (search_fda)" \
    'Call the search_fda tool with dataset="drug_labels", search='"'"'openfda.brand_name:"ASPIRIN"'"'"' and limit=2. Print the complete tool result text in your response verbatim.' \
    "Brand:" "Generic:"

# --- Test 2: Count records ---
run_test "Count records (count_records)" \
    'Call the count_records tool with endpoint="drug/event", count_field="patient.reaction.reactionmeddrapt.exact", limit=5. Print the complete tool result text in your response verbatim.' \
    "Total across" "%" "most common value"

# --- Test 3: Field discovery (list_searchable_fields) ---
run_test "Field discovery (list_searchable_fields)" \
    'Call the list_searchable_fields tool with endpoint="drug/event" and category="common". Print the complete tool result text in your response verbatim.' \
    "patient.drug.openfda.brand_name" "patient.reaction.reactionmeddrapt"

# --- Test 4: Adverse events search ---
run_test "Adverse event search (search_fda)" \
    'Call the search_fda tool with dataset="drug_adverse_events", search='"'"'patient.drug.openfda.brand_name:"IBUPROFEN"'"'"', limit=2. Print the complete tool result text in your response verbatim.' \
    "Report ID:" "Reactions:"

# --- Test 5: Device 510(k) search ---
run_test "Device 510(k) search (search_fda)" \
    'Call the search_fda tool with dataset="device_510k", search='"'"'device_name:"pulse+oximeter"'"'"', limit=2. Print the complete tool result text in your response verbatim.' \
    "K Number:" "Device:"

# --- Summary ---
echo "============================================="
COST_DISPLAY=$(printf '%.4f' "$TOTAL_COST" 2>/dev/null || echo "$TOTAL_COST")
if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}${BOLD}All $TOTAL tests passed!${RESET} (total cost: \$$COST_DISPLAY)"
else
    echo -e "${BOLD}Results: ${GREEN}$PASSED passed${RESET}, ${RED}$FAILED failed${RESET} (out of $TOTAL)"
    echo ""
    echo "Troubleshooting tips:"
    echo "  1. Ensure 'uvx fda-mcp' starts without errors: uvx fda-mcp --help"
    echo "  2. Check Claude CLI is authenticated: claude --version"
    echo "  3. Try running a single test manually:"
    echo "     claude -p 'Use the list_searchable_fields tool with endpoint=\"drug/event\"' \\"
    echo "       --mcp-config /path/to/config.json --allowedTools 'mcp__fda__*' --dangerously-skip-permissions"
    echo "  4. Check MCP server logs for errors during tool execution"
    exit 1
fi
