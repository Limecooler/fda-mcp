"""Response field extraction and flattening per endpoint.

Transforms raw OpenFDA JSON responses into concise, LLM-friendly text.
Each endpoint type has a custom summarizer that extracts the most useful fields
and flattens nested structures.
"""

import json


def summarize_response(endpoint: str, data: dict) -> str:
    """Summarize an OpenFDA API response for LLM consumption.

    Args:
        endpoint: The API path (e.g., "drug/event")
        data: Raw API response dict

    Returns:
        Formatted text summary with pagination info.
    """
    meta = data.get("meta", {})
    results = data.get("results", [])

    total = meta.get("results", {}).get("total", len(results))
    skip = meta.get("results", {}).get("skip", 0)
    showing = len(results)
    has_more = (skip + showing) < total

    header = f"Results: {showing} of {total} total"
    if has_more:
        header += f" (showing {skip + 1}-{skip + showing})"
        header += "\nMore results available — increase skip to paginate."
    if total > 100:
        header += (
            "\nTip: For large result sets, consider using count_records "
            "for aggregation instead of paging through results."
        )
    header += "\n"

    summarizer = _SUMMARIZERS.get(endpoint, _summarize_generic)
    records = [summarizer(r) for r in results]

    separator = "\n---\n"
    return header + separator.join(records)


def _summarize_drug_event(record: dict) -> str:
    """Flatten drug adverse event report."""
    lines = []
    lines.append(f"Report ID: {record.get('safetyreportid', 'N/A')}")
    lines.append(f"Date: {record.get('receiptdate', 'N/A')}")
    lines.append(f"Serious: {record.get('serious', 'N/A')}")

    patient = record.get("patient", {})
    reactions = patient.get("reaction", [])
    reaction_names = [r.get("reactionmeddrapt", "") for r in reactions]
    if reaction_names:
        lines.append(f"Reactions: {', '.join(reaction_names)}")

    drugs = patient.get("drug", [])
    for d in drugs[:5]:
        name = d.get("medicinalproduct", "Unknown")
        role = d.get("drugcharacterization", "")
        role_map = {"1": "Suspect", "2": "Concomitant", "3": "Interacting"}
        role_label = role_map.get(str(role), role)
        lines.append(f"  Drug: {name} ({role_label})")

    if len(drugs) > 5:
        lines.append(f"  ... and {len(drugs) - 5} more drugs")

    outcome = record.get("seriousnessdeath")
    if outcome == "1":
        lines.append("Outcome: Death reported")

    return "\n".join(lines)


def _summarize_drug_label(record: dict) -> str:
    """Summarize drug label, truncating long sections."""
    lines = []
    openfda = record.get("openfda", {})
    brand = openfda.get("brand_name", ["N/A"])
    generic = openfda.get("generic_name", ["N/A"])
    lines.append(f"Brand: {', '.join(brand) if isinstance(brand, list) else brand}")
    lines.append(
        f"Generic: {', '.join(generic) if isinstance(generic, list) else generic}"
    )
    lines.append(
        f"Manufacturer: {', '.join(openfda.get('manufacturer_name', ['N/A']))}"
    )

    sections = [
        "indications_and_usage",
        "dosage_and_administration",
        "warnings",
        "adverse_reactions",
        "contraindications",
        "drug_interactions",
    ]
    for section in sections:
        content = record.get(section)
        if content:
            text = content[0] if isinstance(content, list) else content
            if len(text) > 2000:
                text = text[:2000] + "... [truncated]"
            lines.append(f"\n{section.replace('_', ' ').title()}:\n{text}")

    return "\n".join(lines)


def _summarize_drug_ndc(record: dict) -> str:
    """Summarize NDC directory record."""
    lines = []
    lines.append(f"Product NDC: {record.get('product_ndc', 'N/A')}")
    lines.append(f"Brand: {record.get('brand_name', 'N/A')}")
    lines.append(f"Generic: {record.get('generic_name', 'N/A')}")
    lines.append(f"Dosage Form: {record.get('dosage_form', 'N/A')}")
    lines.append(f"Route: {record.get('route', 'N/A')}")

    ingredients = record.get("active_ingredients", [])
    for ing in ingredients:
        lines.append(
            f"  Ingredient: {ing.get('name', 'N/A')} "
            f"({ing.get('strength', 'N/A')})"
        )

    return "\n".join(lines)


