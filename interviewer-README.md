# cashflow-datamaker-api

This is the repository of the new technical assignment for INGA.

## 1. Purpose of this repo

The previous [Meetup API](https://help.meetup.com/hc/en-us/articles/360028901812-Using-Meetup-s-API) used for INGA's engineering interview assignment has changed its authentication flow and needs a Pro Subscription for even registering an OAuth Consumer. This has added quite some complexity for our interview procedure.

Meanwhile, we are also looking for a case which is closer to the daily work of data engineers in banking system.

Hence, we proposed this new **cashflow-datamaker-api** as an alternative for our technical assignment.

### Info

There are 3 services in the repo:
1. PostgresDB - prePopulated with Data, if you use the dockerimage `utsavjha/cdm_database:2`.
2. DataMaker - Doesnt need to be run if you use the image mentioned above. For creation of fresh Data, this service needs to be run.
3. DataExposer - Data Exposer API with endpoints the candidate connects to.

The image `utsavjha/cdm_database:2` contains a fresh load of data for `Medium` & `Large` loads.

The interviewer should only send the [docker-compose-candidate.yml](./docker-compose-candidate.yml). The DataMaker and Exposer both use an ENVAR to define the type of load.

You can specify the ENVAR `SETTING={small/medium/large/mega}` for both containers. Kindly note the exposer will throw an error if the database doesn't contain the specified load-data.

The `data_exposer` container will be eventually available after the postgres container has successfully started.

### Running The Service

Dockerized solution exists. Interviewer is recommended to use one of the prepulated databases (dockerimages of postgres).

The loads can be quite resource intensive, so its recommended to use the `SETTING=small` for the first-time users of the repo.

There are 2 docker-compose files included here, [docker-compose for candidate](./docker-compose-candidate.yml) & [docker-compose for interviewers](./docker-compose.yml).

To run it:

1. Build the containers: `docker-compose build`.
2. Spin up Containers using `docker-compose up`.
3. If the datamaker-container is started, it will export the data to postgres. Ensure correct runtype setting is chosen: `large` setting onwards need  to be prepared locally.
4. If not, and you want to start testing locally, create a python virtual env by `python3 -m venv venv` & then `source venv/bin/activate`.
5. Download dependencies for running project using `pip3 install -r requirements.txt`.
6. Run [cdm-main() using appropriate ENVAR of Setting](lib/src/main.py#L103) using `python3 lib/src/main.py` in Terminal(ensure PythonPath is Set) or your IDE. The runtype can also be specified as an ENVAR named `SETTING`.
7. Once data is succesfully exported, you need to enter the data exposer: `cd cdm_exposer` and run `go run .`. I assume you have a valid Go installation and GOPATH configured.

> Caution: Since we cater to multiple engineering profiles, the API exposing data must be configured to poll the same tables that are created by the data-populator.
> Just as the Runtype settings in data-maker, same `small, medium, large or mega` settings exist for exposing the data. The main() has a map that can be used.

5 endpoints would be made accessible after this. The endpoints and their descriptions are below.

### Connection Parameters
The candidate compose file doesnt contain any DB Connection parameters and it's intended to abstract that information away from him.
For the interviewers, here are the postgres connection details:

- POSTGRES_USER=su_champ
- POSTGRES_PASSWORD=magic
- POSTGRES_DB=some_company
- POSTGRES_HOSTNAME=postgres

### Application Logic
The application is split in 2 parts:
1. Generate Data: Generates sample data based on input runtype setting. This data generator is developed using Python & code resides under [lib](lib/src/main.py#L103). This data is exported to Postgres.
2. Expose Data from Postgres to candidate: Exposes data from postgres, in the form of an API. Candidate needs to poll this API to get the input data for his case.

Each part is explained below.

##### Data Generation
The DataGenerator has 4 Runtypes, `Small, Medium, Large & Mega`. The [main()](lib/src/main.py:63) is run with a String Argument, specifying the type of Load.

> CAUTION: Run the `Mega` Type Cautiously, its known to blow up on local machines. `large` is safe to run (under 1 hour), `medium` completes within 15 mins, while `small` takes seconds.

The main logic behind data-generation is:
1. Initialise [application](lib/src/main.py) using [Settings.Runtype](lib/src/constants/settings.py). Possible values are `small, medium, large` or `mega`.
2. [Create Companies and IBANs](lib/src/data_maker.py).
3. [Main Orchestrator](lib/src/main.py#L50) Launches 3 seperate processes for:
   - [SEPA Data Generation](lib/src/transformers/sepa.py)
   - [Swift Data Generation](lib/src/transformers/swift.py#L86)
   - [Corrupt SWIFT Data Generation](lib/src/transformers/swift.py#L203)
4. [Swift Data Generation](lib/src/transformers/swift.py::86) launches furthermore [NUM_SWIFT_PROCESS_BATCHES * 2 processes](lib/src/transformers/swift.py#L165) for data generation
   SWIFT Data comprises of both KnownCompany Transactions, and UnknownCompany Transactions. Unknown Companies are generated via a [Seperate LOCALE Setting](lib/src/constants/settings.py#L15).
5. [Results are Read from a Queue and Concatenated to create a Pandas.DataFrame](lib/src/transformers/swift.py#L124)
6. [Balance Computation Starts](lib/src/balance_finder.py) - This finds the balance of created accounts per quarter, as seen in both transaction sources. This does not include the corruptPayments,
so the interviewers can be assured that the balance of reported accounts must be
"atleast the values that they see in the CSV/table". Quite a slow step for larger batches.
7. [Corrupt Payments Generated](lib/src/transformers/swift.py#L204)- Generates 2 forms of corrupt payments:Merges them to add noise to SWIFT data.
    - [Batch Payments](lib/src/transformers/swift.py#L124);
    - [Invalid IBANs](lib/src/constants/transactions_schema.py#L40)
    - These results are [Concatenated with the SWIFT DF](lib/src/data_maker.py#L88).
8. [Data Exported to Postgres in the form of CSVs](lib/src/postgres_connector.py) - Seperate Processes launched to utilise all threads for data-exports to PG-DB. Since
Swift and Sepa Transactions usually range in magnitude of millions, they're also split up in an `append` process to write data to Postgres.

Solution is Dockerized as well. Just run `docker-compose up`.

#### Docker images

1. image: "utsavjha/cdm_database:1" - Contains the database with `large` data exported. Data Directory mounted at `/cdm_data` folder in container.
2. image: "utsavjha/cdm_database:2" - Contains the database with `large` & `medium` data exported. Data Directory mounted at `/cdm_data` folder in container.
3. image: "utsavjha/cdm_db:1" - Contains the database with `large` & `medium` data exported. The data for transaction tables is indexed on `ts` column. Data Directory mounted at `/cdm_db` folder in container.

The "utsavjha/cdm_db:1" is recommended for use with the data-exposer.

The data directory of this image is mounted at `/cdm_db`. Just add the necessary envar to PG container, `PGDATA=cdm_data` and you should be able to connect to the database with data ready for consumption.


##### Exposing Data from Postgres

Code for this is siloed under the [cdm_exposer folder.](/cdm_exposer/main.go#L40)

Exposes data on 5 endpoints, namely:
1. `/company_info`: Exposes ENTIRE company-information in a single poll.
2. `/exchange_rates`: Exposes ENTIRE XRates-information in a single poll.
3. `/sepa`: Exposes Sepa Transactions, grouped for 5 days. Repeated Polling on this endpoint required to get entire data.
4. `/swift`: Exposes SWIFT Transactions, grouped for 5 days. Repeated Polling on this endpoint required to get entire data.
5. `/ping`: Returns a `pong` response.

Since the volume of transactions is vastly more than that of others, their respective endpoints are returning data in batches.

## 2. Description of the assignment

Given source(s) of transactions (both SEPA and SWIFT), candidate is to come up with an API/Application that enables an end-user to monitor any company's balance.

### a. Assignment goal

For the Company, we want to find out:

1. Current account(s) Balance.
2. Over-Committed Balance / Debt.
3. Under-Committed Balance / Credit.
4. Countries transacted with.
5. Perform Historical Analysis on the data: Solution must have the ability to view the Account Balance of a company on customizable
   time intervals, i.e., a user can either select a day, week, month or an entire year for analyzing the client.
6. Surprise us.

### b. Data resources

The candidate will need to work with:

1. SEPA Transactions: Transactions within Euro Payment Area; only consists of EUR payments.
2. SWIFT Transactions: Global Transactions that consists of "multiple currencies" transactions.
3. Company Info: A table describing company Clients and the Accounts they Hold.
4. ExchangeRates: Table Mapping consisting of currencies and USD/EUR Exchange Rates.

We expect solution in either USD / EUR, depending upon candidate choice.

**Data schemas:**

---
| **Company Info** |
|------------------|
| ID               |
| Name             |
| Owner            |
| IBANs            |

---
| **SEPA**         |
|------------------|
| Payer_IBAN       |
| Beneficiary_IBAN |
| Amount           |
| Currency         |
| Timestamp        |

| **SWIFT**         |
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

### c. Acceptance Criteria

**For all candidates:**

- Clean up dirty data: We do not want our application to include "dirty" transactions. Dirty Transactions are of the following 2 types:
     a) BatchPayments - A Batch Payment is a transaction between same id, sender and beneficiary, at same timestamp, but with only different amounts.
     b) Invalid IBANs - An INVALID IBAN is an account number that does NOT start with a valid 2-letter-ISO Country Code.
- Connect to CDM API: the analysis must be done on a minimum of 1000 companies: 100k Sepa transactions, 1M SWIFT transactions (medium runtype batch onwards).
- Ability to perform historical analysis on the data: The solution must have the ability to view the Account Balance of a company on customizable time intervals, i.e., a user can either select a day or an entire year for analyzing the client.
- Data Aggregation: the data must be aggregated over “all transaction sources” to obtain an "accurate" account balance.
- Test: a minimum of 1 Integration Test must be created by candidate.
- All solutions must Pass the UnitTestCase plan that is shipped with the assignment.

**Bonus Points:**
- Dockerize the application.
- Building a Distributed System: Kafka or no Kafka; it doesnt matter so long as your justification suffices.
- Additional Test Cases.
- ...

## 3. The data generator

The  data generator prepares fake data according to the schema above.

We use [Faker](https://faker.readthedocs.io/en/master/) to generate all the data used by this assignment.

### a. Rule to prepare the data

The data is prepared in the following steps:
1. We first generate a fixed number of `Company Info`. each `Company Info` contains at least IBANs.
2. We use the generated `Company Info` to generate `SEPA` and `SWIFT` data.
> **Important to note here that we will populate the transactions in:**
    SEPA transactions are generated **ONLY** on the accounts that are seen in the CompanyInfo Table, while SWIFT transactions are generated over many different IBANs spanning the globe. (i.e. accounts of CompanyInfo + unknown accounts).
3. `Company Info`, `SEPA` and `SWIFT` data is dumped in to postgres database via Github CI/CD pipeline.
4. `Currency` table stores **1:1 mapping** between `SWIFT` and exchange rates currencies. Only `SWIFT` Transactions contain multiple currencies. `SEPA` only has transactions with **EUR**.
5. This data resource is published as a docker image.
6. We have corresponding E2E tests regarding the **Acceptance Criteria**.

### b. Data Corruption
- The `id` of `SWIFT` and `SEPA` is not unique. We've added some payments with same `id`, all with same amounts, from same payers and beneficiaries.
They're termed as `BatchPayments` and an ideal solution must have the capability to analyze both Batch and Normal Transactions.
-

### c. Commands

To run tests

```
python -m pytest
```

To run linting with flake8

```
flake8
```

## 5. Open questions

### a. Are we going to use the same dataset for FE and BE interviews as well?

If so, we suggest the following test points but not limited to them.

**Backend:**
- Increased data-scale: Must work with at least 10k companies, 1m SEPA , 10M SWIFT.
- Within the API, we will add random crashes and ask the candidate to construct a solution to ensure greater reliability & availability.
- Do we want to force any framework or incentivise it?
- Do BE candidates receive only data same as FE candidates, since they need to showcase more on integrating services and system reliability rather than cleaning data?
- Do we want Authentication?

**Frontend:**
- Must have functioning UI - Charts? Graphs? Do we want a dashboard?
- Provide either CSVs or a smaller data footprint & restrictions, since their agenda is to showcase FE skills.
- Do we want to force React framework or incentivise it?
- Do we want Authentication?
