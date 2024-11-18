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
                "description": "Number of Years 😎",
                "type": "integer",
                "required": False,
                "in": "query",
            },
            # "period_status": {
            #     "description": "accepts 3/6/9/12",
            #     "type": "integer",
            #     "required": False,
            #     "in": "query",
            # },
        },
    )
    @marshal_with(FinancialStatementSchema(many=True))
    def get(self, original_id):
        time_series = request.args.get("time_series", type=int)

        # Query financial statements for the company
        query = FinancialStatement.query.filter_by(company_id=original_id).order_by(
            FinancialStatement.period_end.desc()
        )

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
