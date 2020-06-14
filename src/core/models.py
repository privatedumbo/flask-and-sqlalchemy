from datetime import datetime

from src.core.errors import UnableToMapRecordError, UndefinedValueInRecord

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    """User model. Defined based on input file."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String(128), nullable=False)
    timestamp = Column(DateTime, nullable=False)

    def __init__(self, id: int, username: str, timestamp: str = None):
        self.id = id
        self.username = username
        self.timestamp = timestamp or datetime.utcnow()

    @staticmethod
    def dict_from_tuple(record: tuple) -> dict:
        """
        Based on a row from the file, maps it to a dict to later use it on User instantiation.
        Args:
            record (tuple): row from the file as a tuple.
        Returns:
            dict: dict where each key is a User attribute.
        Raises:
            `src.core.errors.UnableToMapRecordError`: when the dict with User attributes cannot be created
                either due to the input data type or to a missing attribute.
        """
        mapped_record = {}

        try:
            if not all(record) or len(record) > 3:
                raise UndefinedValueInRecord
            mapped_record = {
                "id": int(record[0]),
                "username": record[1],
                "timestamp": record[2],
            }
        except (ValueError, IndexError, UndefinedValueInRecord) as e:
            raise UnableToMapRecordError("Unable to map {} - msg: {}".format(record, e))

        return mapped_record
