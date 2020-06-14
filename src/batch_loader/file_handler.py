import os

from src.batch_loader.data import DEFAULT_BASEDIR
from src.core.errors import FileNotFoundError


class LocalFilesHandler:
    """Helper class to read files into a determined directory in the filesystem."""

    def __init__(self, basedir: str = None):
        self.basedir = basedir or DEFAULT_BASEDIR

    def read(self, fname, header=True, **kwargs):
        """
        Reads a file one line at a time.
        Args:
            fname (str): file to be read.
            header (bool): specifies if the file contains a header or not,
                to skip it.
            **kwargs: passed to the `os.open` function.
        Returns:
            str: row read.
        Raises:
            FileNotFoundError: if required file does not exist.
        """
        fpath = self.get_path(fname)

        if not os.path.exists(fpath):
            raise FileNotFoundError("File {} not found in {}".format(fname, fpath))

        with open(fpath, **kwargs) as f:
            # Skips header when required.
            if header:
                next(f)
            for line in f:
                yield line

    def get_path(self, name: str) -> str:
        """Returns a file path given its name."""
        return os.path.join(self.basedir, name)
