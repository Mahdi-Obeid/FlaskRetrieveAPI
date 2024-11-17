import os
import requests
from config import db
from models import Company, Status, FinancialStatement, FinancialStatementItem
from dotenv import load_dotenv
from datetime import datetime

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
    else:
        print("Failed to retrieve data from API:", response.status_code)


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
        else:
            print(
                f"Failed to retrieve status data for company {company_id}: {response.status_code}"
            )

    print("Status data for all companies has been updated.")


def fetch_and_store_financial_statements():
    companies = Company.query.all()
    print(f"Processing financial statements for {len(companies)} companies")

    for company in companies:
        company_id = company.original_id

        url = f"{base_url}/companies/{company_id}/statements/time-series/"
        response = requests.get(url)

        if response.status_code == 200:
            statements_data = response.json().get("data", [])
            print(f"Fetched {len(statements_data)} statements for company {company_id}")

            for statement_data in statements_data:
                # Convert string dates to datetime.date objects
                period_end = datetime.strptime(statement_data["period_end"], "%Y-%m-%d").date()
                fiscal_year_end = datetime.strptime(statement_data["fiscal_year_end"], "%Y-%m-%d").date()

                # Check if statement already exists
                statement = FinancialStatement.query.filter_by(
                    company_id=company.original_id,
                    period_end=period_end,
                    fiscal_year_end=fiscal_year_end,
                    period_type=statement_data["period_type"]
                ).first()

                if not statement:
                    statement = FinancialStatement(company_id=company.original_id)

                # Update statement attributes
                statement.period_end = period_end
                statement.fiscal_year_end = fiscal_year_end
                statement.period_type = statement_data["period_type"]
                statement.audited = statement_data["audited"]
                statement.consolidated = statement_data["consolidated"]
                statement.represented = statement_data["represented"]

                db.session.merge(statement)
                db.session.flush()  # Get the statement ID for items

                # Process statement items
                for item_data in statement_data.get("items", []):
                    item = FinancialStatementItem(
                        id=item_data["id"],
                        financial_statement_id=statement.id,
                        noavaran_id=item_data["noavaran_id"],
                        level_order=item_data["level_order"],
                        title=item_data["title"],
                        financial_statement_item_id=item_data["financial_statement_item_id"],
                        amount=item_data["amount"],
                        statement_type=item_data["statement_type"]
                    )
                    db.session.add(item)


            db.session.commit()
            print(f"Financial statements for company {company_id} committed to database")
        else:
            print(f"Failed to retrieve financial statements for company {company_id}: {response.status_code}")

    print("Financial statements for all companies have been updated.")