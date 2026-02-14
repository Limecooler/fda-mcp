"""Tests for search_device_submissions tool."""

import pytest
from fda_mcp.tools.search import search_device_submissions


@pytest.mark.anyio
async def test_510k_submission(mock_openfda):
    result = await search_device_submissions(
        submission_type="510k", search='device_name:"pulse+oximeter"'
    )
    assert "K213456" in result
    assert "Pulse Oximeter" in result
    assert "Test Medical Inc" in result
    assert "SESE" in result
    assert "/device/510k.json" in str(mock_openfda.calls.last.request.url)


@pytest.mark.anyio
async def test_pma_submission(mock_openfda):
    result = await search_device_submissions(
        submission_type="pma", search='applicant:"Medtronic"'
    )
    assert "P200001" in result
    assert "Test Cardiac Device" in result
    assert "CardioTech Inc" in result
    assert "APPROVAL" in result
    assert "/device/pma.json" in str(mock_openfda.calls.last.request.url)


@pytest.mark.anyio
async def test_classification_submission(mock_openfda):
    result = await search_device_submissions(
        submission_type="classification", search='device_class:3'
    )
    assert "DQA" in result
    assert "Oximeter" in result
    assert "Anesthesiology" in result
    assert "/device/classification.json" in str(mock_openfda.calls.last.request.url)


@pytest.mark.anyio
async def test_registration_submission(mock_openfda):
    result = await search_device_submissions(
        submission_type="registration", search='proprietary_name:"Fitbit"'
    )
    assert "REG123456" in result
    assert "PulseCheck Pro" in result
    assert "/device/registrationlisting.json" in str(
        mock_openfda.calls.last.request.url
    )


@pytest.mark.anyio
async def test_limit_clamping(mock_openfda):
    """Passing limit=200 should result in limit=100 in the API call."""
    await search_device_submissions(
        submission_type="510k", search="test", limit=200
    )
    url = str(mock_openfda.calls.last.request.url)
    assert "/device/510k.json" in url
    assert "limit=100" in url


@pytest.mark.anyio
async def test_parameters_forwarded(mock_openfda):
    await search_device_submissions(
        submission_type="pma",
        search='applicant:"test"',
        limit=5,
        skip=10,
        sort="decision_date:desc",
    )
    url = str(mock_openfda.calls.last.request.url)
    assert "limit=5" in url
    assert "skip=10" in url
