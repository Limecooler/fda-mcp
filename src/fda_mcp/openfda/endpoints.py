"""Enum of all 21 OpenFDA API endpoints."""

from enum import Enum


class OpenFDAEndpoint(str, Enum):
    """All 21 OpenFDA API endpoints.

    Values are the URL path segments used after https://api.fda.gov/
    """

    # Drug endpoints (6)
    DRUG_EVENT = "drug/event"
    DRUG_LABEL = "drug/label"
    DRUG_NDC = "drug/ndc"
    DRUG_ENFORCEMENT = "drug/enforcement"
    DRUG_DRUGSFDA = "drug/drugsfda"
    DRUG_SHORTAGE = "drug/shortage"

    # Device endpoints (9)
    DEVICE_510K = "device/510k"
    DEVICE_PMA = "device/pma"
    DEVICE_CLASSIFICATION = "device/classification"
    DEVICE_ENFORCEMENT = "device/enforcement"
    DEVICE_EVENT = "device/event"
    DEVICE_RECALL = "device/recall"
    DEVICE_REGISTRATIONLISTING = "device/registrationlisting"
    DEVICE_UDI = "device/udi"
    DEVICE_COVID19SEROLOGY = "device/covid19serology"

    # Food endpoints (2)
    FOOD_ENFORCEMENT = "food/enforcement"
    FOOD_EVENT = "food/event"

    # Other endpoints (4)
    OTHER_HISTORICALDOCUMENT = "other/historicaldocument"
    OTHER_NSDE = "other/nsde"
    OTHER_SUBSTANCE = "other/substance"
    OTHER_UNII = "other/unii"

    @property
    def url(self) -> str:
        """Full API URL for this endpoint."""
        return f"https://api.fda.gov/{self.value}.json"

    @property
    def category(self) -> str:
        """Top-level category (drug, device, food, other)."""
        return self.value.split("/")[0]

    @property
    def description(self) -> str:
        """Human-readable description of this endpoint."""
        return _DESCRIPTIONS.get(self, self.value)


_DESCRIPTIONS: dict["OpenFDAEndpoint", str] = {
    OpenFDAEndpoint.DRUG_EVENT: "Drug adverse event reports (FAERS)",
    OpenFDAEndpoint.DRUG_LABEL: "Drug product labeling (SPL)",
    OpenFDAEndpoint.DRUG_NDC: "National Drug Code directory",
    OpenFDAEndpoint.DRUG_ENFORCEMENT: "Drug recall enforcement reports",
    OpenFDAEndpoint.DRUG_DRUGSFDA: "FDA-approved drugs (Drugs@FDA)",
    OpenFDAEndpoint.DRUG_SHORTAGE: "Drug shortage reports",
    OpenFDAEndpoint.DEVICE_510K: "510(k) premarket notifications",
    OpenFDAEndpoint.DEVICE_PMA: "Premarket approval (PMA) decisions",
    OpenFDAEndpoint.DEVICE_CLASSIFICATION: "Device classification (product codes)",
    OpenFDAEndpoint.DEVICE_ENFORCEMENT: "Device recall enforcement reports",
    OpenFDAEndpoint.DEVICE_EVENT: "Device adverse event reports (MAUDE)",
    OpenFDAEndpoint.DEVICE_RECALL: "Device recall details",
    OpenFDAEndpoint.DEVICE_REGISTRATIONLISTING: "Device registration and listing",
    OpenFDAEndpoint.DEVICE_UDI: "Unique Device Identifier (UDI) database",
    OpenFDAEndpoint.DEVICE_COVID19SEROLOGY: "COVID-19 serological test evaluations",
    OpenFDAEndpoint.FOOD_ENFORCEMENT: "Food recall enforcement reports",
    OpenFDAEndpoint.FOOD_EVENT: "Food adverse event reports (CAERS)",
    OpenFDAEndpoint.OTHER_HISTORICALDOCUMENT: "Historical FDA documents",
    OpenFDAEndpoint.OTHER_NSDE: "NDC/SPL data elements",
    OpenFDAEndpoint.OTHER_SUBSTANCE: "Substance registration data",
    OpenFDAEndpoint.OTHER_UNII: "Unique Ingredient Identifier (UNII) codes",
}


def endpoint_from_path(path: str) -> OpenFDAEndpoint:
    """Look up an endpoint enum member by its API path string.

    Raises ValueError if the path doesn't match any known endpoint.
    """
    for ep in OpenFDAEndpoint:
        if ep.value == path:
            return ep
    raise ValueError(f"Unknown endpoint path: {path}")
