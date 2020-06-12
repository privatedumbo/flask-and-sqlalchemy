import logging

from src.batch_loader.file_handler import LocalFilesHandler
from src.core.dao import db_manager as db
from src.core.config import config
from src.core.models import Temperature

from sqlalchemy.exc import SQLAlchemyError


class Migrator:
    """Class that launches and handles the DB loading process."""

    def __init__(self):
        self.session = db.session

        self.input_fname = config.get("INPUT_DATA", "FILENAME")
        self.batch_size = config.getint("INPUT_DATA", "BATCH_SIZE")
        self.file_handler = LocalFilesHandler()

    def run(self) -> None:
        logging.info("Starting batch load")
        records = self.fetch_records()
        for i, record in enumerate(records):
            temperature = self.temperature_from_record(record)
            self.session.add(temperature)
            if self._batch_size_reached(i):
                self._add_records()

        # Commit remaining records.
        self._add_records()
        logging.info("Batch load finished.")

    def fetch_records(self) -> tuple:
        """Yields each line of the file as a tuple."""
        lines = self.file_handler.read(self.input_fname, header=True)
        for line in lines:
            record = tuple(line.split(config.get("INPUT_DATA", "DELIMITER")))
            yield record

    def temperature_from_record(self, record: tuple) -> Temperature:
        """
        Given a tuple, maps it according to its order and creates a temperature instance to be inserted.
        Args:
            record (tuple): data from a line of the file.
        Returns:
            Temperature: instance of Temperature with the `record` input.
        """
        mapped_record = Temperature.dict_from_tuple(record)
        temperature = Temperature(**mapped_record)
        return temperature

    def _batch_size_reached(self, index: int) -> bool:
        """Defines whether the inserted records should or should not be commited according
        to an user defined param."""
        if self.batch_size < 0:
            return False
        return index % self.batch_size == 0

    def _add_records(self):
        """Handles record insertion. In case of an SQLAlchemy exception, just logs the error and continues.
        It should log errors into an error's file to handle them properly.
        In case of error, all records in the session are rollbacked.
        """
        try:
            self.session.commit()
        except SQLAlchemyError as e:
            logging.error(
                "Error inserting record - msg: {}".format(e.__class__.__name__)
            )
            self.session.rollback()