def _summarize_enforcement(record: dict) -> str:
    """Summarize enforcement/recall record (shared by drug, device, food)."""
    lines = []
    lines.append(f"Recall Number: {record.get('recall_number', 'N/A')}")
    lines.append(f"Classification: {record.get('classification', 'N/A')}")
    lines.append(f"Status: {record.get('status', 'N/A')}")
    lines.append(f"Recalling Firm: {record.get('recalling_firm', 'N/A')}")
    lines.append(f"Product: {record.get('product_description', 'N/A')}")
    reason = record.get("reason_for_recall", "N/A")
    if len(str(reason)) > 500:
        reason = str(reason)[:500] + "... [truncated]"
    lines.append(f"Reason: {reason}")
    lines.append(
        f"Distribution: {record.get('distribution_pattern', 'N/A')}"
    )
    lines.append(f"Date: {record.get('report_date', 'N/A')}")
    return "\n".join(lines)


def _summarize_drugsfda(record: dict) -> str:
    """Summarize Drugs@FDA record."""
    lines = []
    lines.append(
        f"Application Number: {record.get('application_number', 'N/A')}"
    )
    lines.append(f"Sponsor: {record.get('sponsor_name', 'N/A')}")

    products = record.get("products", [])
    for p in products[:5]:
        lines.append(
            f"  Product: {p.get('brand_name', 'N/A')} — "
            f"{p.get('active_ingredients', 'N/A')}"
        )
        lines.append(
            f"    Dosage: {p.get('dosage_form', 'N/A')}, "
            f"Route: {p.get('route', 'N/A')}"
        )

    submissions = record.get("submissions", [])
    for s in submissions[:3]:
        lines.append(
            f"  Submission: {s.get('submission_type', '')} "
            f"{s.get('submission_number', '')} — "
            f"{s.get('submission_status', '')}"
        )

    return "\n".join(lines)


def _summarize_drug_shortage(record: dict) -> str:
    """Summarize drug shortage record."""
    lines = []
    lines.append(f"Generic Name: {record.get('generic_name', 'N/A')}")
    lines.append(f"Brand Name: {record.get('brand_name', 'N/A')}")
    lines.append(f"Status: {record.get('status', 'N/A')}")
    lines.append(f"Company: {record.get('company', 'N/A')}")
    lines.append(
        f"Presentation: {record.get('presentation', 'N/A')}"
    )
    return "\n".join(lines)


def _summarize_device_510k(record: dict) -> str:
    """Summarize 510(k) record."""
    lines = []
    lines.append(f"K Number: {record.get('k_number', 'N/A')}")
    lines.append(f"Device: {record.get('device_name', 'N/A')}")
    lines.append(f"Applicant: {record.get('applicant', 'N/A')}")
    lines.append(f"Decision: {record.get('decision_description', 'N/A')}")
    lines.append(f"Decision Date: {record.get('decision_date', 'N/A')}")
    lines.append(f"Product Code: {record.get('product_code', 'N/A')}")
    lines.append(
        f"Review Panel: {record.get('review_panel', 'N/A')}"
    )
    return "\n".join(lines)


def _summarize_device_pma(record: dict) -> str:
    """Summarize PMA record."""
    lines = []
    lines.append(f"PMA Number: {record.get('pma_number', 'N/A')}")
    lines.append(f"Trade Name: {record.get('trade_name', 'N/A')}")
    lines.append(f"Applicant: {record.get('applicant', 'N/A')}")
    lines.append(
        f"Decision: {record.get('decision_description', 'N/A')}"
    )
    lines.append(f"Decision Date: {record.get('decision_date', 'N/A')}")
    lines.append(f"Product Code: {record.get('product_code', 'N/A')}")
    lines.append(
        f"Advisory Committee: {record.get('advisory_committee_description', 'N/A')}"
    )
    return "\n".join(lines)


def _summarize_device_classification(record: dict) -> str:
    """Summarize device classification record."""
    lines = []
    lines.append(f"Product Code: {record.get('product_code', 'N/A')}")
    lines.append(f"Device Name: {record.get('device_name', 'N/A')}")
    lines.append(f"Device Class: {record.get('device_class', 'N/A')}")
    lines.append(
        f"Regulation Number: {record.get('regulation_number', 'N/A')}"
    )
    lines.append(
        f"Medical Specialty: {record.get('medical_specialty_description', 'N/A')}"
    )
    lines.append(f"Review Panel: {record.get('review_panel', 'N/A')}")
    return "\n".join(lines)


