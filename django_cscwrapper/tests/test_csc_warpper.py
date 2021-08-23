from django_cscwrapper.utils.CSCWrapper import CSCWrapper
from django.test import TestCase
from collections import OrderedDict
import os


class TestsCSCWrapper(TestCase):
    """
    Tests SOAPHandlerBase class
    """
    order_id = None

    def setUp(self):
        # NOTE: add credentials here
        self.soap_handler = CSCWrapper(
            guid=...,
            contact_no=...,
            url="https://eservices-test.cscfinancialonline.com/"
        )
        self.soap_handler.headers = {
            'content-type': 'text/xml',
        }
        self.order_id = None
        self.guid_prod = ...
        self.contact_no_prod = ...
        self.url_prod = "https://eservices.cscfinancialonline.com/"
        self.base64_file = ...
    
    def test_get_jurisdictions(self):
        r = self.soap_handler.get_jurisdictions('TX')
        assert r.status_code == 200
        assert isinstance(r.value, OrderedDict)

    def test_available_searches(self):
        r = self.soap_handler.get_available_searches('TX', None, 'True')
        assert r.status_code == 200
        assert r.value['AvailableSearches'] != None

    def test_submit_offline_search(self):
        _dict = {
            'search_type': 'UCC',
            'state': 'TX',
            'first_name': 'John',
            'last_name': 'Smith',
            'references': [
                {
                    'key': 'Billing Ref',
                    'value': 'E-Service'
                }
            ]
        }
        r = self.soap_handler.submit_search(True, _dict)

        assert r.status_code == 200
        assert isinstance(r.get_value('OrderID'), int)

    def test_submit_online_search(self):
        _dict = {
            'search_type': 'UCC',
            'state': 'TX',
            'first_name': 'John',
            'last_name': 'Smith',
            'references': [
                {
                    'key': 'Pizza',
                    'value': 'Topping'
                }
            ]
        }
        r = self.soap_handler.submit_search(False, _dict)


        assert r.status_code == 200
        assert r.get('return').get('orderInfo').get_value('OrderID') != None
        assert isinstance(r.get('return').get_value('summaryResults'), list)
    
    def test_create_filing(self):
        _dict = {
            'references': [
                {
                    'name': 'Billing Ref',
                    'value': 'Biling Ref Value'
                }
            ],
            'filing_jurisdiction_state': 'IL',
            'filing_jurisdiction_name': '(S.O.S)',
            'filing_jurisdiciton_id': '3154',
            'submitter_reference': 'Submitter Reference',
            'debtors': [
                {
                    'organization_name': 'My First Debtor',
                    'mailing_address': '123 Debtor St',
                    'city': 'DebtorVille',
                    'state': 'IL',
                    'postal_code': '12345',
                    'country': 'USA',
                    'organization_type': 'Corporation',
                    'organization_jurisdiction': 'IL',
                    'organization_id': '7777777'
                },
                {
                    'first_name': 'Frank',
                    'last_name': 'Smith',
                    'middle_name': 'I',
                    'suffix': 'JR',
                    'mailing_address': '123 Debtor St',
                    'city': 'DebtorVille',
                    'state': 'IL',
                    'postal_code': '12345',
                    'country': 'USA',
                    'organization_type': 'Corporation',
                    'organization_jurisdiction': 'IL',
                    'organization_id': '7777777'
                }
            ],
            'secured_name_organization_name': 'Secured Part Name',
            'secured_name_organization_mailing_address': '500 Street Avenue',
            'secured_name_organization_city': 'SPRINGFIELD',
            'secured_name_organization_state': 'IL',
            'secured_name_organization_postal': '62708',
            'secured_name_organization_country': 'USA',
            'col_text': 'COL TEXT TEST'
        }

        r = self.soap_handler.create_filing(_dict)

        assert r.status_code == 200
        assert r.get_value('OrderID') != None
        assert isinstance(r.get('Filing').value, OrderedDict)
        assert isinstance(r.get('Messages').value, OrderedDict)
    
    def test_update_filing(self):
        _dict = {
            'references': [
                {
                    'name': 'Billing Ref',
                    'value': 'Biling Ref Value'
                }
            ],
            'filing_jurisdiction_state': 'IL',
            'filing_jurisdiction_name': '(S.O.S)',
            'filing_jurisdiciton_id': '3154',
            'submitter_reference': 'Submitter Reference',
            'debtors': [
                {
                    'organization_name': 'My Updated Debtor Name',
                }
            ],
            'secured_name_organization_name': 'UPDATE_SECURE_NAME',
            'col_text': 'COL TEXT TEST -- UPDATE'
        }
        r = self.soap_handler.update_filing('153288221', _dict)

        assert r.status_code == 200

    
    def test_terminate_filing(self):
        r = self.soap_handler.terminate_filing('153288011')
        assert r.status_code == 200
    
    def test_approve_filing(self):
        r =self.soap_handler.approve_order('153288011')
        assert r.status_code == 200
        assert r.get_value('OrderID') != None

    def test_get_order_info(self):
        r = self.soap_handler.get_order_info('153287997')
        assert r.status_code == 200
        assert isinstance(r.value, OrderedDict)

    def test_validate_filing(self):
        r = self.soap_handler.validate_filing('153287997')
        assert r.status_code == 200
        assert isinstance(r.value, OrderedDict)

    def test_get_report(self):
        r = self.soap_handler.get_report('153281613', 'Summary')
        assert r.status_code == 200
        assert r.get_value('AttachmentURL').split("//")[0] == 'https:'
    
    def test_get_changed_orders(self):
        r = self.soap_handler.get_changed_orders('C', '2021-06-06T13:50:00.0000000-05:00')
        assert r.status_code == 200
        assert isinstance(r.value, OrderedDict)
    
    def test_set_summary_results(self):
        r = self.soap_handler.set_selected_results('summary', '153281613', [])
        assert r.status_code == 200
    
    def test_set_detail_results(self):
        r = self.soap_handler.set_selected_results('detail', '153281613', [])
        assert r.status_code == 200
    
    def test_upload_attachment(self):
        r = self.soap_handler.upload_attachment(
            '153281613',
            'application/pdf',
            'test.pdf',
            self.base64_file
        )

        assert r.status_code == 200
        assert r.get_value('AttachmentID') != None
    
    def test_get_attachment(self):
        r = self.soap_handler.get_attachment('80634867')
        assert r.status_code == 200
        assert "https://" in r.get_value('AttachmentURL')
    
    def test_get_summary_results(self):
        r = self.soap_handler.get_summary_results('153281613')
        assert r.status_code == 200
        assert r.get('orderInfo').get_value('OrderID') != None
    
    def test_get_detail_results(self):
        r = self.soap_handler.get_detail_results('153281613')
        assert r.status_code == 200
    
    def test_get_documents(self):
        r = self.soap_handler.get_documents('153281613')
        assert r.status_code == 200