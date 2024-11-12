from config import app
from flask_apispec import FlaskApiSpec
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin


app.config.update(
    {
        "APISPEC_SPEC": APISpec(
            title="Companies API",
            version="0.0.0",
            plugins=[MarshmallowPlugin()],
            openapi_version="2.0",
        ),
        "APISPEC_SWAGGER_URL": "/swagger/",
        "APISPEC_SWAGGER_UI_URL": "/swagger-ui/",
    }
)


docs = FlaskApiSpec(app)
