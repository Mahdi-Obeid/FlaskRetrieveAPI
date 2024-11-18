import os
import requests
from config import db
from models import Company, Status, FinancialStatement
from dotenv import load_dotenv

load_dotenv()
base_url = os.getenv("URL")


def fetch_and_store_data_companies():
    url = f"{base_url}/companies/"
    response = requests.get(url)

    if response.status_code == 200:
        companies_data = response.json().get("data", [])
        print(f"Fetched {len(companies_data)} companies")

        for item in companies_data:
            company = Company.query.filter_by(original_id=item["id"]).first()
            if not company:
                company = Company(original_id=item["id"])

            company.name = item["name"]
            company.symbol = item["symbol"]
            company.national_id = item["national_id"]
            company.source = item["source"]
            company.industry_name = item["industry_name"]
            company.group_name = item["group_name"]
            company.in_market = item["in_market"]

            db.session.merge(company)
        db.session.commit()
        print("Companies data committed to the database.")


def fetch_and_store_data_status():
    companies = Company.query.all()
    print(f"Processing status for {len(companies)} companies")

    for company in companies:
        company_id = company.original_id

        url = f"{base_url}/companies/{company_id}/statements/profile/status/"
        response = requests.get(url)

        if response.status_code == 200:
            status_data = response.json()
            count = status_data.get("count")
            number = status_data.get("number")

            if count is not None and number is not None:
                status = Status.query.filter_by(company_original_id=company_id).first()
                if not status:
                    status = Status(company_original_id=company_id)

                status.count = count
                status.number = number
                db.session.merge(status)
                db.session.commit()


def fetch_and_store_financial_statements(limit=5):
    companies = Company.query.limit(limit).all()
    print(f"Processing financial statements for {len(companies)} companies")

    for company in companies:
        company_id = company.original_id

        url = f"{base_url}/companies/{company_id}/statements/time-series/"
        response = requests.get(url)

        if response.status_code == 200:
            statements_data = response.json().get("data", [])
            print(f"Fetched {len(statements_data)} statements for company {company_id}")

            for statement in statements_data:
                financial_statement = FinancialStatement.query.filter_by(
                    company_id=company_id,
                    period_end=statement["period_end"],
                ).first()

                if not financial_statement:
                    financial_statement = FinancialStatement(
                        company_id=company_id,
                        period_end=statement["period_end"],
                    )

                financial_statement.fiscal_year_end = statement["fiscal_year_end"]
                financial_statement.period_type = statement["period_type"]
                financial_statement.audited = statement["audited"]
                financial_statement.consolidated = statement["consolidated"]
                financial_statement.represented = statement["represented"]

                db.session.merge(financial_statement)

            db.session.commit()
