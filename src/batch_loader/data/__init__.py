import os

DEFAULT_BASEDIR = os.path.dirname(os.path.abspath(__file__))


def mock_dataset(n_rows: int):
    """
    Generates a file with mock data so that we can test the solution easily with
    different dataset sizes.

    Some imports are done inside the function because we don't want to import
    unused modules just for a use case that is not part of the regular flow.

    Args:
        n_rows (int): number of rows to generate in the mocked dataset.
    """

    import string
    import random
    from datetime import datetime

    from src.core.config import config

    def username() -> str:
        """Generates a random username."""
        letters = string.ascii_lowercase
        return "".join(random.choice(letters) for _ in range(random.randrange(5, 32)))

    def record(id: int, delimiter: str) -> str:
        """Returns a mocked string to be used as input."""
        return (
            str(id) + delimiter + username() + delimiter + str(datetime.utcnow()) + "\n"
        )

    fpath = os.path.join(DEFAULT_BASEDIR, config.get("INPUT_DATA", "FILENAME"))
    delimiter = config.get("INPUT_DATA", "DELIMITER")
    with open(fpath, "w+") as f:
        for i in range(n_rows):
            f.write(record(i, delimiter))
