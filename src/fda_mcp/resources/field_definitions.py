"""Static field metadata per endpoint — used by list_searchable_fields tool
and the fda://reference/fields/{endpoint} resource template."""

from fda_mcp.server import mcp

# Field definitions: endpoint -> { field_name: { type, description } }
# "common" fields are the most frequently used subset.
# "all" includes everything in common plus additional fields.

_FIELD_DEFS: dict[str, dict[str, dict[str, dict[str, str]]]] = {
    "drug/event": {
        "common": {
            "patient.drug.openfda.brand_name": {
                "type": "string",
                "description": "Drug brand name",
            },
            "patient.drug.openfda.generic_name": {
                "type": "string",
                "description": "Drug generic name",
            },
            "patient.reaction.reactionmeddrapt": {
                "type": "string",
                "description": "Adverse reaction (MedDRA preferred term)",
            },
            "serious": {
                "type": "string",
                "description": "Serious report (1=yes, 2=no)",
            },
            "receiptdate": {
                "type": "date",
                "description": "Date report received (YYYYMMDD)",
            },
            "patient.drug.drugcharacterization": {
                "type": "string",
                "description": "Drug role (1=Suspect, 2=Concomitant, 3=Interacting)",
            },
            "seriousnessdeath": {
                "type": "string",
                "description": "Death reported (1=yes)",
            },
        },
        "all": {
            "safetyreportid": {
                "type": "string",
                "description": "Unique report ID",
            },
            "primarysource.qualification": {
                "type": "string",
                "description": (
                    "Reporter qualification (numeric). "
                    "1=Physician, 2=Pharmacist, 3=Other Health Professional, "
                    "4=Lawyer, 5=Consumer/Non-Health Professional"
                ),
            },
            "patient.patientonsetage": {
                "type": "string",
                "description": "Patient age at onset",
            },
            "patient.patientsex": {
                "type": "string",
                "description": "Patient sex (0=Unknown, 1=Male, 2=Female)",
            },
            "patient.drug.medicinalproduct": {
                "type": "string",
                "description": "Drug name as reported",
            },
            "patient.drug.drugindication": {
                "type": "string",
                "description": "Drug indication",
            },
            "occurcountry": {
                "type": "string",
                "description": "Country of occurrence",
            },
        },
    },
    "drug/label": {
        "common": {
            "openfda.brand_name": {
                "type": "string",
                "description": "Brand name",
            },
            "openfda.generic_name": {
                "type": "string",
                "description": "Generic name",
            },
            "openfda.manufacturer_name": {
                "type": "string",
                "description": "Manufacturer name",
            },
            "indications_and_usage": {
                "type": "string",
                "description": "Indications and usage text",
            },
            "warnings": {
                "type": "string",
                "description": "Warnings section text",
            },
        },
        "all": {
            "openfda.product_type": {
                "type": "string",
                "description": "Product type (OTC/Rx)",
            },
            "openfda.route": {
                "type": "string",
                "description": "Route of administration",
            },
            "dosage_and_administration": {
                "type": "string",
                "description": "Dosage info",
            },
            "adverse_reactions": {
                "type": "string",
                "description": "Adverse reactions section",
            },
            "contraindications": {
                "type": "string",
                "description": "Contraindications",
            },
            "drug_interactions": {
                "type": "string",
                "description": "Drug interactions",
            },
            "effective_time": {
                "type": "date",
                "description": "Label effective date",
            },
        },
    },
    "drug/ndc": {
        "common": {
            "brand_name": {
                "type": "string",
                "description": "Drug brand name",
            },
            "generic_name": {
                "type": "string",
                "description": "Drug generic name",
            },
            "product_ndc": {
                "type": "string",
                "description": "Product NDC code",
            },
            "dosage_form": {
                "type": "string",
                "description": "Dosage form",
            },
            "route": {
                "type": "string",
                "description": "Route of administration",
            },
        },
        "all": {
            "labeler_name": {
                "type": "string",
                "description": "Labeler/manufacturer name",
            },
            "active_ingredients.name": {
                "type": "string",
                "description": "Active ingredient name",
            },
            "active_ingredients.strength": {
                "type": "string",
                "description": "Active ingredient strength",
            },
            "product_type": {
                "type": "string",
                "description": "Product type",
            },
            "marketing_category": {
                "type": "string",
                "description": "Marketing category (NDA, ANDA, etc.)",
            },
        },
    },
    "drug/enforcement": {
        "common": {
            "recalling_firm": {
                "type": "string",
                "description": "Company initiating recall",
            },
            "classification": {
                "type": "string",
                "description": (
                    "Recall class. Values: \"Class I\" (most serious, "
                    "health hazard), \"Class II\" (less serious), "
                    "\"Class III\" (least serious)"
                ),
            },
            "status": {
                "type": "string",
                "description": "Recall status: Ongoing, Terminated, or Completed",
            },
            "reason_for_recall": {
                "type": "string",
                "description": "Reason for the recall",
            },
            "product_description": {
                "type": "string",
                "description": "Product description",
            },
        },
        "all": {
            "recall_number": {
                "type": "string",
                "description": "Recall event number",
            },
            "report_date": {
                "type": "date",
                "description": "Report date (YYYYMMDD)",
            },
            "distribution_pattern": {
                "type": "string",
                "description": "Distribution pattern",
            },
            "voluntary_mandated": {
                "type": "string",
                "description": (
                    "Voluntary or mandated. Values: "
                    "\"Voluntary: Firm initiated\", \"FDA Mandated\""
                ),
            },
            "state": {
                "type": "string",
                "description": "State of recalling firm (2-letter abbreviation)",
            },
        },
    },
    "drug/drugsfda": {
        "common": {
            "application_number": {
                "type": "string",
                "description": "Application number (NDA/ANDA/BLA)",
            },
            "sponsor_name": {
                "type": "string",
                "description": "Sponsor company name",
            },
            "products.brand_name": {
                "type": "string",
                "description": "Product brand name",
            },
            "products.active_ingredients": {
                "type": "string",
                "description": "Active ingredients",
            },
        },
        "all": {
            "products.dosage_form": {
                "type": "string",
                "description": "Dosage form",
            },
            "products.route": {
                "type": "string",
                "description": "Route",
            },
            "submissions.submission_type": {
                "type": "string",
                "description": "Submission type",
            },
            "submissions.submission_status": {
                "type": "string",
                "description": "Submission status",
            },
        },
    },
    "drug/shortage": {
        "common": {
            "generic_name": {
                "type": "string",
                "description": "Generic drug name",
            },
            "brand_name": {
                "type": "string",
                "description": "Brand name",
            },
            "status": {
                "type": "string",
                "description": "Shortage status",
            },
            "company": {
                "type": "string",
                "description": "Company name",
            },
        },
        "all": {
            "presentation": {
                "type": "string",
                "description": "Drug presentation/form",
            },
        },
    },
    "device/510k": {
        "common": {
            "k_number": {
                "type": "string",
                "description": "510(k) number (e.g., K213456)",
            },
            "device_name": {
                "type": "string",
                "description": "Device name",
            },
            "applicant": {
                "type": "string",
                "description": "Applicant/company name",
            },
            "advisory_committee": {
                "type": "string",
                "description": (
                    "FDA advisory committee (2-letter code). "
                    "AN=Anesthesiology, CH=Clinical Chemistry, CV=Cardiovascular, "
                    "DE=Dental, EN=Ear/Nose/Throat, GU=Gastroenterology/Urology, "
                    "HE=Hematology, HO=General Hospital, IM=Immunology, "
                    "MG=Medical Genetics, MI=Microbiology, NE=Neurology, "
                    "OB=Obstetrics/Gynecology, OP=Ophthalmic, OR=Orthopedic, "
                    "PA=Pathology, PM=Physical Medicine, RA=Radiology, "
                    "SU=General/Plastic Surgery, TX=Clinical Toxicology"
                ),
            },
            "advisory_committee_description": {
                "type": "string",
                "description": "Full name of advisory committee (e.g., 'Dental')",
            },
            "decision_code": {
                "type": "string",
                "description": (
                    "Decision code. SESE=Substantially Equivalent, "
                    "DENG=De Novo Granted, SN=Not Substantially Equivalent, "
                    "SESK=SE(Kit), SEKD=SE(Kit Device), SESD=SE(Split Device), "
                    "SESU=SE(Unknown), SESP=SE(Split Pending), PT=Petition"
                ),
            },
            "decision_description": {
                "type": "string",
                "description": "Full text of decision (e.g., 'Substantially Equivalent')",
            },
            "decision_date": {
                "type": "date",
                "description": "Decision date (YYYYMMDD)",
            },
            "product_code": {
                "type": "string",
                "description": "Product classification code (3-letter, e.g., DQA)",
            },
        },
        "all": {
            "review_panel": {
                "type": "string",
                "description": (
                    "Review panel (same 2-letter codes as advisory_committee). "
                    "Note: quote 'OR' in queries since OR is a reserved operator"
                ),
            },
            "clearance_type": {
                "type": "string",
                "description": (
                    "Clearance type: Traditional, Special, Abbreviated, "
                    "Direct, Post-NSE, Dual Track"
                ),
            },
            "statement_or_summary": {
                "type": "string",
                "description": "Whether a Summary or Statement was filed",
            },
            "date_received": {
                "type": "date",
                "description": "Date received (YYYYMMDD)",
            },
            "third_party_flag": {
                "type": "string",
                "description": "Third party review (Y/N)",
            },
        },
    },
    "device/pma": {
        "common": {
            "pma_number": {
                "type": "string",
                "description": "PMA number (e.g., P140017)",
            },
            "trade_name": {
                "type": "string",
                "description": "Device trade name",
            },
            "applicant": {
                "type": "string",
                "description": "Applicant/company name",
            },
            "advisory_committee": {
                "type": "string",
                "description": (
                    "FDA advisory committee (2-letter code). "
                    "Same codes as device/510k: AN, CH, CV, DE, EN, GU, HE, "
                    "HO, IM, MG, MI, NE, OB, OP, OR, PA, PM, RA, SU, TX"
                ),
            },
            "advisory_committee_description": {
                "type": "string",
                "description": "Full name of advisory committee (e.g., 'Cardiovascular')",
            },
            "decision_code": {
                "type": "string",
                "description": "Decision code (e.g., APPR=Approved)",
            },
            "decision_description": {
                "type": "string",
                "description": "Full text of decision",
            },
            "decision_date": {
                "type": "date",
                "description": "Decision date (YYYYMMDD)",
            },
            "product_code": {
                "type": "string",
                "description": "Product classification code",
            },
        },
        "all": {
            "supplement_number": {
                "type": "string",
                "description": "Supplement number (e.g., S042)",
            },
            "supplement_type": {
                "type": "string",
                "description": (
                    "Supplement type: 30-Day Notice, Normal 180 Day Track, "
                    "Real-Time Process, Panel Track, etc."
                ),
            },
        },
    },
    "device/classification": {
        "common": {
            "product_code": {
                "type": "string",
                "description": "Product classification code (3-letter, e.g., DQA)",
            },
            "device_name": {
                "type": "string",
                "description": "Device name",
            },
            "device_class": {
                "type": "string",
                "description": (
                    "Device class. 1=Class I, 2=Class II, 3=Class III, "
                    "f=HDE (Humanitarian Device Exemption), U=Unclassified, "
                    "N=Not classified"
                ),
            },
            "regulation_number": {
                "type": "string",
                "description": "CFR regulation number (e.g., 872.3275)",
            },
            "medical_specialty_description": {
                "type": "string",
                "description": (
                    "Medical specialty (e.g., 'Dental', 'Cardiovascular'). "
                    "Matches advisory_committee descriptions from device/510k"
                ),
            },
            "review_panel": {
                "type": "string",
                "description": (
                    "Review panel (same 2-letter codes as device/510k advisory_committee). "
                    "AN, CH, CV, DE, EN, GU, HE, HO, IM, MG, MI, NE, OB, OP, "
                    "OR, PA, PM, RA, SU, TX. Note: quote 'OR' in queries"
                ),
            },
        },
        "all": {
            "submission_type_id": {
                "type": "string",
                "description": (
                    "Submission type ID (numeric). "
                    "1=510(k), 2=PMA, 3=Contact FDA, 4=510(k) Exempt, "
                    "6=De Novo, 7=HDE, 8=Emergency Use"
                ),
            },
            "definition": {
                "type": "string",
                "description": "Device definition text",
            },
            "implant_flag": {
                "type": "string",
                "description": "Is an implant (Y/N)",
            },
            "life_sustain_support_flag": {
                "type": "string",
                "description": "Life sustaining/supporting (Y/N)",
            },
            "gmp_exempt_flag": {
                "type": "string",
                "description": "GMP exempt (Y/N)",
            },
            "summary_malfunction_reporting": {
                "type": "string",
                "description": "Summary malfunction reporting (Eligible/Ineligible)",
            },
            "third_party_flag": {
                "type": "string",
                "description": "Third party review eligible (Y/N)",
            },
        },
    },
    "device/enforcement": {
        "common": {
            "recalling_firm": {
                "type": "string",
                "description": "Company initiating recall",
            },
            "classification": {
                "type": "string",
                "description": (
                    "Recall class. Values: \"Class I\" (most serious), "
                    "\"Class II\", \"Class III\" (least serious)"
                ),
            },
            "status": {
                "type": "string",
                "description": "Recall status: Ongoing, Terminated, or Completed",
            },
            "reason_for_recall": {
                "type": "string",
                "description": "Recall reason",
            },
            "product_description": {
                "type": "string",
                "description": "Product description",
            },
        },
        "all": {
            "recall_number": {
                "type": "string",
                "description": "Recall number",
            },
            "report_date": {
                "type": "date",
                "description": "Report date (YYYYMMDD)",
            },
            "distribution_pattern": {
                "type": "string",
                "description": "Distribution pattern",
            },
            "voluntary_mandated": {
                "type": "string",
                "description": (
                    "Voluntary or mandated. Values: "
                    "\"Voluntary: Firm initiated\", \"FDA Mandated\""
                ),
            },
        },
    },
    "device/event": {
        "common": {
            "device.generic_name": {
                "type": "string",
                "description": "Device generic name",
            },
            "device.brand_name": {
                "type": "string",
                "description": "Device brand name",
            },
            "event_type": {
                "type": "string",
                "description": "Event type",
            },
            "date_received": {
                "type": "date",
                "description": "Date received",
            },
            "device.manufacturer_d_name": {
                "type": "string",
                "description": "Manufacturer name",
            },
        },
        "all": {
            "mdr_report_key": {
                "type": "string",
                "description": "Report key",
            },
            "device.product_code": {
                "type": "string",
                "description": "Product code",
            },
            "type_of_report": {
                "type": "string",
                "description": "Report type",
            },
        },
    },
    "device/recall": {
        "common": {
            "product_code": {
                "type": "string",
                "description": "Product code",
            },
            "recalling_firm": {
                "type": "string",
                "description": "Recalling firm",
            },
            "root_cause_description": {
                "type": "string",
                "description": "Root cause",
            },
            "product_description": {
                "type": "string",
                "description": "Product description",
            },
        },
        "all": {
            "res_event_number": {
                "type": "string",
                "description": "Event number",
            },
            "action": {
                "type": "string",
                "description": "Action taken",
            },
        },
    },
    "device/registrationlisting": {
        "common": {
            "registration_number": {
                "type": "string",
                "description": "Registration number",
            },
            "establishment_type": {
                "type": "string",
                "description": "Establishment type",
            },
            "proprietary_name": {
                "type": "string",
                "description": "Proprietary name",
            },
            "products.product_code": {
                "type": "string",
                "description": "Product code",
            },
        },
        "all": {
            "products.openfda.device_name": {
                "type": "string",
                "description": "Device name",
            },
            "products.openfda.device_class": {
                "type": "string",
                "description": "Device class",
            },
        },
    },
    "device/udi": {
        "common": {
            "brand_name": {
                "type": "string",
                "description": "Brand name",
            },
            "company_name": {
                "type": "string",
                "description": "Company name",
            },
            "device_description": {
                "type": "string",
                "description": "Device description",
            },
            "version_or_model_number": {
                "type": "string",
                "description": "Version or model number",
            },
        },
        "all": {
            "identifiers.id": {
                "type": "string",
                "description": "Device identifier",
            },
            "identifiers.issuing_agency": {
                "type": "string",
                "description": "Issuing agency",
            },
            "MRISafety": {
                "type": "string",
                "description": "MRI safety status",
            },
        },
    },
    "device/covid19serology": {
        "common": {
            "manufacturer": {
                "type": "string",
                "description": "Test manufacturer",
            },
            "device": {
                "type": "string",
                "description": "Test device name",
            },
            "sensitivity": {
                "type": "string",
                "description": "Test sensitivity",
            },
            "specificity": {
                "type": "string",
                "description": "Test specificity",
            },
        },
        "all": {
            "date_updated": {
                "type": "date",
                "description": "Date updated",
            },
        },
    },
    "food/enforcement": {
        "common": {
            "recalling_firm": {
                "type": "string",
                "description": "Company initiating recall",
            },
            "classification": {
                "type": "string",
                "description": (
                    "Recall class. Values: \"Class I\" (most serious), "
                    "\"Class II\", \"Class III\" (least serious)"
                ),
            },
            "status": {
                "type": "string",
                "description": "Recall status: Ongoing, Terminated, or Completed",
            },
            "reason_for_recall": {
                "type": "string",
                "description": "Recall reason",
            },
            "product_description": {
                "type": "string",
                "description": "Product description",
            },
        },
        "all": {
            "recall_number": {
                "type": "string",
                "description": "Recall number",
            },
            "report_date": {
                "type": "date",
                "description": "Report date (YYYYMMDD)",
            },
            "distribution_pattern": {
                "type": "string",
                "description": "Distribution pattern",
            },
            "voluntary_mandated": {
                "type": "string",
                "description": (
                    "Voluntary or mandated. Values: "
                    "\"Voluntary: Firm initiated\", \"FDA Mandated\""
                ),
            },
        },
    },
    "food/event": {
        "common": {
            "products.name_brand": {
                "type": "string",
                "description": "Product brand name",
            },
            "products.industry_name": {
                "type": "string",
                "description": "Industry name",
            },
            "reactions": {
                "type": "string",
                "description": "Reported reactions",
            },
            "outcomes": {
                "type": "string",
                "description": "Patient outcomes",
            },
        },
        "all": {
            "report_number": {
                "type": "string",
                "description": "CAERS report number",
            },
            "date_started": {
                "type": "date",
                "description": "Event start date",
            },
            "products.role": {
                "type": "string",
                "description": "Product role",
            },
        },
    },
    "other/historicaldocument": {
        "common": {
            "title": {
                "type": "string",
                "description": "Document title",
            },
            "date": {
                "type": "date",
                "description": "Document date",
            },
            "type": {
                "type": "string",
                "description": "Document type",
            },
        },
        "all": {
            "url": {
                "type": "string",
                "description": "Document URL",
            },
        },
    },
    "other/nsde": {
        "common": {
            "product_ndc": {
                "type": "string",
                "description": "Product NDC",
            },
            "package_ndc": {
                "type": "string",
                "description": "Package NDC",
            },
            "marketing_category": {
                "type": "string",
                "description": "Marketing category",
            },
        },
        "all": {
            "spl_id": {
                "type": "string",
                "description": "SPL ID",
            },
        },
    },
    "other/substance": {
        "common": {
            "substance_name": {
                "type": "string",
                "description": "Substance name",
            },
            "unii": {
                "type": "string",
                "description": "UNII code",
            },
        },
        "all": {
            "codes.code": {
                "type": "string",
                "description": "Code value",
            },
            "codes.code_system": {
                "type": "string",
                "description": "Code system",
            },
        },
    },
    "other/unii": {
        "common": {
            "unii": {
                "type": "string",
                "description": "UNII code",
            },
            "display_name": {
                "type": "string",
                "description": "Display name",
            },
            "preferred_term": {
                "type": "string",
                "description": "Preferred term",
            },
        },
        "all": {
            "mf": {
                "type": "string",
                "description": "Molecular formula",
            },
            "inchikey": {
                "type": "string",
                "description": "InChIKey",
            },
        },
    },
}


