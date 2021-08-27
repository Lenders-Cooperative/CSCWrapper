
from requests.sessions import OrderedDict
from django_soap.utils.SOAPHandlerBase import SOAPHandlerBase
from enum import Enum
from django.db.models.query import QuerySet
import os


class CSCWrapper(SOAPHandlerBase):
    """
    Handles all SOAP requests for CSC server
    """

    class CSCRules:
        def __init__(self, csc_wrapper):
            self.csc_wrapper = csc_wrapper

    headers = {"content-type" : "text/xml"}
    url = "https://eservices-test.cscfinancialonline.com/"
    TEMPLATES = {
        'ApproveOrder': 'csc_envelopes/ApproveOrder.xml',
        'AvailableSearches': 'csc_envelopes/AvailableSearches.xml',
        'CreateFiling': 'csc_envelopes/CreateFiling.xml',
        'ContinueFiling': 'csc_envelopes/ContinueFiling.xml',
        'GetAttachment': 'csc_envelopes/GetAttachment.xml',
        'GetChangedOrders': 'csc_envelopes/GetChangedOrders.xml',
        'GetDetailResults': 'csc_envelopes/GetDetailResults.xml',
        'GetDocuments': 'csc_envelopes/GetDocuments.xml',
        'GetJurisdictions': 'csc_envelopes/GetJurisdictions.xml',
        'GetOrderInformation': 'csc_envelopes/GetOrderInformation.xml',
        'GetReport': 'csc_envelopes/GetReport.xml',
        'GetSummaryResults': 'csc_envelopes/GetSummaryResults.xml',
        'SetSelectedDetailResults': 'csc_envelopes/SetSelectedDetailResults.xml',
        'SetSelectedSummaryResults': 'csc_envelopes/SetSelectedSummaryResults.xml',
        'SubmitOfflineSearch': 'csc_envelopes/SubmitOfflineSearch.xml',
        'SubmitOnlineSearch': 'csc_envelopes/SubmitOnlineSearch.xml',
        'TerminateFiling': 'csc_envelopes/TerminateFiling.xml',
        'UpdateFiling': 'csc_envelopes/UpdateFiling.xml',
        'UploadAttachment': 'csc_envelopes/UploadAttachment.xml',
        'ValidateFiling': 'csc_envelopes/ValidateFiling.xml',
    }

    def _get_config_from_env(self, value: str):
        """
        Returns the CSC env value from environment variables.
        """
        return os.environ.get(value)

    def __init__(self, *args, **kwargs):
        self.guid = kwargs['guid'] or self._get_config_from_env('CSC_LOGIN_GUID')
        self.contact_no = kwargs['contact_no'] or self._get_config_from_env('CSC_CONTACT_NO')
        self.url = self._get_config_from_env('CSC_URL') or kwargs['url']

        if self.contact_no is None:
            raise EnvironmentError(f"CSC_CONTACT_NO is not set")
        
        if self.guid is None:
            raise EnvironmentError(f"CSC_LOGIN_ID is not set")
        
        super(CSCWrapper, self).__init__(*args, **kwargs)

    def _handle_fault_codes(self, response):
        if response.status_code != 200:
            error = (
                response
                    .find('soap:Fault')
                    .get_value('faultstring')
            )
            # error_message = error.split(':')[1].split('at')[0]
            raise Exception(
                f"{error} \n"
            )
        return response.status_code

    # Filing Functions
    def create_filing(self, filing):
        _dict = filing
        if isinstance(filing, QuerySet):
            _dict = list(filing.values())

        response = self.post(self.TEMPLATES['CreateFiling'], _dict)
        if self._handle_fault_codes(response) != 200:
            return
        # TODO are we going to be saving the entire response?
        # to return all varaibles / save to DB here
        # currently returns filing orderID
        return (
            response
                .get('soap:Envelope')
                .get('soap:Body')
                .get('CreateFilingResponse')
                .get('CreateFilingResult')
                .get('OrderInfo')
        )

    def validate_filing(self, order_id):
        response = self.post(self.TEMPLATES['ValidateFiling'], {'order_id': order_id})
        if self._handle_fault_codes(response) != 200:
            return
        value = (
            response
                .get('soap:Envelope')
                .get('soap:Body')
                .get('ValidateFilingResponse')
                .get('ValidateFilingResult')
                .get_list('Messages')
        )
        return value
    
    def update_filing(self, order_id, update_filing):
        response = self.post(self.TEMPLATES['UpdateFiling'], {'order_id': order_id, **update_filing})
    
        if self._handle_fault_codes(response) != 200:
            return
        
        return (
            response
                .get('soap:Envelope')
                .get('soap:Body')
                .get('UpdateFilingResponse')
                .get('UpdateFilingResult')
                .get('OrderInfo')
        ) 
    
    def approve_order(self, order_id):
        response = self.post(self.TEMPLATES['ApproveOrder'], {'order_id': order_id})
        print(response.xml_to_json())
        if self._handle_fault_codes(response) != 200:
            return
        value = (
            response
                .get('soap:Envelope')
                .get('soap:Body')
                .get('ApproveOrderResponse')
                .get('ApproveOrderResult')
                .get('OrderInfo')
                # .get_value('OrderID')
        )
        return value
    
    def continue_filing(self, order_id):
        response = self.post(self.TEMPLATES['ContinueFiling'], {'orderID': order_id})
        if self._handle_fault_codes(response) != 200:
            return
        value = (
            response
                .get('soap:Envelope')
                .get('soap:Body')
                .get('ContinueFilingResponse')
                .get('ContinueFilingResult')
                .get('OrderInfo')
                # .get_value('OrderID')
        )
        return value

    def terminate_filing(self, order_id):
        response = self.post(self.TEMPLATES['TerminateFiling'], {'order_id': order_id})
        if self._handle_fault_codes(response) != 200:
            return
        value = (
            response
                .get('soap:Envelope')
                .get('soap:Body')
                .get('TerminateFilingResponse')
                .get('TerminateFilingResult')
                .get('OrderInfo')
                # .get_value('OrderID')
        )
        return value

    def get_order_info(self, order_id: int) -> OrderedDict:
        response = self.post(self.TEMPLATES['GetOrderInformation'], {'order_id': order_id})
        if self._handle_fault_codes(response) != 200:
            return

        return (
            response
                .get('soap:Envelope')
                .get('soap:Body')
                .get('GetOrderInformationResponse')
                .get('GetOrderInformationResult')
                .get_list('OrderInfo')
        )
    
    def get_changed_orders(self, status, from_date) -> OrderedDict:
        response = self.post(
            self.TEMPLATES['GetChangedOrders'],
            {'status': status, 'from_date': from_date}
        )
        if self._handle_fault_codes(response) != 200:
            return
        return (
            response
                .get('soap:Envelope')
                .get('soap:Body')
                .get('GetChangedOrdersResponse')
                .get('GetChangedOrdersResult')
                .get_list('ChangedOrders')
        )
    
    def upload_attachment(self, order_id, content_type, description, attachment):
        """
        Uploads file to CSC servers

        params:
            order_id: int
            content_type: str
            description: str
            file: base64 str
        
        returns:
            response: SoapResult
        """
        response = self.post(self.TEMPLATES['UploadAttachment'], {
            'order_id': order_id,
            'content_type': content_type,
            'description': description,
            'attachment': attachment
        })

        if self._handle_fault_codes(response) != 200:
            return

        return (
            response
                .get('soap:Envelope')
                .get('soap:Body')
                .get('UploadAttachmentResponse')
                .get('UploadAttachmentResult')
                .get('return')
        )
    
    def get_attachment(self, attachment_id):
        response = self.post(self.TEMPLATES['GetAttachment'], {'attachment_id': attachment_id})
        if self._handle_fault_codes(response) != 200:
            return

        return (
            response
                .get('soap:Envelope')
                .get('soap:Body')
                .get('GetAttachmentResponse')
                .get('GetAttachmentResult')
                .get('return')
        )
    
    # Search Functions
    def get_available_searches(self, state, search_type, is_online):
        # TODO take in search type
        _dict = {
            'state': state,
            'is_online': is_online,
            'search_type': search_type,
        }
        response = self.post(self.TEMPLATES['AvailableSearches'] , _dict)
        if self._handle_fault_codes(response) != 200:
            return
        return (
            response
                .get('soap:Envelope')
                .get('soap:Body')
                .get('AvailableSearchesResponse')
                .get('AvailableSearchesResult')
                .get('return')
        )
    
    def get_jurisdictions(self, state):
        response = self.post(self.TEMPLATES['GetJurisdictions'], {'state': state})
        if self._handle_fault_codes(response) != 200:
            return
        return (
            response
                .get('soap:Envelope')
                .get('soap:Body')
                .get('GetJurisdictionsResponse')
                .get('GetJurisdictionsResult')
                .get('return')
        ) 

    def get_summary_results(self, order_id):
        response = self.post(self.TEMPLATES['GetSummaryResults'], {'order_id': order_id})

        print(response.xml_to_json())

        if self._handle_fault_codes(response) != 200:
            return
        
        return (
            response
                .get('soap:Envelope')
                .get('soap:Body')
                .get('GetSummaryResultsResponse')
                .get('GetSummaryResultsResult')
                .get('return')
        ) 
    
    def get_detail_results(self, order_id):
        response = self.post(self.TEMPLATES['GetDetailResults'], {'order_id': order_id})
        if self._handle_fault_codes(response) != 200:
            return
        return (
            response
                .get('soap:Envelope')
                .get('soap:Body')
                .get('GetDetailResultsResponse')
                .get('GetDetailResultsResult')
                .get('return')
        )
    
    def get_report(self, order_id, report_type):
        response = self.post(
            self.TEMPLATES['GetReport'],
            {'order_id': order_id, 'report_type': report_type}
        )
        if self._handle_fault_codes(response) != 200:
            return
        return (
            response
                .get('soap:Envelope')
                .get('soap:Body')
                .get('GetReportResponse')
                .get('GetReportResult')
                .get('return')
                # .get_value('AttachmentURL')
        )
    
    def get_documents(self, order_id, selected_results=None):
        response = self.post(
            self.TEMPLATES['GetDocuments'],
            {'order_id': order_id, 'selected_results': selected_results}
        )

        if self._handle_fault_codes(response) != 200:
            return

        return (
            response
                .get('soap:Envelope')
                .get('soap:Body')
                .get('GetDocumentsResponse')
                .get('GetDocumentsResult')
                .get('return')
                # .get_value('ReportURL')
        )
    
    def set_selected_results(self, result_type, order_id, row_ids=[]):
        if result_type == 'summary':
            template = self.TEMPLATES['SetSelectedSummaryResults']
        elif result_type == 'detail':
            template = self.TEMPLATES['SetSelectedDetailResults']
        else:
            raise ValueError('Invalid result type')
        
        response = self.post(
            template,
            {'order_id': order_id, 'row_ids': row_ids}
        )

        if self._handle_fault_codes(response) != 200:
            return

        return response
    
    def submit_search(self, is_offline, evenlope_attributes):
        _dict = evenlope_attributes
        # if isinstance(evenlope_attributes, QuerySet):
        #     _dict['search'] = list(evenlope_attributes.values())
        # else:
        #     _dict = evenlope_attributes
        
        template = self.TEMPLATES['SubmitOnlineSearch']
        response_value = 'SubmitOnlineSearchResponse'
        result_value = 'SubmitOnlineSearchResult'
        if is_offline:
            template = self.TEMPLATES['SubmitOfflineSearch']
            response_value = 'SubmitOfflineSearchResponse'
            result_value = 'SubmitOfflineSearchResult'
    
        response = self.post(template, _dict)

        if self._handle_fault_codes(response) != 200:
            return
        
        return (
            response
                .get('soap:Envelope')
                .get('soap:Body')
                .get(response_value)
                .get(result_value)
        )