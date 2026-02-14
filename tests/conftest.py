"""Shared test fixtures — mock HTTP responses for all 21 endpoints."""

import pytest
import respx
import httpx

BASE_URL = "https://api.fda.gov"


def _wrap_response(results: list, total: int | None = None) -> dict:
    """Wrap results in standard OpenFDA response envelope."""
    if total is None:
        total = len(results)
    return {
        "meta": {
            "disclaimer": "Test data",
            "terms": "https://open.fda.gov/terms/",
            "license": "https://open.fda.gov/license/",
            "last_updated": "2024-01-01",
            "results": {
                "skip": 0,
                "limit": 10,
                "total": total,
            },
        },
        "results": results,
    }


# -- Drug endpoint sample responses --

DRUG_EVENT_RESPONSE = _wrap_response([
    {
        "safetyreportid": "10001",
        "receiptdate": "20240101",
        "serious": "1",
        "seriousnessdeath": "0",
        "patient": {
            "reaction": [
                {"reactionmeddrapt": "Nausea"},
                {"reactionmeddrapt": "Headache"},
            ],
            "drug": [
                {
                    "medicinalproduct": "ASPIRIN",
                    "drugcharacterization": "1",
                },
            ],
        },
    }
])

DRUG_LABEL_RESPONSE = _wrap_response([
    {
        "openfda": {
            "brand_name": ["LIPITOR"],
            "generic_name": ["ATORVASTATIN CALCIUM"],
            "manufacturer_name": ["Pfizer"],
        },
        "indications_and_usage": ["For the reduction of elevated total cholesterol."],
        "dosage_and_administration": ["10-80 mg once daily."],
        "warnings": ["Liver enzyme abnormalities have been reported."],
        "adverse_reactions": ["Nasopharyngitis, arthralgia, diarrhea."],
        "contraindications": ["Active liver disease."],
        "drug_interactions": ["Cyclosporine, gemfibrozil."],
    }
])

DRUG_NDC_RESPONSE = _wrap_response([
    {
        "product_ndc": "0069-1530",
        "brand_name": "LIPITOR",
        "generic_name": "ATORVASTATIN CALCIUM",
        "dosage_form": "TABLET, FILM COATED",
        "route": ["ORAL"],
        "active_ingredients": [
            {"name": "ATORVASTATIN CALCIUM", "strength": "10 mg"},
        ],
    }
])

DRUG_ENFORCEMENT_RESPONSE = _wrap_response([
    {
        "recall_number": "D-0001-2024",
        "classification": "Class II",
        "status": "Ongoing",
        "recalling_firm": "Test Pharma Inc",
        "product_description": "Test Drug 10mg Tablets",
        "reason_for_recall": "Failed dissolution testing",
        "distribution_pattern": "Nationwide",
        "report_date": "20240101",
    }
])

DRUGSFDA_RESPONSE = _wrap_response([
    {
        "application_number": "NDA021457",
        "sponsor_name": "Pfizer",
        "products": [
            {
                "brand_name": "LIPITOR",
                "active_ingredients": "ATORVASTATIN CALCIUM",
                "dosage_form": "TABLET",
                "route": "ORAL",
            }
        ],
        "submissions": [
            {
                "submission_type": "ORIG",
                "submission_number": "1",
                "submission_status": "AP",
            }
        ],
    }
])

DRUG_SHORTAGE_RESPONSE = _wrap_response([
    {
        "generic_name": "DOXYCYCLINE HYCLATE",
        "brand_name": "VIBRAMYCIN",
        "status": "Currently in Shortage",
        "company": "Pfizer",
        "presentation": "100mg Capsules",
    }
])

# -- Device endpoint sample responses --

DEVICE_510K_RESPONSE = _wrap_response([
    {
        "k_number": "K213456",
        "device_name": "Pulse Oximeter",
        "applicant": "Test Medical Inc",
        "decision_description": "SESE",
        "decision_date": "2024-01-15",
        "product_code": "DQA",
        "review_panel": "AN",
    }
])

