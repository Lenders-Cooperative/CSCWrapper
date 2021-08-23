from enum import Enum

# TODO implement these constants on search
class SEARCHTYPE(Enum):
    UCC = "UCC"
    CORP = "Corp"
    SLJ = "SLJ"
    CNV = "CNV"

# TODO implement these rules on search routes
class OfflineSearchRules(Enum):
    UCC = [
        'company_name',
        'first_name',
        'last_name',
        'doc_number',
        'secured_party_name'
    ]
    FIXTURE = ['debtor_name']
    FOUR_PART = ['company_name']
    INCORP_ARTICLES = ['company_name']
    CERT_EXIST = ['company_name']
    CORP_ANNUAL_REPORT = ['company_name']
    FICT_BUSINESS = [
        'company_name',
        'ficticious_business_name',
        'owner_name'
    ]
    GOOD_STAND = ['company_name']
    CORP = [
        'business_id', 
        'company_name', 
        'first_name', 
        'last_name'
    ]
    FED_TAX_LIENS = ['debtor_name']
    JUDGE_LIENS = ['debtor_name']
    STATE_TAX_LIENS = ['debtor_name']
    DEBTOR_TRACK = [
        'company_name', 
        'criteria', 
        'state'
    ]
    CORP_TRACK = [
        'company_name',
        'business_id'
    ]
    FED_CIVIL_LIT = [
        'subject',
        'criteria',
        'open_type',
        'litigant_type',
        'docket',
        'complaint',
        'last_action_filed'
    ]