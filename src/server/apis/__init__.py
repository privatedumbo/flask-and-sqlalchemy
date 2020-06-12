from .ping import api as ping
from .temperature import api as temperature

from flask_restx import Api


api = Api(
    title="Temperature metrics", version="1.0", description="Temperature Metrics CRUD"
)

api.add_namespace(ping, path="/ping")
api.add_namespace(temperature, path="/temperature")
