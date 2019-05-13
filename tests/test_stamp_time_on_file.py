import src.stampTimeOnFile as sut
import pytest


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
