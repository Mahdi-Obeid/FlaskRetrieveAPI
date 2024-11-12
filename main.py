from config import app, db
from models import Company
from fetch import fetch_and_store_data_companies, fetch_and_store_data_status
from flask_apispec import doc, marshal_with
from flask_apispec.views import MethodResource
from schemas import CompanySchema
from flask.views import MethodView
from swaggerConfig import docs


class CompanyResource(MethodResource, MethodView):
    @doc(tags=["Companies"])
    @marshal_with(CompanySchema(many=True))
    # get method
    def get(self):
        companies = Company.query.all()
        return companies


# Convert class to function view
company_view = CompanyResource.as_view("company_resource")

# Register endpoint
app.add_url_rule("/companies/", view_func=company_view)

# Register for Swagger
docs.register(CompanyResource, endpoint="company_resource")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        fetch_and_store_data_companies()
        fetch_and_store_data_status(limit=100)

    app.run(debug=True)