DEVICE_PMA_RESPONSE = _wrap_response([
    {
        "pma_number": "P200001",
        "trade_name": "Test Cardiac Device",
        "applicant": "CardioTech Inc",
        "decision_description": "APPROVAL",
        "decision_date": "2024-02-01",
        "product_code": "NIQ",
        "advisory_committee_description": "Cardiovascular",
    }
])

DEVICE_CLASSIFICATION_RESPONSE = _wrap_response([
    {
        "product_code": "DQA",
        "device_name": "System, Oximeter, Pulse",
        "device_class": "2",
        "regulation_number": "870.2710",
        "medical_specialty_description": "Anesthesiology",
        "review_panel": "AN",
    }
])

DEVICE_ENFORCEMENT_RESPONSE = _wrap_response([
    {
        "recall_number": "Z-0001-2024",
        "classification": "Class I",
        "status": "Ongoing",
        "recalling_firm": "Test Device Corp",
        "product_description": "Infusion Pump Model X",
        "reason_for_recall": "Software defect",
        "distribution_pattern": "Nationwide",
        "report_date": "20240201",
    }
])

DEVICE_EVENT_RESPONSE = _wrap_response([
    {
        "mdr_report_key": "12345",
        "date_received": "20240301",
        "event_type": "Injury",
        "device": [
            {
                "generic_name": "Infusion Pump",
                "brand_name": "PumpX",
                "manufacturer_d_name": "Test Device Corp",
            }
        ],
        "mdr_text": [
            {"text": "Patient experienced adverse event during pump use."}
        ],
        "patient": [
            {"sequence_number_outcome": ["Treated"]}
        ],
    }
])

DEVICE_RECALL_RESPONSE = _wrap_response([
    {
        "res_event_number": "78901",
        "product_code": "FRN",
        "recalling_firm": "Test Device Corp",
        "root_cause_description": "Software Bug",
        "action": "Voluntary recall",
        "product_description": "Infusion Pump Software v2.0",
    }
])

DEVICE_REGISTRATION_RESPONSE = _wrap_response([
    {
        "registration_number": "REG123456",
        "establishment_type": ["Manufacturer"],
        "products": {
            "product_code": "DQA",
            "openfda": {
                "device_name": "Pulse Oximeter",
            },
        },
        "proprietary_name": ["PulseCheck Pro"],
    }
])

DEVICE_UDI_RESPONSE = _wrap_response([
    {
        "identifiers": [
            {"id": "00886009100121", "issuing_agency": "GS1"},
        ],
        "brand_name": "FreeStyle Libre 2",
        "company_name": "Abbott Diabetes Care",
        "device_description": "Continuous Glucose Monitor",
        "version_or_model_number": "Libre2-001",
        "MRISafety": "MR Unsafe",
    }
])

DEVICE_COVID19_RESPONSE = _wrap_response([
    {
        "manufacturer": "Abbott",
        "device": "Architect SARS-CoV-2 IgG",
        "sensitivity": "99.6%",
        "specificity": "99.3%",
        "date_updated": "2024-01-01",
    }
])

# -- Food endpoint sample responses --

FOOD_ENFORCEMENT_RESPONSE = _wrap_response([
    {
        "recall_number": "F-0001-2024",
        "classification": "Class I",
        "status": "Ongoing",
        "recalling_firm": "Test Foods Inc",
        "product_description": "Peanut Butter",
        "reason_for_recall": "Undeclared allergen",
        "distribution_pattern": "Nationwide",
        "report_date": "20240401",
    }
])

FOOD_EVENT_RESPONSE = _wrap_response([
    {
        "report_number": "CAERS-2024-001",
        "date_started": "20240501",
        "products": [
            {
                "name_brand": "TestSupp Energy Drink",
                "role": "Suspect",
                "industry_name": "Dietary Supplements",
            }
        ],
        "reactions": ["Nausea", "Vomiting", "Diarrhea"],
        "outcomes": ["Hospitalization"],
    }
])

