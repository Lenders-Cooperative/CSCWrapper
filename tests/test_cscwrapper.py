from collections import OrderedDict

from cscwrapper.CSCWrapper import CSCWrapper


class TestsCSCWrapper:
    order_id = None

    def setup_method(self, method):
        # NOTE: add credentials here
        self.handler = CSCWrapper(
            "https://eservices-test.cscfinancialonline.com/",
            "...guid...",
            "...contact_no...",
        )
        self.handler.headers = {
            "content-type": "text/xml",
        }
        self.base64_file = ...

    def test_get_jurisdictions(self):
        r = self.handler.get_jurisdictions("TX")
        assert isinstance(r, OrderedDict)

    def test_available_searches(self):
        r = self.handler.get_available_searches("TX", "True")
        assert isinstance(r, OrderedDict)

    def test_submit_offline_search(self):
        _dict = {
            "search_type": "UCC",
            "state": "TX",
            "first_name": "John",
            "last_name": "Smith",
            "references": [{"key": "Billing Ref", "value": "E-Service"}],
        }
        r = self.handler.submit_search(True, _dict)
        assert isinstance(r, OrderedDict)

    def test_submit_online_search(self):
        _dict = {
            "search_type": "UCC",
            "state": "TX",
            "first_name": "John",
            "last_name": "Smith",
            "references": [{"key": "Pizza", "value": "Topping"}],
        }
        r = self.handler.submit_search(False, _dict)
        assert isinstance(r, OrderedDict)

    def test_create_filing(self):
        _dict = {
            "references": [{"name": "Billing Ref", "value": "Biling Ref Value"}],
            "filing_jurisdiction_state": "IL",
            "filing_jurisdiction_name": "(S.O.S)",
            "filing_jurisdiciton_id": "3154",
            "submitter_reference": "Submitter Reference",
            "debtors": [
                {
                    "organization_name": "My First Debtor",
                    "mailing_address": "123 Debtor St",
                    "city": "DebtorVille",
                    "state": "IL",
                    "postal_code": "12345",
                    "country": "USA",
                    "organization_type": "Corporation",
                    "organization_jurisdiction": "IL",
                    "organization_id": "7777777",
                },
                {
                    "first_name": "Frank",
                    "last_name": "Smith",
                    "middle_name": "I",
                    "suffix": "JR",
                    "mailing_address": "123 Debtor St",
                    "city": "DebtorVille",
                    "state": "IL",
                    "postal_code": "12345",
                    "country": "USA",
                    "organization_type": "Corporation",
                    "organization_jurisdiction": "IL",
                    "organization_id": "7777777",
                },
            ],
            "secured_name_organization_name": "Secured Part Name",
            "secured_name_organization_mailing_address": "500 Street Avenue",
            "secured_name_organization_city": "SPRINGFIELD",
            "secured_name_organization_state": "IL",
            "secured_name_organization_postal": "62708",
            "secured_name_organization_country": "USA",
            "col_text": "COL TEXT TEST",
        }

        r = self.handler.create_filing(_dict)
        assert isinstance(r, OrderedDict)

    def test_update_filing(self):
        _dict = {
            "references": [{"name": "Billing Ref", "value": "Biling Ref Value"}],
            "filing_jurisdiction_state": "IL",
            "filing_jurisdiction_name": "(S.O.S)",
            "filing_jurisdiciton_id": "3154",
            "submitter_reference": "Submitter Reference",
            "debtors": [
                {
                    "organization_name": "My Updated Debtor Name",
                }
            ],
            "secured_name_organization_name": "UPDATE_SECURE_NAME",
            "col_text": "COL TEXT TEST -- UPDATE",
        }
        r = self.handler.update_filing("153288221", _dict)
        assert isinstance(r, OrderedDict)

    def test_terminate_filing(self):
        r = self.handler.terminate_filing("153288011")
        assert isinstance(r, OrderedDict)

    def test_approve_filing(self):
        r = self.handler.approve_order("153288011")
        assert isinstance(r, OrderedDict)

    def test_get_order_info(self):
        r = self.handler.get_order_info("153287997")
        assert isinstance(r, OrderedDict)

    def test_validate_filing(self):
        r = self.handler.validate_filing("153287997")
        assert isinstance(r, OrderedDict)

    def test_get_report(self):
        r = self.handler.get_report("153281613", "Summary")
        assert isinstance(r, OrderedDict)

    def test_get_changed_orders(self):
        r = self.handler.get_changed_orders("C", "2021-06-06T13:50:00.0000000-05:00")
        assert isinstance(r, OrderedDict)

    def test_set_summary_results(self):
        r = self.handler.set_selected_results("summary", "153281613", [])
        assert isinstance(r, OrderedDict)

    def test_set_detail_results(self):
        r = self.handler.set_selected_results("detail", "153281613", [])
        assert isinstance(r, OrderedDict)

    def test_upload_attachment(self):
        r = self.handler.upload_attachment(
            "153281613", "application/pdf", "test.pdf", self.base64_file
        )

        assert isinstance(r, OrderedDict)

    def test_get_attachment(self):
        r = self.handler.get_attachment("80634867")
        assert isinstance(r, OrderedDict)

    def test_get_summary_results(self):
        r = self.handler.get_summary_results("153281613")
        assert isinstance(r, OrderedDict)

    def test_get_detail_results(self):
        r = self.handler.get_detail_results("153281613")
        assert isinstance(r, OrderedDict)

    def test_get_documents(self):
        r = self.handler.get_documents("153281613")
        assert isinstance(r, OrderedDict)
