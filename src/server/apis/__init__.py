from .ping import api as ping
from .user import api as user

from flask_restx import Api


api = Api(
    title="Users data", version="1.0", description="Users CRUD"
)

api.add_namespace(ping, path="/ping")
api.add_namespace(user, path="/users")
