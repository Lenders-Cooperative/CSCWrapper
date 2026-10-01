"""Verify CSC filing XML contracts through a mocked HTTP transport."""

from unittest.mock import patch
from xml.etree import ElementTree

import pytest

from cscwrapper.CSCWrapper import CSCWrapper


@pytest.mark.parametrize("operation", ["create", "update"])
@pytest.mark.parametrize("filing_state", ["WY", "CA", "IL", "NY"])
@pytest.mark.parametrize("is_organization", [False, True])
def test_debtor_organization_fields_follow_filing_state(
    operation: str, filing_state: str, is_organization: bool
) -> None:
    """Filing XML omits County and limits organization tags to NY filing jurisdiction."""
    debtor = {
        "mailing_address": "1 Main St Suite 2",
        "city": "Example City",
        "state": "WY" if filing_state == "NY" else "NY",
        "postal_code": "12345",
        "country": "USA",
        "organization_type": "LLC",
        "organization_jurisdiction": "WY",
        "organization_id": "SYNTHETIC-ID",
    }
    if is_organization:
        debtor.update(first_name=None, organization_name="Synthetic & Co")
    else:
        debtor.update(first_name="Ada", last_name="Lovelace", middle_name="", suffix="")
    filing = {
        "references": [{"name": "Application ID", "value": "12345678"}],
        "filing_jurisdiction_state": filing_state,
        "filing_jurisdiction_name": "Secretary of State",
        "filling_jurisdiction_id": "SYNTHETIC-JURISDICTION",
        "debtors": [debtor],
        "col_text": "Equipment < secured assets",
    }
    client = CSCWrapper(
        "https://csc.example.invalid", "synthetic-guid", "1", logging=False
    )
    with patch.object(
        client._api_handler, "_send_request", return_value="<Response/>"
    ) as transport:
        if operation == "create":
            client.create_filing(filing)
        else:
            client.update_filing("SYNTHETIC-ORDER", filing)

    transport.assert_called_once()
    root = ElementTree.fromstring(transport.call_args.args[1])
    names = root.find(".//Debtors/DebtorName/Names")
    assert names is not None
    assert names.find("County") is None
    for tag, key in (
        ("OrganizationalType", "organization_type"),
        ("OrganizationalJuris", "organization_jurisdiction"),
        ("OrganizationalID", "organization_id"),
    ):
        element = names.find(tag)
        if filing_state == "NY":
            assert element is not None
            assert element.text == debtor[key]
        else:
            assert element is None
    assert names.findtext("MailAddress") == debtor["mailing_address"]
    assert names.findtext("State") == debtor["state"]
    assert root.findtext(".//ReferenceFieldName") == "Application ID"
    assert root.findtext(".//ReferenceFieldValue") == "12345678"
    assert root.findtext(".//ColText") == filing["col_text"]
    if is_organization:
        assert names.findtext("OrganizationName") == debtor["organization_name"]
    else:
        assert names.findtext("IndividualName/FirstName") == "Ada"
