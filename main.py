from flask import request
from config import app, db
from models import (
    Company,
    Status,
    FinancialStatement,
    CurrentRatio,
    QuickRatio,
    CashRatio,
)

from fetch import (
    fetch_and_store_data_companies,  # noqa
    fetch_and_store_data_status,  # noqa
    fetch_and_store_financial_statements,  # noqa
)
from flask_apispec import doc, marshal_with
from flask_apispec.views import MethodResource
from schemas import (
    CompanySchema,
    StatusSchema,
    FinancialStatementSchema,
    CurrentRatioSchema,
    QuickRatioSchema,
    CashRatioSchema,
)
from flask.views import MethodView
from swaggerConfig import docs
from datetime import datetime
from dateConverter import jalali_to_gregorian_year
from FinancialRatios.CurrentRatio import calculate_current_ratio  # noqa
from FinancialRatios.QuickRatio import calculate_quick_ratio  # noqa
from FinancialRatios.CashRatio import calculate_cash_ratio  # noqa


class CompanyResource(MethodResource, MethodView):
    @doc(tags=["Companies"])
    @marshal_with(CompanySchema(many=True))
    def get(self):
        companies = Company.query.all()
        return companies


class StatusResource(MethodResource, MethodView):
    @doc(
        tags=["Financial Statements"],
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
    def get(self, original_id):
        status = Status.query.filter_by(company_id=original_id).first()
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


class CurrentRatioResource(MethodResource, MethodView):
    @doc(
        tags=["Financial Ratios"],
        params={
            "original_id": {
                "description": "Company ID",
                "type": "integer",
                "required": True,
                "in": "path",
            },
        },
    )
    @marshal_with(CurrentRatioSchema(many=True))
    def get(self, company_id):
        ratios = CurrentRatio.query.filter_by(company_id=company_id).all()
        return ratios


class QuickRatioResource(MethodResource, MethodView):
    @doc(
        tags=["Financial Ratios"],
        params={
            "original_id": {
                "description": "Company ID",
                "type": "integer",
                "required": True,
                "in": "path",
            },
        },
    )
    @marshal_with(QuickRatioSchema(many=True))
    def get(self, company_id):
        ratios = QuickRatio.query.filter_by(company_id=company_id).all()
        return ratios


class CashRatioResource(MethodResource, MethodView):
    @doc(
        tags=["Financial Ratios"],
        params={
            "original_id": {
                "description": "Company ID",
                "type": "integer",
                "required": True,
                "in": "path",
            },
        },
    )
    @marshal_with(CashRatioSchema(many=True))
    def get(self, company_id):
        ratios = CashRatio.query.filter_by(company_id=company_id).all()
        return ratios


# Convert class to function view
company_view = CompanyResource.as_view("company_resource")
status_view = StatusResource.as_view("status_resource")
financial_statement_view = FinancialStatementResource.as_view(
    "financial_statement_resource"
)
current_ratio_view = CurrentRatioResource.as_view("current_ratio_resource")
quick_ratio_view = QuickRatioResource.as_view("quick_ratio_resource")
cash_ratio_view = CashRatioResource.as_view("cash_ratio_resource")

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
app.add_url_rule(
    "/financial-ratios/current-ratio/<int:company_id>/",
    view_func=current_ratio_view,
)
app.add_url_rule(
    "/financial-ratios/quick-ratio/<int:company_id>/",
    view_func=quick_ratio_view,
)
app.add_url_rule(
    "/financial-ratios/cash-ratio/<int:company_id>/",
    view_func=cash_ratio_view,
)

# Register for Swagger
docs.register(CompanyResource, endpoint="company_resource")
docs.register(StatusResource, endpoint="status_resource")
docs.register(FinancialStatementResource, endpoint="financial_statement_resource")
docs.register(CurrentRatioResource, endpoint="current_ratio_resource")
docs.register(QuickRatioResource, endpoint="quick_ratio_resource")
docs.register(CashRatioResource, endpoint="cash_ratio_resource")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        # fetch_and_store_data_companies()
        # fetch_and_store_data_status(limit=5)
        # fetch_and_store_financial_statements(limit=5)
        calculate_current_ratio()
        calculate_quick_ratio()
        calculate_cash_ratio()

    app.run(debug=True, use_reloader=False)
