import src.checkForModifiedFiles as sut
from src.stampTimeOnFile import stamp_time_on_file
from tests.helper import add_files
from time import sleep


class TestCheckModifiedFilesAgainstTimestamp(object):
    def test_all_new_files_no_timestamp_file(self, tmpdir):
        file_names = add_files(tmpdir)
        assert sut.check_modified_files_against_timestamp(file_names, tmpdir / 'timestamp') == []

    def test_all_new_files_and_timestamp_file(self, tmpdir):
        file_names = add_files(tmpdir)
        timestamp_file = str(tmpdir / 'timestamp')
        with open(timestamp_file, 'w') as f:
            f.write('1.0')
        assert sut.check_modified_files_against_timestamp(file_names, timestamp_file) == file_names

    def test_some_new_files_and_timestamp_file(self, tmpdir):
        file_names = add_files(tmpdir)
        timestamp_file = str(tmpdir / 'timestamp')
        stamp_time_on_file(timestamp_file)
        sleep(0.001)
        for i in range(2):
            with open(file_names[i], 'a') as f:
                f.write('something new')
        assert sut.check_modified_files_against_timestamp(file_names, timestamp_file) == file_names[:2]

    def test_no_new_files_and_timestamp_file(self, tmpdir):
        file_names = add_files(tmpdir)
        timestamp_file = str(tmpdir / 'timestamp')
        stamp_time_on_file(timestamp_file)
        assert sut.check_modified_files_against_timestamp(file_names, timestamp_file) == []
