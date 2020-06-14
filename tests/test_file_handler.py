from src.batch_loader.file_handler import LocalFilesHandler
from src.core.errors import FileNotFoundError

import pytest


class TestFileHandler:

    def test_read_file_returns_str_generator(self, tmpdir):
        test_fname = "test_file.txt"
        p = tmpdir.mkdir("sub").join(test_fname)
        p.write("some original content\nanother original content")

        workdir = LocalFilesHandler(basedir=p.dirname)
        f = workdir.read(test_fname, header=False)

        assert next(f) == "some original content\n"
        assert next(f) == "another original content"

    def test_reading_unexistent_file_raises_not_found_error(self, tmpdir):
        workdir = LocalFilesHandler(basedir="foo")
        f = workdir.read("bar.txt")

        with pytest.raises(FileNotFoundError):
            next(f)
