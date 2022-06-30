import json
from datetime import date

import requests

baseurl = "http://localhost:8080/"


def call_ping():
    """Test cdm_exposer API
    
    Parameters
    ----------
    None
    
    Returns
    ----------
    dict:
        {'message': 'pong'} 
    """
    # Ping endpoint
    endpoint = "ping"

    url = baseurl + endpoint
    payload = {}
    files = []
    headers = {}

    return requests.request("GET", url, headers=headers, data=payload, files=files)


def get_exchange_rates():
    """Retrieve the exchange rates
    
    Parameters
    ----------
    None
    
    Returns
    ----------
    response: request.response
        `Response` object containing the exchange rates
    """
    # exchange rates endpoint
    endpoint = "exchange_rates"

    url = baseurl + endpoint
    payload = {}
    files = []
    headers = {}

    return requests.request("GET", url, headers=headers, data=payload, files=files)


def get_company_info():
    """Retrieve the company info table
    
    Parameters
    ----------
    None
    
    Returns
    ----------
    response: request.response
        `Response` object containing the company info
    """
    # company_info endpoint
    endpoint = "company_info"

    url = baseurl + endpoint
    payload = {"companyID": "93614"}
    files = []
    headers = {}

    response_company_info = requests.request(
        "GET", url, headers=headers, data=payload, files=files
    )
    return json.loads(response_company_info.json()["company_info"])


def get_sepa_transactions(
    company_id: int = 0, start_date: date = "2018-01-01", end_date: date = "2022-01-01"
):
    """Retrieve the sepa transactions for a company
    
    Parameters
    ----------
    company_id: int
        The Company Id for which transactions are retrieved
    start_date: datetime.date
        Beginning of period for transactions
    end_date: datetime.date
        End of period for transactions
    Returns
    ----------
    response: request.response
        `Response` object containing thetransactions for the period
    """
    pass


def get_swift_transactions(
    company_id: int = 0, start_date: date = "2018-01-01", end_date: date = "2022-01-01"
):
    """Retrieve the swift transactions for a company
    
    Parameters
    ----------
    company_id: int
        The Company Id for which transactions are retrieved
    start_date: datetime.date
        Beginning of period for transactions
    end_date: datetime.date
        End of period for transactions
    Returns
    ----------
    response: request.response
        `Response` object containing thetransactions for the period
    """
    pass
