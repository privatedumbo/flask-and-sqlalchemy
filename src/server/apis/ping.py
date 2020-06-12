from flask_restx import Namespace, Resource, fields

api = Namespace("Ping", description="API Health check endpoint")

ping = api.model(
    "Ping",
    {
        "ping": fields.String(
            required=True,
            description="Any string value to assert API proper functionality",
        )
    },
)


HEALTH_CHECK_RESPONSE = {"ping": "pong"}


@api.route("/")
class Ping(Resource):
    @api.doc("Health check response")
    @api.marshal_with(ping)
    def get(self):
        return HEALTH_CHECK_RESPONSE
