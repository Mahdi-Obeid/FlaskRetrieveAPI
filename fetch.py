import os
import requests
from config import db
from models import Company
from dotenv import load_dotenv

load_dotenv()
# http://192.168.112.144:5001/api/v2.1
base_url = os.getenv("URL")


def fetch_and_store_data_companies():
    url = f"{base_url}/companies/"
    response = requests.get(url)

    if response.status_code == 200:
        companies_data = response.json().get("data", [])
        print(f"Fetched {len(companies_data)} companies")

        for item in companies_data:
            company = Company(
                id=item["id"],
                name=item["name"],
                symbol=item["symbol"],
                national_id=item["national_id"],
                source=item["source"],
                industry_name=item["industry_name"],
                group_name=item["group_name"],
                in_market=item["in_market"],
            )
            db.session.merge(company)
        db.session.commit()
        print("Companies data committed to the database.")
    else:
        print("Failed to retrieve data from API:", response.status_code)


def fetch_and_store_data_status():
    companies = Company.query.all()
    for company in companies:
        company_id = company.id

        url = f"{base_url}/companies/{company_id}/statements/profile/status/"
        response = requests.get(url)

        if response.status_code == 200:
            status_data = response.json()
            count = status_data.get("count")
            number = status_data.get("number")

            if count is not None and number is not None:
                company.count = count
                company.number = number
                db.session.commit()
                print(
                    f"Updated company {company_id} with count: {count}, number: {number}"
                )
            else:
                print(
                    f"Missing data for company {company_id}: count or number not found"
                )
        else:
            print(
                f"Failed to retrieve status data for company {company_id}: {response.status_code}"
            )

    print("Status data for all companies has been updated.")
