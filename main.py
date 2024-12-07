from flask import request
from config import app, db
from models import (
    Company,
    Status,
    FinancialStatement,
)
from fetch import (
    fetch_and_store_data_companies,
    # fetch_and_store_data_status,
    fetch_and_store_financial_statements,
)
from flask_apispec import doc, marshal_with
from flask_apispec.views import MethodResource
from schemas import (
    CompanySchema,
    StatusSchema,
    FinancialStatementSchema,
)
from flask.views import MethodView
from swaggerConfig import docs
from datetime import datetime
from dateConverter import jalali_to_gregorian_year


class CompanyResource(MethodResource, MethodView):
    @doc(tags=["Companies"])
    @marshal_with(CompanySchema(many=True))
    # get method
    def get(self):
        companies = Company.query.all()
        return companies


class StatusResource(MethodResource, MethodView):
    @doc(
        tags=["Companies"],
        params={
            "original_id": {
                "description": "Company ID",
                "type": "integer",
                "required": True,
                "in": "path",
            },
        },
    )
    @marshal_with(StatusSchema)
    # get method
    def get(self, original_id):
        status = Status.query.filter_by(company_original_id=original_id).first()
        return status


class FinancialStatementResource(MethodResource, MethodView):
    @doc(
        tags=["Financial Statements"],
        params={
            "original_id": {
                "description": "Company ID",
                "type": "integer",
                "required": True,
                "in": "path",
            },
            "time_series": {
                "description": "Filter By Number of Years",
                "type": "integer",
                "required": False,
                "in": "query",
            },
            "consolidated": {
                "description": "Filter by Consolidated Statement",
                "type": "boolean",
                "required": False,
                "in": "query",
            },
            "audited": {
                "description": "Filter by Audited Statement",
                "type": "boolean",
                "required": False,
                "in": "query",
            },
            "year_filter": {
                "description": "Filter By Jalali Year",
                "type": "integer",
                "required": False,
                "in": "query",
            },
        },
    )
    @marshal_with(FinancialStatementSchema(many=True))
    def get(self, original_id):
        # Get query parameters
        time_series = request.args.get("time_series", type=int)
        consolidated = request.args.get(
            "consolidated", type=lambda v: v.lower() == "true", default=None
        )
        audited = request.args.get(
            "audited", type=lambda v: v.lower() == "true", default=None
        )
        year_filter = request.args.get("year_filter", type=int)

        # Query financial statements for the company
        query = (
            FinancialStatement.query.filter_by(company_id=original_id)
            .order_by(FinancialStatement.period_end.desc())
            .filter_by(company_id=original_id)
        )

        # Apply Filters
        if year_filter:
            gregorian_year = jalali_to_gregorian_year(year_filter)
            start_date = datetime(gregorian_year, 1, 1)

            query = query.filter(FinancialStatement.fiscal_year_end >= start_date)

        if consolidated is not None:
            query = query.filter(FinancialStatement.consolidated == consolidated)

        if audited is not None:
            query = query.filter(FinancialStatement.audited == audited)

        if time_series:
            query = query.limit(time_series)

        statements = query.all()
        return statements


# Convert class to function view
company_view = CompanyResource.as_view("company_resource")
status_view = StatusResource.as_view("status_resource")
financial_statement_view = FinancialStatementResource.as_view(
    "financial_statement_resource"
)

# Register endpoint
app.add_url_rule(
    "/companies/",
    view_func=company_view,
)
app.add_url_rule(
    "/companies/status/<int:original_id>/",
    view_func=status_view,
)
app.add_url_rule(
    "/companies/<int:original_id>/statements/time-series/",
    view_func=financial_statement_view,
)

# Register for Swagger
docs.register(CompanyResource, endpoint="company_resource")
docs.register(StatusResource, endpoint="status_resource")
docs.register(FinancialStatementResource, endpoint="financial_statement_resource")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        fetch_and_store_data_companies()
        # fetch_and_store_data_status()
        fetch_and_store_financial_statements(limit=5)

    app.run(debug=True, use_reloader=False)
