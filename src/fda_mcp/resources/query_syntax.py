"""Query syntax reference resource."""

from fda_mcp.server import mcp

QUERY_SYNTAX_REFERENCE = """# OpenFDA Query Syntax

## Search Operators
- AND: field1:value1+AND+field2:value2
- OR:  field1:value1+field2:value2  (space = OR)
- NOT: NOT+field:value

## Wildcards
- Trailing only: field:val*  (min 2 chars before *)

## Date Ranges
- field:[20200101+TO+20231231]

## Exact Matching
- field.exact:"complete phrase"  (use with count queries)

## Quoting
- Phrases: field:"my phrase"
- Combine: field:"value one"+AND+field2:"value two"

## Numeric Ranges
- field:[1+TO+100]
- field:>10
- field:>=10

## Special Fields
- _exists_:field  (field has a value)

## Examples
- search=patient.drug.openfda.brand_name:"ASPIRIN"+AND+serious:1
- search=recalling_firm:"Pfizer"+AND+classification:"Class I"
- search=device_name:"pump"+AND+decision_date:[20230101+TO+20231231]
- count=patient.reaction.reactionmeddrapt.exact&limit=10
"""


@mcp.resource("fda://reference/query-syntax")
async def get_query_syntax() -> str:
    """OpenFDA query syntax reference with operators, wildcards, date ranges, and examples."""
    return QUERY_SYNTAX_REFERENCE
