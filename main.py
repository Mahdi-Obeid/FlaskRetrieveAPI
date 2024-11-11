from flask import jsonify
from config import app, db
from models import Company
from fetch import (
    fetch_and_store_data_companies,
    fetch_and_store_data_status,
)


@app.route("/companies", methods=["GET"])
def get_companies():
    companies = Company.query.all()
    print(f"Retrieved {len(companies)} companies from the database.")

    data = [
        {
            "id": company.id,
            "name": company.name,
            "symbol": company.symbol,
            "national_id": company.national_id,
            "source": company.source,
            "industry_name": company.industry_name,
            "group_name": company.group_name,
            "in_market": company.in_market,
            "count": company.count,
            "number": company.number,
        }
        for company in companies
    ]

    return jsonify({"data": data})


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        fetch_and_store_data_companies()
        fetch_and_store_data_status()

    app.run()
