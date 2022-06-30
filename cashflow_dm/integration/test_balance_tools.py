import logging
from datetime import date

from cashflow_dm import balance_tools

log = logging.getLogger(__name__)


def test_get_account_balance():
    company_id = 0
    date = "2018-01-01"
    assert balance_tools.get_account_balance(company_id=company_id, date=date) is None


def test_get_countries_transacted():
    company_id = 0
    start_date = "2018-01-01"
    end_date = "2012-01-01"

    assert (
        balance_tools.get_countries_transacted(
            company_id=company_id, start_date=start_date, end_date=end_date
        )
        is None
    )


def test_get_accrued_interest(
    company_id: int = 0, start_date: date = "2018-01-01", end_date: date = "2022-01-01"
):
    assert balance_tools.get_accrued_interest() is None


def predict_balance(company_id: int, date: date):
    assert balance_tools.predict_balance() is None
