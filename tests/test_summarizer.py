"""Tests for the response summarizer — one test per endpoint type."""

from tests.conftest import SAMPLE_RESPONSES
from fda_mcp.openfda.summarizer import summarize_response, summarize_count_response


def _assert_has_pagination(text: str):
    """All summaries should include pagination metadata."""
    assert "Results:" in text
    assert "of" in text


def test_drug_event_summary():
    result = summarize_response("drug/event", SAMPLE_RESPONSES["drug/event"])
    _assert_has_pagination(result)
    assert "Report ID: 10001" in result
    assert "Nausea" in result
    assert "ASPIRIN" in result
    assert "Suspect" in result


def test_drug_label_summary():
    result = summarize_response("drug/label", SAMPLE_RESPONSES["drug/label"])
    _assert_has_pagination(result)
    assert "LIPITOR" in result
    assert "ATORVASTATIN" in result
    assert "cholesterol" in result.lower()


def test_drug_ndc_summary():
    result = summarize_response("drug/ndc", SAMPLE_RESPONSES["drug/ndc"])
    _assert_has_pagination(result)
    assert "0069-1530" in result
    assert "LIPITOR" in result
    assert "10 mg" in result


def test_drug_enforcement_summary():
    result = summarize_response(
        "drug/enforcement", SAMPLE_RESPONSES["drug/enforcement"]
    )
    _assert_has_pagination(result)
    assert "D-0001-2024" in result
    assert "Class II" in result
    assert "dissolution" in result.lower()


def test_drugsfda_summary():
    result = summarize_response(
        "drug/drugsfda", SAMPLE_RESPONSES["drug/drugsfda"]
    )
    _assert_has_pagination(result)
    assert "NDA021457" in result
    assert "Pfizer" in result
    assert "LIPITOR" in result


def test_drug_shortage_summary():
    result = summarize_response(
        "drug/shortage", SAMPLE_RESPONSES["drug/shortage"]
    )
    _assert_has_pagination(result)
    assert "DOXYCYCLINE" in result
    assert "Currently in Shortage" in result


def test_device_510k_summary():
    result = summarize_response(
        "device/510k", SAMPLE_RESPONSES["device/510k"]
    )
    _assert_has_pagination(result)
    assert "K213456" in result
    assert "Pulse Oximeter" in result
    assert "SESE" in result


def test_device_pma_summary():
    result = summarize_response(
        "device/pma", SAMPLE_RESPONSES["device/pma"]
    )
    _assert_has_pagination(result)
    assert "P200001" in result
    assert "APPROVAL" in result
    assert "CardioTech" in result


def test_device_classification_summary():
    result = summarize_response(
        "device/classification", SAMPLE_RESPONSES["device/classification"]
    )
    _assert_has_pagination(result)
    assert "DQA" in result
    assert "Class" in result or "2" in result


def test_device_enforcement_summary():
    result = summarize_response(
        "device/enforcement", SAMPLE_RESPONSES["device/enforcement"]
    )
    _assert_has_pagination(result)
    assert "Class I" in result
    assert "Software defect" in result


def test_device_event_summary():
    result = summarize_response(
        "device/event", SAMPLE_RESPONSES["device/event"]
    )
    _assert_has_pagination(result)
    assert "12345" in result
    assert "Injury" in result
    assert "PumpX" in result


def test_device_recall_summary():
    result = summarize_response(
        "device/recall", SAMPLE_RESPONSES["device/recall"]
    )
    _assert_has_pagination(result)
    assert "78901" in result
    assert "Software Bug" in result


def test_device_registration_summary():
    result = summarize_response(
        "device/registrationlisting",
        SAMPLE_RESPONSES["device/registrationlisting"],
    )
    _assert_has_pagination(result)
    assert "REG123456" in result


def test_device_udi_summary():
    result = summarize_response(
        "device/udi", SAMPLE_RESPONSES["device/udi"]
    )
    _assert_has_pagination(result)
    assert "FreeStyle" in result
    assert "Abbott" in result


def test_device_covid19_summary():
    result = summarize_response(
        "device/covid19serology",
        SAMPLE_RESPONSES["device/covid19serology"],
    )
    _assert_has_pagination(result)
    assert "Abbott" in result
    assert "99.6%" in result


def test_food_enforcement_summary():
    result = summarize_response(
        "food/enforcement", SAMPLE_RESPONSES["food/enforcement"]
    )
    _assert_has_pagination(result)
    assert "Peanut Butter" in result
    assert "allergen" in result.lower()


def test_food_event_summary():
    result = summarize_response(
        "food/event", SAMPLE_RESPONSES["food/event"]
    )
    _assert_has_pagination(result)
    assert "CAERS-2024-001" in result
    assert "Nausea" in result


def test_historical_document_summary():
    result = summarize_response(
        "other/historicaldocument",
        SAMPLE_RESPONSES["other/historicaldocument"],
    )
    _assert_has_pagination(result)
    assert "Historical FDA Guidance" in result


def test_nsde_summary():
    result = summarize_response(
        "other/nsde", SAMPLE_RESPONSES["other/nsde"]
    )
    _assert_has_pagination(result)
    assert "0002-3227" in result


def test_substance_summary():
    result = summarize_response(
        "other/substance", SAMPLE_RESPONSES["other/substance"]
    )
    _assert_has_pagination(result)
    assert "ASPIRIN" in result
    assert "R16CO5Y76E" in result


def test_unii_summary():
    result = summarize_response(
        "other/unii", SAMPLE_RESPONSES["other/unii"]
    )
    _assert_has_pagination(result)
    assert "R16CO5Y76E" in result
    assert "C9H8O4" in result


def test_pagination_has_more():
    data = {
        "meta": {"results": {"skip": 0, "limit": 1, "total": 101}},
        "results": [{"test": "data"}],
    }
    result = summarize_response("other/unii", data)
    assert "More results available" in result
    assert "count_records" in result


def test_count_response_summary():
    data = {
        "results": [
            {"term": "NAUSEA", "count": 500},
            {"term": "HEADACHE", "count": 300},
            {"term": "FATIGUE", "count": 200},
        ]
    }
    result = summarize_count_response(data)
    assert "1,000" in result
    assert "NAUSEA" in result
    assert "50.0%" in result
    assert "most common" in result


def test_count_response_empty():
    result = summarize_count_response({"results": []})
    assert "No count results" in result
