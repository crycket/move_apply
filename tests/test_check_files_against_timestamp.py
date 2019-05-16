from time import sleep

import pytest

import src.check_files as sut
from tests.helper import add_files


class TestStampTimeOnFile(object):
    def test_file_exists_and_has_iso_timestamp(self, tmpdir):
        """
        Timestamp file exists and has value 1.0.
        sut.stamp_time_on_file will return the value inside the timestamp file and update the value.
        """
        file_name = 'timestamp'
        iso_timestamp = 1.0
        with open(tmpdir / file_name, 'w') as f:
            f.write(str(iso_timestamp))
        assert sut.stamp_time_on_file(tmpdir / file_name) == iso_timestamp
        with open(tmpdir / file_name, 'r') as f:
            assert float(f.read()) != iso_timestamp

    def test_file_exists_and_has_no_iso_timestamp(self, tmpdir):
        """
        Timestamp file exists has no value.
        sut.stamp_time_on_file will return None and update timestamp file.
        """
        file_name = 'timestamp'
        with open(tmpdir / file_name, 'x'):
            pass
        iso_timestamp = sut.stamp_time_on_file(tmpdir / file_name)
        assert not iso_timestamp
        with open(tmpdir / file_name, 'r') as f:
            assert float(f.read()) != iso_timestamp

    def test_file_exists_and_has_gibberish(self, tmpdir):
        """
        Timestamp file exists has gibberish.
        sut.stamp_time_on_file will return None and update timestamp file.
        """
        file_name = 'timestamp'
        with open(tmpdir / file_name, 'w') as f:
            f.writelines(['1.0\n', '98.00\ngibberish'])
        iso_timestamp = sut.stamp_time_on_file(tmpdir / file_name)
        assert not iso_timestamp
        with open(tmpdir / file_name, 'r') as f:
            assert float(f.read()) != iso_timestamp

    def test_no_file_exists(self, tmpdir):
        """
        Timestamp file doesn't exist.
        sut.stamp_time_on_file will return the current timestamp and update timestamp file with it.
        """
        file_name = 'timestamp'
        with pytest.raises(FileNotFoundError):
            with open(tmpdir / file_name, 'r'):
                pass
        iso_timestamp = sut.stamp_time_on_file(tmpdir / file_name)
        with open(tmpdir / file_name, 'r') as f:
            assert float(f.read()) != iso_timestamp


class TestCheckFilesAgainstTimestamp(object):
    """
    add_files:
    tmpdir/a.cpp
          /b.hpp
          /c.py
    """
    def test_all_new_files_no_timestamp_file(self, tmpdir):
        files = dict(zip(add_files(tmpdir), ['A', 'A', 'A']))
        assert sut.check_files_against_timestamp(files, tmpdir / 'timestamp') == files

    def test_all_new_files_and_timestamp_file(self, tmpdir):
        files = dict(zip(add_files(tmpdir), ['A', 'A', 'A']))
        timestamp_file = str(tmpdir / 'timestamp')
        with open(timestamp_file, 'w') as f:
            f.write('1.0')
        assert sut.check_files_against_timestamp(files, timestamp_file) == files

    def test_some_new_files_and_timestamp_file(self, tmpdir):
        files = dict(zip(add_files(tmpdir), ['A', 'A', 'A']))
        timestamp_file = str(tmpdir / 'timestamp')
        sut.stamp_time_on_file(timestamp_file)
        sleep(0.001)
        old_file = None
        for i, file in enumerate(files.keys()):
            if i == 2:
                old_file = file
                continue
            with open(file, 'a') as f:
                f.write('something new')
        del files[old_file]
        assert sut.check_files_against_timestamp(files, timestamp_file) == files

    def test_no_new_files_and_timestamp_file(self, tmpdir):
        files = dict(zip(add_files(tmpdir), ['A', 'A', 'A']))
        timestamp_file = str(tmpdir / 'timestamp')
        sut.stamp_time_on_file(timestamp_file)
        assert sut.check_files_against_timestamp(files, timestamp_file) == dict()

    def test_no_new_files_and_deleted_file(self, tmpdir):
        files = dict(zip(add_files(tmpdir), ['A', 'A', 'A']))
        files[str(tmpdir / 'd.cpp')] = 'D'
        timestamp_file = str(tmpdir / 'timestamp')
        sut.stamp_time_on_file(timestamp_file)
        assert sut.check_files_against_timestamp(files, timestamp_file) == {str(tmpdir / 'd.cpp'): 'D'}