def get_fields(
    endpoint: str, category: str = "common"
) -> dict[str, dict[str, str]]:
    """Get field definitions for an endpoint.

    Args:
        endpoint: API path (e.g., "drug/event")
        category: "common" or "all"

    Returns:
        Dict of field_name -> {type, description}
    """
    ep_fields = _FIELD_DEFS.get(endpoint, {})
    common = ep_fields.get("common", {})
    if category == "common":
        return common
    # "all" merges common + additional fields
    all_fields = dict(common)
    all_fields.update(ep_fields.get("all", {}))
    return all_fields


def get_fields_text(endpoint: str) -> str:
    """Get formatted field reference text for an endpoint."""
    fields = get_fields(endpoint, "all")
    if not fields:
        return f"No field definitions available for {endpoint}."

    lines = [f"# Fields for {endpoint}\n"]
    for name, info in fields.items():
        field_type = info.get("type", "string")
        desc = info.get("description", "")
        lines.append(f"- **{name}** ({field_type}): {desc}")
    return "\n".join(lines)


# Resource template for per-endpoint field reference
@mcp.resource("fda://reference/fields/{endpoint_path}")
async def get_fields_resource(endpoint_path: str) -> str:
    """Field reference for a specific OpenFDA endpoint."""
    # The endpoint_path comes as "drug/event" etc.
    return get_fields_text(endpoint_path)
