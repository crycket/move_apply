import src.svn_commands as sut
import pytest


class TestSvnCommands(object):
    def test_svn_summarize_with_new_files(self, checkout_dir, files_to_check):
        """
        New files added to directory but not under version control.
        Summarize should return empty.
        """
        assert sut.svn_di_summarize(checkout_dir) == []

    def test_svn_summarize_with_new_versioned_files(self, checkout_dir, files_to_check, svn_add):
        """
        New files added to directory by files_to_check then under version control by svn_add.
        sut.svn_di_summarize should return the new files that are under version control.
        """
        file_names = files_to_check
        modified_files = sut.svn_di_summarize(checkout_dir)
        for file in file_names:
            assert file in modified_files

    def test_svn_patch(self, checkout_dir, files_to_check, svn_add):
        """
        New files added to directory by files_to_check then under version control by svn_add.
        sut.svn_di_to_file should create patch.diff and return no error.
        """
        files_names = files_to_check
        assert sut.svn_di_to_file(str(checkout_dir), files_names) == ''
        with pytest.raises(FileExistsError):
            with open(checkout_dir / 'patch.diff', 'x'):
                pass
