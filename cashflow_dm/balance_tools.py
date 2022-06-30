from datetime import date

from cashflow_dm import load_data


def get_account_balance(company_id: int, date: date):
    sepa_transactions = load_data.get_sepa_transactions(
        company_id=company_id, end_date=date
    )
    swift_transactions = load_data.get_swift_transactions(
        company_id=company_id, end_date=date
    )

    return None


def get_countries_transacted(
    company_id: int = 0, start_date: date = "2018-01-01", end_date: date = "2022-01-01"
):
    pass


def get_accrued_interest(
    company_id: int = 0, start_date: date = "2018-01-01", end_date: date = "2022-01-01"
):
    pass


def predict_balance(company_id: int, date: date):
    pass