def _summarize_device_event(record: dict) -> str:
    """Flatten device adverse event report."""
    lines = []
    lines.append(
        f"Report Number: {record.get('mdr_report_key', 'N/A')}"
    )
    lines.append(f"Date: {record.get('date_received', 'N/A')}")
    lines.append(f"Event Type: {record.get('event_type', 'N/A')}")

    devices = record.get("device", [])
    for d in devices[:3]:
        lines.append(
            f"  Device: {d.get('generic_name', 'N/A')} "
            f"({d.get('brand_name', 'N/A')})"
        )
        lines.append(
            f"    Manufacturer: {d.get('manufacturer_d_name', 'N/A')}"
        )

    text_entries = record.get("mdr_text", [])
    for t in text_entries[:2]:
        text = t.get("text", "")
        if len(text) > 500:
            text = text[:500] + "... [truncated]"
        lines.append(f"  Narrative: {text}")

    patient = record.get("patient", [])
    if patient:
        outcomes = []
        for p in patient:
            seq = p.get("sequence_number_outcome", [])
            outcomes.extend(seq if isinstance(seq, list) else [seq])
        if outcomes:
            lines.append(f"  Patient Outcomes: {', '.join(str(o) for o in outcomes)}")

    return "\n".join(lines)


def _summarize_device_recall(record: dict) -> str:
    """Summarize device recall record."""
    lines = []
    lines.append(
        f"Recall Number: {record.get('res_event_number', 'N/A')}"
    )
    lines.append(
        f"Product Code: {record.get('product_code', 'N/A')}"
    )
    lines.append(f"Firm: {record.get('recalling_firm', 'N/A')}")
    lines.append(
        f"Root Cause: {record.get('root_cause_description', 'N/A')}"
    )
    lines.append(
        f"Action: {record.get('action', 'N/A')}"
    )
    lines.append(
        f"Product: {record.get('product_description', 'N/A')}"
    )
    return "\n".join(lines)


def _summarize_device_registration(record: dict) -> str:
    """Summarize device registration/listing record."""
    lines = []
    lines.append(
        f"Registration Number: {record.get('registration_number', 'N/A')}"
    )
    lines.append(f"Firm: {record.get('establishment_type', 'N/A')}")

    products = record.get("products", {})
    if isinstance(products, dict):
        lines.append(
            f"  Product Code: {products.get('product_code', 'N/A')}"
        )
        openfda = products.get("openfda", {})
        lines.append(
            f"  Device Name: {openfda.get('device_name', 'N/A')}"
        )
    elif isinstance(products, list):
        for p in products[:3]:
            lines.append(
                f"  Product Code: {p.get('product_code', 'N/A')}"
            )

    proprietary = record.get("proprietary_name", [])
    if proprietary:
        names = proprietary if isinstance(proprietary, list) else [proprietary]
        lines.append(f"  Proprietary Names: {', '.join(str(n) for n in names[:5])}")

    return "\n".join(lines)


def _summarize_device_udi(record: dict) -> str:
    """Summarize UDI record."""
    lines = []
    identifiers = record.get("identifiers", [])
    for ident in identifiers[:3]:
        lines.append(
            f"Identifier: {ident.get('id', 'N/A')} "
            f"(Issuing Agency: {ident.get('issuing_agency', 'N/A')})"
        )

    lines.append(
        f"Brand: {record.get('brand_name', 'N/A')}"
    )
    lines.append(
        f"Company: {record.get('company_name', 'N/A')}"
    )
    lines.append(
        f"Device Description: {record.get('device_description', 'N/A')}"
    )
    lines.append(
        f"Version/Model: {record.get('version_or_model_number', 'N/A')}"
    )
    lines.append(
        f"MRI Safety: {record.get('MRISafety', 'N/A')}"
    )
    return "\n".join(lines)


def _summarize_device_covid19(record: dict) -> str:
    """Summarize COVID-19 serology test record."""
    lines = []
    lines.append(f"Manufacturer: {record.get('manufacturer', 'N/A')}")
    lines.append(f"Device: {record.get('device', 'N/A')}")
    lines.append(f"Sensitivity: {record.get('sensitivity', 'N/A')}")
    lines.append(f"Specificity: {record.get('specificity', 'N/A')}")
    lines.append(f"Date Updated: {record.get('date_updated', 'N/A')}")
    return "\n".join(lines)


