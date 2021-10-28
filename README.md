<h1 align="center">CSC Wrapper</h1>

<div align="center">

</div>

---

<p align="center"> A wrapper for an the CSC XML Service. 
    <br> 
</p>

## 📝 Table of Contents

- [About](#about)
- [Getting Started](#getting-started)
- [Running Tests](#running-tests)
- [Usage](#usage)
- [Built Using](#built-using)
- [Authors](#authors)
- [Acknowledgments](#acknowledgements)

### Installing

```
pip install cscwarpper
```

## Running Tests

```
pytest
```

## Usage

Example usage of the CSC client:

```python
client = CSCWrapper(
    "https://eservices-test.cscfinancialonline.com/",
    "guid",
    "contact_no"
)

r = client.get_jurisdictions('TX')
print(r)
```

More examples can be viewed under `/tests/test_csc_wrapper.py`

### Functions

* `create_filing(filing: dict)` - Creates a filing through CSC. The filing param is a dictionary an example dictionary can be seen in tests.
* `validate_filing(order_id: int)` - Validates a filing which return messages if there's any errors. The param is the OrderID for the filing.
* `update_filing(order_id: int, filing: dict)` - This method will allow you to update the data associated with a filing. This method is used the same way 
CreateFiling is used. You just need to provide the OrderID that needs to be updated. 
* `approve_order(order_id: int)` - This method approves the filing. Filings can only be approved if they do not have any validation messages above 
level two. Any level two (yellow) messages should be displayed to users so they can decide how to best handle the 
message.
* `continue_filing(order_id: int)` - This method allows you to file a continuation to an existing filing that is in the system. The following requirements 
must be met in order for the filing to be continued:

    • The order must be a filing order  
    • The filing must be approved  
    • The filing must be filed within the US 

* `terminate_filing(order_id: int)` - This method allows you to file a termination to an existing filing that is in the system.  
* `get_order_info(order_id: int)` - This method allows you to get various pieces of information about an order in the CSC database. This includes the 
types of services the order has, as well as information on the status of an order.
* `get_changed_orders(status: str, from_date: datetime)` - This method retrieves orders whose statuses have changed in the specified timeframe. This would be used to check 
on the status of orders in the system.
* `upload_attachment(order_id: int, content_type: str, description: str, attachment: str)` - This method is used to upload an attachment to an existing order. The attachment param requires base64 string.  
* `get_attachment(attachment_id: int)` - This method is used to retrieve an attachment from an existing order.  
* `get_available_searches(state: str, serach_type:str, is_online: bool)` - This method returns a list of available searches with “thru dates” and online status. When this method is used with 
no parameters, it returns a listing of all searches possible in the CSC system that can return results.
* `get_jurisdictions(state: str)` - This method returns a list of jurisdictions to use within the CSC system. These jurisdictions are very important 
when placing orders. Using the wrong jurisdiction could send an offline request to the wrong county, which would 
result in additional costs incurred. If called with no parameters, all jurisdictions are returned. 
* `get_summary_results(order_id: int)` - This method gets the summary results from a search that has been submitted. This is not available for offline 
search requests. 
* `get_detail_results(order_id: int)` - This method gets the detail results from a search that has been submitted. If you call this method without calling 
GetSummaryResults you will get the same result as if all summary records were selected. Calling this method after 
calling GetSummaryResults without passing any selected results will return no records. 
* `get_report(order_id: int, report_type: str)` - Once you get detail results and optionally select a subset of those, you can call this method to generate a report of 
the results.
* `get_documents(order_id: int, selected_results: list)` - This method gets documents from a detail report. 
* `set_selected_results(result_type: str, order_id: int, row_ids: list)` - Given the result_type, detail / summary, this method selects the detail results for an online search OR selects the summary results for an online search.
* `submit_search(is_offline: bool, envelope_attributes: dict)` - Given the `is_offline` param, this function can either send an offline / online search request.  

    If online this method submits a search request and finds online search results. With this call, the user expects to receive 
    search results immediately. If the database is offline, the method will throw an exception. The type of search run is 
    determined by a combination of the “type” parameter and the criteria parameters chosen. 

    If offline, this method submits an offline search request. When submitting an offline search, results are not retrieved 
    instantly. Instead, an order is created and submitted for CSC to fulfill. 

NB, you can check the tests to see what the functions require for building the XML envelope.