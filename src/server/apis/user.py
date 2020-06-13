from http import HTTPStatus

from src.core.models import User
from src.server.extensions import db

from flask import abort, request
from flask_restx import Namespace, Resource, fields
from sqlalchemy.exc import SQLAlchemyError


api = Namespace("User", description="Users data.")

user = api.model(
    "User",
    {
        "id": fields.Integer(required=True, description="User identifier"),
        "username": fields.String(required=True, description="Username"),
        "timestamp": fields.DateTime(required=False, descripter="User's creation date"),
    },
)


@api.route("/")
class UserListView(Resource):
    @api.doc("List all users loaded.")
    @api.marshal_list_with(user)
    def get(self):
        try:
            users = User.query.all()
        except SQLAlchemyError as e:
            raise abort(
                HTTPStatus.INTERNAL_SERVER_ERROR,
                {"description": "Internal server error", "detail": str(e)},
            )

        return users

    @api.doc("Creates a user in the database.")
    @api.expect(user)
    @api.marshal_with(user)
    def post(self):
        user_definition = request.get_json(force=True)
        try:
            user = User(**user_definition)
            db.session.add(user)
            db.session.commit()
        except (SQLAlchemyError, TypeError) as e:
            """TypeError is raised if there is an error creating a `User`."""
            db.session.rollback()
            raise abort(
                HTTPStatus.INTERNAL_SERVER_ERROR,
                {"description": "Internal server error", "detail": str(e)},
            )

        return user


@api.route("/<id>")
@api.param("id", "User identifier")
class UserView(Resource):
    @api.doc("Returns the user for the required `id`.")
    @api.marshal_list_with(user)
    def get(self, id):
        try:
            user = User.query.filter(User.id == id).all()
            if not user:
                raise abort(
                    HTTPStatus.NOT_FOUND,
                    {"description": "No record found for id {}".format(id)},
                )
        except SQLAlchemyError as e:
            raise abort(
                HTTPStatus.INTERNAL_SERVER_ERROR,
                {"description": "Internal server error", "detail": str(e)},
            )

        return user