def _summarize_food_event(record: dict) -> str:
    """Summarize CAERS food adverse event report."""
    lines = []
    lines.append(f"Report Number: {record.get('report_number', 'N/A')}")
    lines.append(f"Date: {record.get('date_started', 'N/A')}")

    products = record.get("products", [])
    for p in products[:3]:
        lines.append(
            f"  Product: {p.get('name_brand', 'N/A')} ({p.get('role', 'N/A')})"
        )
        lines.append(f"    Industry: {p.get('industry_name', 'N/A')}")

    reactions = record.get("reactions", [])
    if reactions:
        lines.append(f"Reactions: {', '.join(reactions[:10])}")

    outcomes = record.get("outcomes", [])
    if outcomes:
        lines.append(f"Outcomes: {', '.join(outcomes[:5])}")

    return "\n".join(lines)


def _summarize_historical_document(record: dict) -> str:
    """Summarize historical FDA document."""
    lines = []
    lines.append(f"Title: {record.get('title', 'N/A')}")
    lines.append(f"Date: {record.get('date', 'N/A')}")
    lines.append(f"Type: {record.get('type', 'N/A')}")
    lines.append(f"URL: {record.get('url', 'N/A')}")
    return "\n".join(lines)


def _summarize_nsde(record: dict) -> str:
    """Summarize NDC/SPL data elements record."""
    lines = []
    lines.append(f"Product NDC: {record.get('product_ndc', 'N/A')}")
    lines.append(f"Package NDC: {record.get('package_ndc', 'N/A')}")
    lines.append(f"SPL ID: {record.get('spl_id', 'N/A')}")
    lines.append(
        f"Marketing Category: {record.get('marketing_category', 'N/A')}"
    )
    return "\n".join(lines)


def _summarize_substance(record: dict) -> str:
    """Summarize substance registration record."""
    lines = []
    lines.append(f"UNII: {record.get('unii', 'N/A')}")
    lines.append(
        f"Substance Name: {record.get('substance_name', 'N/A')}"
    )
    codes = record.get("codes", [])
    for c in codes[:3]:
        lines.append(
            f"  Code: {c.get('code', 'N/A')} ({c.get('code_system', 'N/A')})"
        )
    return "\n".join(lines)


def _summarize_unii(record: dict) -> str:
    """Summarize UNII record."""
    lines = []
    lines.append(f"UNII: {record.get('unii', 'N/A')}")
    lines.append(f"Display Name: {record.get('display_name', 'N/A')}")
    lines.append(f"Preferred Term: {record.get('preferred_term', 'N/A')}")
    lines.append(f"MF: {record.get('mf', 'N/A')}")
    lines.append(f"InChIKey: {record.get('inchikey', 'N/A')}")
    return "\n".join(lines)


def _summarize_generic(record: dict) -> str:
    """Fallback summarizer — compact JSON."""
    return json.dumps(record, indent=2, default=str)[:3000]


def summarize_count_response(data: dict) -> str:
    """Summarize a count/aggregation query response.

    Includes pre-calculated percentages and a narrative summary.
    """
    results = data.get("results", [])
    if not results:
        return "No count results returned."

    total = sum(r.get("count", 0) for r in results)
    lines = [f"Total across {len(results)} categories: {total:,}\n"]

    for r in results:
        term = r.get("term", "N/A")
        count = r.get("count", 0)
        pct = (count / total * 100) if total > 0 else 0
        lines.append(f"  {term}: {count:,} ({pct:.1f}%)")

    if results:
        top = results[0]
        top_term = top.get("term", "N/A")
        top_count = top.get("count", 0)
        top_pct = (top_count / total * 100) if total > 0 else 0
        lines.append(
            f"\nSummary: '{top_term}' is the most common value "
            f"with {top_count:,} occurrences ({top_pct:.1f}% of total)."
        )

    return "\n".join(lines)


_SUMMARIZERS: dict[str, callable] = {
    "drug/event": _summarize_drug_event,
    "drug/label": _summarize_drug_label,
    "drug/ndc": _summarize_drug_ndc,
    "drug/enforcement": _summarize_enforcement,
    "drug/drugsfda": _summarize_drugsfda,
    "drug/shortage": _summarize_drug_shortage,
    "device/510k": _summarize_device_510k,
    "device/pma": _summarize_device_pma,
    "device/classification": _summarize_device_classification,
    "device/enforcement": _summarize_enforcement,
    "device/event": _summarize_device_event,
    "device/recall": _summarize_device_recall,
    "device/registrationlisting": _summarize_device_registration,
    "device/udi": _summarize_device_udi,
    "device/covid19serology": _summarize_device_covid19,
    "food/enforcement": _summarize_enforcement,
    "food/event": _summarize_food_event,
    "other/historicaldocument": _summarize_historical_document,
    "other/nsde": _summarize_nsde,
    "other/substance": _summarize_substance,
    "other/unii": _summarize_unii,
}
