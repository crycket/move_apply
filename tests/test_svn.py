import pytest

import src.svn as sut


class TestSvnLocal(object):
    def test_summarize_with_new_files(self, checkout_dir, files_to_check):
        """
        New files added to directory but not under version control.
        Summarize should return empty.
        """
        svn = sut.SVN(path=checkout_dir, local=True)
        svn.summarize(checkout_dir)
        assert svn.result == []

    def test_summarize_with_new_versioned_files(self, checkout_dir, files_to_check, svn_add):
        """
        New files added to directory by files_to_check then under version control by svn_add.
        sut.svn_di_summarize should return the new files that are under version control.
        """
        svn = sut.SVN(path=checkout_dir, local=True)
        file_names = files_to_check
        svn.summarize(file_names)
        modified_files = svn.result
        for file in file_names:
            assert file in modified_files

    def test_diff(self, checkout_dir, files_to_check, svn_add):
        """
        New files added to directory by files_to_check then under version control by svn_add.
        sut.svn_di_to_file should create patch.diff and return no error.
        """
        files_names = files_to_check
        svn = sut.SVN(path=checkout_dir, local=True)
        svn.diff_to_file(files_names)
        with pytest.raises(FileExistsError):
            with open(checkout_dir / 'patch.diff', 'x'):
                pass
# TODO: Add more tests


class TestSvnRemote(object):
    @pytest.mark.parametrize('cmd, cmd_str', [(sut.SVN.add, 'add'), (sut.SVN.diff_to_file, 'diff'),
                                              (sut.SVN.revert, 'revert'), (sut.SVN.summarize, 'diff --summarize')])
    def test_remote(self, cmd, cmd_str):
        path = 'cd /var/fpwork/crmocan/trunk_dem/dem'
        svn = sut.SVN(path=path, local=False)
        files = ['a.cpp', 'b.hpp', 'c.py']
        cd = 'cd {}'.format(path)
        svn_cmd = 'svn {} {}'.format(cmd_str, ' '.join(files))
        assert cmd(svn, files) == '{} && {}'.format(cd, svn_cmd)

    def test_diff(self):
        path = 'cd /var/fpwork/crmocan/trunk_dem/dem'
        svn = sut.SVN(path=path, local=False)
        print(svn.diff_to_file([]))