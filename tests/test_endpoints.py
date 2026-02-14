"""Tests for the OpenFDA endpoint enum."""

from fda_mcp.openfda.endpoints import OpenFDAEndpoint, endpoint_from_path


def test_exactly_21_endpoints():
    assert len(OpenFDAEndpoint) == 21


def test_no_duplicate_values():
    values = [ep.value for ep in OpenFDAEndpoint]
    assert len(values) == len(set(values))


def test_drug_endpoints():
    drug_eps = [ep for ep in OpenFDAEndpoint if ep.category == "drug"]
    assert len(drug_eps) == 6
    paths = {ep.value for ep in drug_eps}
    assert paths == {
        "drug/event", "drug/label", "drug/ndc",
        "drug/enforcement", "drug/drugsfda", "drug/shortage",
    }


def test_device_endpoints():
    device_eps = [ep for ep in OpenFDAEndpoint if ep.category == "device"]
    assert len(device_eps) == 9
    paths = {ep.value for ep in device_eps}
    assert "device/510k" in paths
    assert "device/pma" in paths
    assert "device/covid19serology" in paths


def test_food_endpoints():
    food_eps = [ep for ep in OpenFDAEndpoint if ep.category == "food"]
    assert len(food_eps) == 2


def test_other_endpoints():
    other_eps = [ep for ep in OpenFDAEndpoint if ep.category == "other"]
    assert len(other_eps) == 4


def test_url_construction():
    assert OpenFDAEndpoint.DRUG_EVENT.url == "https://api.fda.gov/drug/event.json"
    assert OpenFDAEndpoint.DEVICE_510K.url == "https://api.fda.gov/device/510k.json"


def test_description():
    assert "adverse" in OpenFDAEndpoint.DRUG_EVENT.description.lower()
    assert "510" in OpenFDAEndpoint.DEVICE_510K.description


def test_endpoint_from_path():
    ep = endpoint_from_path("drug/event")
    assert ep == OpenFDAEndpoint.DRUG_EVENT


def test_endpoint_from_path_invalid():
    import pytest
    with pytest.raises(ValueError, match="Unknown endpoint"):
        endpoint_from_path("invalid/endpoint")
