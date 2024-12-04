from flask import request
from config import app, db
from models import (
    Company,
    Status,
    FinancialStatement,
    RatioList,
    RatioCalculation,
)
from fetch import (
    fetch_and_store_data_companies,  # noqa
    fetch_and_store_data_status,  # noqa
    fetch_and_store_financial_statements,  # noqa
)
from flask_apispec import doc, marshal_with, use_kwargs
from flask_apispec.views import MethodResource
from schemas import (
    CompanySchema,
    StatusSchema,
    FinancialStatementSchema,
    RatioListSchema,
    RatioCalculationSchema,
)
from flask.views import MethodView
from swaggerConfig import docs
from datetime import datetime
from dateConverter import jalali_to_gregorian_year
from financialRatios import (
    calculate_cash_ratio,
    calculate_current_ratio,
    calculate_quick_ratio,
)


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
        query = FinancialStatement.query.filter_by(company_id=original_id)

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


class RatioCalculationResource(MethodResource, MethodView):
    @doc(
        tags=["Financial Ratios"],
        params={
            "company_id": {
                "description": "Company ID",
                "type": "integer",
                "required": True,
                "in": "path",
            },
            "financial_statement_id": {
                "description": "Financial Statement ID",
                "type": "integer",
                "required": False,
                "in": "query",
            },
            "ratio_list_id": {
                "description": "Ratio List ID",
                "type": "integer",
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
    @marshal_with(RatioCalculationSchema(many=True))
    def get(self, company_id):
        # Get query parameters
        financial_statement_id = request.args.get("financial_statement_id", type=int)
        ratio_list_id = request.args.get("ratio_list_id", type=int)
        year_filter = request.args.get("year_filter", type=int)

        # Query financial ratios
        query = RatioCalculation.query.filter_by(company_original_id=company_id)

        # Apply Filters
        if year_filter:
            gregorian_year = jalali_to_gregorian_year(year_filter)
            start_date = datetime(gregorian_year, 1, 1)
            query = query.filter(RatioCalculation.fiscal_year_end >= start_date)

        if financial_statement_id:
            query = query.filter_by(financial_statement_id=financial_statement_id)

        if ratio_list_id:
            query = query.filter_by(ratio_list_id=ratio_list_id)

        statements = query.all()
        return statements


class RatioListResource(MethodResource):
    @doc(tags=["Ratio List"])
    @use_kwargs(RatioListSchema, location=("json"))
    @marshal_with(RatioListSchema)
    def post(self, **kwargs):
        ratio = RatioList(**kwargs)
        db.session.add(ratio)
        db.session.commit()
        return ratio

    @doc(
        tags=["Ratio List"],
        params={
            "ratio_list_id": {
                "description": "Ratio List ID",
                "type": "integer",
                "required": True,
                "in": "path",
            },
        },
    )
    @marshal_with(RatioListSchema)
    def delete(self, ratio_list_id):
        ratio = RatioList.query.get_or_404(ratio_list_id)
        db.session.delete(ratio)
        db.session.commit()
        return ratio

    @doc(tags=["Ratio List"])
    @marshal_with(RatioListSchema(many=True))
    def get(self):
        ratios = RatioList.query.all()
        return ratios


# Convert class to function view
company_view = CompanyResource.as_view("company_resource")
status_view = StatusResource.as_view("status_resource")
financial_statement_view = FinancialStatementResource.as_view(
    "financial_statement_resource"
)
ratio_calculation_view = RatioCalculationResource.as_view("ratio_calculation_resource")
ratio_list_view = RatioListResource.as_view("ratio_list_resource")

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
    "/companies/<int:company_id>/ratios/",
    view_func=ratio_calculation_view,
)
app.add_url_rule(
    "/companies/add_ratio/",
    view_func=ratio_list_view,
    methods=["POST", "GET"],
)
app.add_url_rule(
    "/companies/delete_ratio/<int:ratio_list_id>/",
    view_func=ratio_list_view,
    methods=["DELETE"],
)

# Register for Swagger
docs.register(CompanyResource, endpoint="company_resource")
docs.register(StatusResource, endpoint="status_resource")
docs.register(FinancialStatementResource, endpoint="financial_statement_resource")
docs.register(RatioCalculationResource, endpoint="ratio_calculation_resource")
docs.register(RatioListResource, endpoint="ratio_list_resource")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        # fetch_and_store_data_companies()
        # fetch_and_store_data_status(limit=5)
        # fetch_and_store_financial_statements(limit=5)
        calculate_cash_ratio()
        calculate_quick_ratio()
        calculate_current_ratio()

    app.run(debug=True, use_reloader=False)
