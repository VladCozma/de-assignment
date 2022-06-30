# CashFlow Datamaker - ING BTP Technical Assessment Case
Being one of the world's largest Financial Institutions, ING provides Financial-Services to clients in almost every business sector. Transactions lie at the heart of these
financial services and we have a constant need to analyze accounts and the transactions.

**Hence, as the engineering take-home assignment, we ask you to develop a
_CashFlow Monitoring Application_.**

### Objective
You are given a multitude of datasets: 2 International Transaction, 1 company-information and 1 Currency-ExchangeRates datasets.

ING Clients want to use a CashFlow monitoring application that helps an end-user
to analyze the accounts to which the transactions are linked.

For a given input Company, your application must be able to provide:

1. Current account(s) Balance.
2. Over-Committed Balance / Debt.
3. Under-Committed Balance / Credit.
4. Which Countries did the client transact within?
5. Perform Historical Analysis on the data: Solution must have the ability to view the Account Balance of a company on customizable
time intervals, i.e., a user can either select a day, week, month or an entire year for analyzing the client.
6. Predict the account balance at some point in the future
7. We love being surprised with new ideas so put your thinking cap on!

## Acceptance Criteria for your Solution

**All candidate solutions must adhere to the following requirements:**

- Include ALL sources: Your application must analyze the incoming data from _all transaction sources_ to obtain the "accurate" account balance.
- Testing: 1 Integration Test must be created. Try to add unit tests where you think the functionality is critical.
- All solutions must Pass the UnitTestCase plan that is shipped with the assignment.
- Clean up `Dirty Transactions`: Our transactions datasets may contain Invalid Transactions. We do not want to our analysis to include this "dirty" data.

An InvalidTransaction is one which has the same ID, Sender, Beneficiary and Timestamp between the transacting clients.

Also, reader should note that analysis must be conducted only on `valid IBANs`. For sake of simplicity, you can consider an invalid IBAN to be an account which does not start with an ISO-2-Letter-Country-Code.
Or IBAN validation: https://en.wikipedia.org/wiki/International_Bank_Account_Number


Additionally, Your solution design must:
- Connect to the bundled API for generating its input data, using the endpoints listed above.
- Repeatedly poll the endpoints (you can assume that the CDM API may start returning duplicate results, periodically).

Too many terms for your liking? Do not worry, we have included a Glossary.

Also, our interviewers will try to assess your engineering skills, not how you handle fancy Banking Nomenclature.


### Bonus Points
- How would you alter your solution if 1 ING client held multiple IBANs? (1:N relationship).
- Dockerize your solution.
- Include a Cloud Deployment Diagram: How / what would you change in your solution architecture?
- Justifying a Distributed System: Kafka or no Kafka; it doesnt matter so long as your justification suffices. The reason on WHY ___  is more important.
- Can you provide a NonTechnical explaination of your solution to a layman?
- Additional Test Cases.


## Provided Resources

There is an included [docker-compose file with the database and services](./docker-compose-candidate.yml) for you. Just run `docker-compose -f docker-compose-candidate.yml up`
to start the services. The `data_exposer` container will be eventually available after the `Postgres` container has successfully started.
start with evnironment variable SETTING=small
```
    environment:
      - SETTING=small
```

You are given 4 dataset to work with:

1. **Company Info**: Describes ING Clients and the Accounts they Hold.
2. **SEPA Transactions**: Transactions _only within Euro Payment Area_. This dataset only has transactions with `EUR` currency.
These Transactions _only include the accounts from `CompanyInfo` dataset_.
3. **SWIFT Transactions**: _Global Transactions DataSet_ including transactions from multiple currencies and countries, across the globe.
4. **ExchangeRates:** **1:1 mapping** between `SWIFT` and currencies seen therein. Only `SWIFT` data contains multiple currencies.
5. You can choose either EUR or USD as the currency rate for your analysis.

We provide you with a sample REST API, called `cdm_exposer`, that exposes 4 endpoints, one for each dataset listed above:
- `/companyInfo` provides ALL `CompanyInfo` Details.
- `/sepa` provides `SEPA` transactions for only the accounts in `CompanyInfo`. This endpoint only returns data for certain days at a time. It needs to be repeatedly polled.
- `/swift` provides `SWIFT` transactions for accounts _**globally**_. This endpoint only returns data for certain days at a time. It needs to be repeatedly polled.
- `/exchange_rates` provides currencies' exchange rates for `SWIFT` transactions for accounts _**globally**_.


### Data schemas

#### Glossary

- IBAN - International Banking Account Number: For the scope of this assignment, candidate can assume that `ALL VALID IBANs start with a 2-letter ISO-CountryCode`.
An Account, or IBAN, are synonymous and mean the same thing.
- SEPA: Single Euro Payments Area: Consists of transactions `ONLY in euros`, for countries that are inside the Euro Payment Zone, using Euros as their default currency.
- SWIFT: Global Payment Messaging System which has transactions of `multiple currencies`, being executed globally.
- ExchangeRates: This Table includes the information of `currencies with their current exchange rates, mapped out to either EUR / USD`.
The currencies in this Table follow `ISO Currency Codes`, which is a 3-letter-ISO-Code. All other codes maybe deemed invalid.

| **Company Info** |
|------------------|
| CompanyID        |
| Name             |
| Address          |
| Balance          |
| IBANs            |


| **SEPA**         |
|------------------|
| Payer_IBAN       |
| Beneficiary_IBAN |
| Amount           |
| Currency         |
| Timestamp        |

| **SWIFT**        |
|------------------|
| Payer_IBAN       |
| Beneficiary_IBAN |
| Amount           |
| Currency         |
| Timestamp        |


| **ExchangeRates** |
|-------------------|
| Currency          |
| USD_Rate          |
| EUR_Rate          |
---
---
