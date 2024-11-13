from config import app, db
from models import Company, Status
from fetch import fetch_and_store_data_companies, fetch_and_store_data_status
from flask_apispec import doc, marshal_with
from flask_apispec.views import MethodResource
from schemas import CompanySchema, StatusSchema
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
    @doc(tags=["Companies"])
    @marshal_with(StatusSchema)
    # get method
    def get(self, original_id):
        status = Status.query.filter_by(company_original_id=original_id).first()
        return status


# Convert class to function view
company_view = CompanyResource.as_view("company_resource")
status_view = StatusResource.as_view("status_resource")

# Register endpoint
app.add_url_rule("/companies/", view_func=company_view)
app.add_url_rule("/status/<int:original_id>", view_func=status_view)

# Register for Swagger
docs.register(CompanyResource, endpoint="company_resource")
docs.register(StatusResource, endpoint="status_resource")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        fetch_and_store_data_companies()
        fetch_and_store_data_status()

    app.run(debug=True)
