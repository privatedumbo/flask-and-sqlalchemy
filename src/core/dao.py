from src.core.config import config
from src.core.models import Base

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class DBManager:
    """
    An SQLAlchemy based DB Manager. Exposes `engine` and `session` attributes to handle
    DB interactions.
    It is also responsible for the DB initialization.
    """

    def __init__(self):
        self.engine = self._engine()
        self.session = self._session()

        Base.metadata.create_all(self.engine)

    def _engine(self):
        engine = create_engine(self.sqlalchemy_uri())
        return engine

    def _session(self):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        return session

    @staticmethod
    def sqlalchemy_uri() -> str:
        return "{}+{}://{}:{}@{}:{}/{}".format(
            config.get("DATABASE", "DIALECT"),
            config.get("DATABASE", "DRIVER"),
            config.get("DATABASE", "USERNAME"),
            config.get("DATABASE", "PASSWORD"),
            config.get("DATABASE", "HOST"),
            config.get("DATABASE", "PORT"),
            config.get("DATABASE", "DB"),
        )


db_manager = DBManager()
