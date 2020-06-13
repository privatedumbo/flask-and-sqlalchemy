from src.core.dao import DBManager
from src.core.models import Base

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(model_class=Base)


def create_app():
    app = Flask(__name__)

    # accepts both /endpoint and /endpoint/ as valid URLs
    app.url_map.strict_slashes = False

    register_namespaces(app)

    register_extensions(app)

    custom_config(app)

    return app


def register_namespaces(app):
    """Register Flask namespaces."""
    from src.server.apis import api

    api.init_app(app)


def register_extensions(app):
    """Register Flask extensions."""

    app.config["SQLALCHEMY_DATABASE_URI"] = DBManager.sqlalchemy_uri()
    # Related to https://github.com/pallets/flask-sqlalchemy/issues/365
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)


def custom_config(app):
    """Configs that don't follow flask documentation but are required by our domain."""

    # Related to https://flask-restful.readthedocs.io/en/0.3.6/quickstart.html?highlight=ERROR_404_HELP
    app.config["ERROR_404_HELP"] = False
