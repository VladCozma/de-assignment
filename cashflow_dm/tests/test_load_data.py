import logging

from cashflow_dm import load_data

log = logging.getLogger(__name__)


def test_call_ping():
    expected_result = {"message": "pong"}
    assert load_data.call_ping().json() == expected_result


def test_get_exchange_rates():
    expected_result = {
        "exchange_rates": '[{"currency":"EUR","usd_rate":1,"eur_rate":0.92},{"currency":"GBP","usd_rate":0.83,"eur_rate":1.32},{"currency":"USD","usd_rate":1.1,"eur_rate":1},{"currency":"SGP","usd_rate":1.49,"eur_rate":0.78},{"currency":"JPY","usd_rate":133.18,"eur_rate":0.0082},{"currency":"NOK","usd_rate":9.51,"eur_rate":0.12},{"currency":"PLN","usd_rate":4.72,"eur_rate":0.23}]'
    }
    assert load_data.get_exchange_rates().json() == expected_result


def test_get_company_info():
    expected_result = {
        "companyID": 0,
        "ibans": "{GB91PIEX43597764800353}",
        "name": "Kemp and Sons",
        "address": "17884 Nicholas Flat\nNorth Michael, MN 36663",
        "balance": 1814,
    }
    assert load_data.get_company_info()[0] == expected_result
