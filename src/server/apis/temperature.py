from http import HTTPStatus

from src.core.models import Temperature

from flask import abort, render_template, make_response
from flask_restx import Namespace, Resource, fields
from sqlalchemy.exc import SQLAlchemyError


api = Namespace("Temperature", description="Temperature measurement & metrics CRUD")

temperature = api.model(
    "Temperature",
    {
        "id": fields.String(required=True, description="The temperature identifier"),
        "timestamp": fields.DateTime(required=True, descripter="Measurement timestamp"),
        "temperature": fields.Float(required=True, description="Temperature measured"),
        "duration": fields.String(required=True, description="Duration of the measure"),
    },
)


def render_temperature(temperature: list):
    response = make_response(render_template("index.html", temperatures=temperature))
    response.headers["Content-Type"] = "text/html"
    return response


@api.route("/")
class TemperatureListView(Resource):
    @api.doc("List all temperatures loaded.")
    @api.marshal_list_with(temperature)
    def get(self):
        try:
            temperatures = Temperature.query.all()
        except SQLAlchemyError as e:
            raise abort(
                HTTPStatus.INTERNAL_SERVER_ERROR,
                {"description": "Internal server error", "detail": str(e)},
            )

        return temperatures


@api.route("/<id>")
@api.param("id", "The temperature identifier")
class TemperatureView(Resource):
    @api.doc("Returns the temperature for the required `id`.")
    @api.marshal_list_with(temperature)
    def get(self, id):
        try:
            temperature = Temperature.query.filter(Temperature.id == id).all()
            if not temperature:
                raise abort(
                    HTTPStatus.NOT_FOUND,
                    {"description": "No record found for id {}".format(id)},
                )
        except SQLAlchemyError as e:
            raise abort(
                HTTPStatus.INTERNAL_SERVER_ERROR,
                {"description": "Internal server error", "detail": str(e)},
            )

        return temperature