# -- Other endpoint sample responses --

HISTORICAL_DOCUMENT_RESPONSE = _wrap_response([
    {
        "title": "Historical FDA Guidance",
        "date": "19800101",
        "type": "Guidance",
        "url": "https://www.fda.gov/example",
    }
])

NSDE_RESPONSE = _wrap_response([
    {
        "product_ndc": "0002-3227",
        "package_ndc": "0002-3227-30",
        "spl_id": "abc-123",
        "marketing_category": "NDA",
    }
])

SUBSTANCE_RESPONSE = _wrap_response([
    {
        "unii": "R16CO5Y76E",
        "substance_name": "ASPIRIN",
        "codes": [
            {"code": "50-78-2", "code_system": "CAS"},
        ],
    }
])

UNII_RESPONSE = _wrap_response([
    {
        "unii": "R16CO5Y76E",
        "display_name": "ASPIRIN",
        "preferred_term": "ASPIRIN",
        "mf": "C9H8O4",
        "inchikey": "BSYNRYMUTXBXSQ-UHFFFAOYSA-N",
    }
])

# Count response
COUNT_RESPONSE = {
    "results": [
        {"term": "NAUSEA", "count": 500},
        {"term": "HEADACHE", "count": 300},
        {"term": "FATIGUE", "count": 200},
    ]
}


# Mapping of endpoint paths to sample responses
SAMPLE_RESPONSES: dict[str, dict] = {
    "drug/event": DRUG_EVENT_RESPONSE,
    "drug/label": DRUG_LABEL_RESPONSE,
    "drug/ndc": DRUG_NDC_RESPONSE,
    "drug/enforcement": DRUG_ENFORCEMENT_RESPONSE,
    "drug/drugsfda": DRUGSFDA_RESPONSE,
    "drug/shortage": DRUG_SHORTAGE_RESPONSE,
    "device/510k": DEVICE_510K_RESPONSE,
    "device/pma": DEVICE_PMA_RESPONSE,
    "device/classification": DEVICE_CLASSIFICATION_RESPONSE,
    "device/enforcement": DEVICE_ENFORCEMENT_RESPONSE,
    "device/event": DEVICE_EVENT_RESPONSE,
    "device/recall": DEVICE_RECALL_RESPONSE,
    "device/registrationlisting": DEVICE_REGISTRATION_RESPONSE,
    "device/udi": DEVICE_UDI_RESPONSE,
    "device/covid19serology": DEVICE_COVID19_RESPONSE,
    "food/enforcement": FOOD_ENFORCEMENT_RESPONSE,
    "food/event": FOOD_EVENT_RESPONSE,
    "other/historicaldocument": HISTORICAL_DOCUMENT_RESPONSE,
    "other/nsde": NSDE_RESPONSE,
    "other/substance": SUBSTANCE_RESPONSE,
    "other/unii": UNII_RESPONSE,
}


@pytest.fixture
def mock_openfda():
    """Mock all OpenFDA API endpoints using respx.

    Returns a respx.MockRouter context. Use mock_openfda.get(...) to
    customize responses for specific tests.
    """
    with respx.mock(assert_all_called=False) as router:
        for endpoint_path, response_data in SAMPLE_RESPONSES.items():
            url = f"{BASE_URL}/{endpoint_path}.json"
            router.get(url).mock(
                return_value=httpx.Response(200, json=response_data)
            )
        yield router


@pytest.fixture
def mock_openfda_count():
    """Mock OpenFDA API for count queries."""
    with respx.mock(assert_all_called=False) as router:
        # Mock all endpoints for count queries
        for endpoint_path in SAMPLE_RESPONSES:
            url = f"{BASE_URL}/{endpoint_path}.json"
            router.get(url).mock(
                return_value=httpx.Response(200, json=COUNT_RESPONSE)
            )
        yield router
