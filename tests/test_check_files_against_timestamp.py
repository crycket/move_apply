from time import sleep

import pytest

from src.check_files import CheckFilesTimestamp
from tests.helper import add_files

timestamp_file = 'timestamp'


@pytest.fixture()
def sut(tmpdir):
    yield CheckFilesTimestamp(tmpdir / 'timestamp')


class TestStampTimeOnFile(object):
    def test_file_exists_and_has_iso_timestamp(self, tmpdir, sut):
        """
        Timestamp file exists and has value 1.0.
        _stamp_time_on_file will return the value inside the timestamp file and update the value.
        """
        iso_timestamp = 1.0
        with open(tmpdir / timestamp_file, 'w') as f:
            f.write(str(iso_timestamp))
        assert sut._stamp_time_on_file() == iso_timestamp
        with open(tmpdir / timestamp_file, 'r') as f:
            assert float(f.read()) != iso_timestamp

    def test_file_exists_and_has_no_iso_timestamp(self, tmpdir, sut):
        """
        Timestamp file exists has no value.
        _stamp_time_on_file will return None and update timestamp file.
        """
        with open(tmpdir / timestamp_file, 'x'):
            pass
        iso_timestamp = sut._stamp_time_on_file()
        assert not iso_timestamp
        with open(tmpdir / timestamp_file, 'r') as f:
            assert float(f.read()) != iso_timestamp

    def test_file_exists_and_has_gibberish(self, tmpdir, sut):
        """
        Timestamp file exists has gibberish.
        _stamp_time_on_file will return None and update timestamp file.
        """
        with open(tmpdir / timestamp_file, 'w') as f:
            f.writelines(['1.0\n', '98.00\ngibberish'])
        iso_timestamp = sut._stamp_time_on_file()
        assert not iso_timestamp
        with open(tmpdir / timestamp_file, 'r') as f:
            assert float(f.read()) != iso_timestamp

    def test_no_file_exists(self, tmpdir, sut):
        """
        Timestamp file doesn't exist.
        _stamp_time_on_file will return the current timestamp and update timestamp file with it.
        """
        with pytest.raises(FileNotFoundError):
            with open(tmpdir / timestamp_file, 'r'):
                pass
        iso_timestamp = sut._stamp_time_on_file()
        with open(tmpdir / timestamp_file, 'r') as f:
            assert float(f.read()) != iso_timestamp


class TestCheckFilesAgainstTimestamp(object):
    """
    add_files:
    tmpdir/a.cpp
          /b.hpp
          /c.py
    """
    def test_all_new_files_no_timestamp_file(self, tmpdir, sut):
        files = dict(zip(add_files(tmpdir), ['A', 'A', 'A']))
        assert sut.check_files_against_timestamp(files) == files

    def test_all_new_files_and_timestamp_file(self, tmpdir, sut):
        files = dict(zip(add_files(tmpdir), ['A', 'A', 'A']))
        with open(timestamp_file, 'w') as f:
            f.write('1.0')
        assert sut.check_files_against_timestamp(files) == files

    def test_some_new_files_and_timestamp_file(self, tmpdir, sut):
        files = dict(zip(add_files(tmpdir), ['A', 'A', 'A']))
        sut._stamp_time_on_file()
        sleep(0.001)
        old_file = None
        for i, file in enumerate(files.keys()):
            if i == 2:
                old_file = file
                continue
            with open(file, 'a') as f:
                f.write('something new')
        del files[old_file]
        assert sut.check_files_against_timestamp(files) == files

    def test_no_new_files_and_timestamp_file(self, tmpdir, sut):
        files = dict(zip(add_files(tmpdir), ['A', 'A', 'A']))
        sut._stamp_time_on_file()
        assert sut.check_files_against_timestamp(files) == dict()

    def test_no_new_files_and_deleted_file(self, tmpdir, sut):
        files = dict(zip(add_files(tmpdir), ['A', 'A', 'A']))
        files[str(tmpdir / 'd.cpp')] = 'D'
        sut._stamp_time_on_file()
        assert sut.check_files_against_timestamp(files) == {str(tmpdir / 'd.cpp'): 'D'}
