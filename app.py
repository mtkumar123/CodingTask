from flask import Flask, request, abort
from flask_restful import Api, Resource
from marshmallow import Schema, fields, validate
import re
import requests
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_apispec.extension import FlaskApiSpec
from flask_apispec.views import MethodResource
from flask_apispec import marshal_with, doc, use_kwargs


def get_url_data(url):
    """
    Handler function to get the payload of the URL specified by the user
    :param url: URL string user wants to obtain the payload for
    :return: Response object from the request sent to the URL
    """
    response = requests.get(url)
    return response


class ping_response_schema(Schema):
    """
    Schema object using Marshmallow specifying the response schema for the ping endpoint.
    """
    status_code = fields.Str(required=True, description="Status Code of the Response")
    payload = fields.Str(required=True, description="Payload of the response")


class info_response_schema(Schema):
    """
    Schema object using Marshmallow specifying the response schema for the info endpoint
    """
    receiver = fields.Str(required=True, description="Hard Coded Text")


class Ping(MethodResource):
    """
    Creating the  Ping endpoint.  This endpoint handles POST calls which have a data payload:
    {"url" : "https://www.google.com". The endpoint response has the following structure:
    {"status_code" : status_code, "payload": payload}
    """
    @doc(description="Help user get payload of URL specified")
    @use_kwargs({"url": fields.Str(required=True, validate=validate.Regexp(regex=r"(http:\/\/www\.\w+\.)|("
                                                                                 r"https:\/\/www\.\w+\.)",
                                                                           flags=re.IGNORECASE))}, location="form")
    @marshal_with(ping_response_schema)
    def post(self, url):
        response = get_url_data(url)
        return {"status_code": response.status_code, "payload": response.text}


class Info(MethodResource):
    """
    Creating the info endpoint. This endpoint handles GET calls. The endpoint response is
    hard coded to always return {"receiver": "Cisco is the best!"}
    """
    @doc(description="Return hardcoded fact that Cisco is the best")
    @marshal_with(info_response_schema)
    def get(self):
        return {"receiver": "Cisco is the best!"}


app = Flask(__name__)
api = Api(app)

api.add_resource(Info, "/info")
api.add_resource(Ping, "/ping")

app.config.update({
    'APISPEC_SPEC': APISpec(
        title='Cisco Project',
        version='v1',
        plugins=[MarshmallowPlugin()],
        openapi_version='2.0.0'
    ),
    'APISPEC_SWAGGER_URL': '/swagger/',  # URI to access API Doc JSON
    'APISPEC_SWAGGER_UI_URL': '/swagger-ui/'  # URI to access UI of API Doc
})
docs = FlaskApiSpec(app)
docs.register(Ping)
docs.register(Info)

if __name__ == "__main__":
    # Keeping debug=True for verbosity purposes.
    app.run(debug=True, host="0.0.0.0")
