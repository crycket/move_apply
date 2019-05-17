import os
import subprocess
from typing import List


__author__ = 'crmocan'
__date__ = '2019-05-16'
__version__ = 0.02
__description__ = ''


class SVNException(Exception):
    """
    Exception raised when svn has unexpected behavior.
    """
    def __init__(self, cmd, message):
        self.cmd = cmd
        self.message = message
        print(self.message)


class SVN(object):
    def __init__(self, path: str, local: bool = True):
        """
        :param path: str - Location of local repository.
        :param local: bool - Execute it locally or send it to remote.
        """
        self._path = path
        self._cmd = 'svn {} {}'
        self._local = local
        if local:
            os.chdir(path)
        self._diff_name = 'patch.diff'
        self.result = None

    def add(self, files: List[str]):
        """
        svn add files
        :param files: The added files.
        :return:
        """
        cmd = self._cmd.format('add', ' '.join(files))
        if self._local:
            self._run(cmd)
        else:
            return cmd

    def diff_to_file(self, files: List[str]):
        """
        svn diff files
        :param files: The diffed files.
        :return:
        """
        cmd = self._cmd.format('diff', ' '.join(files))
        if self._local:
            patch = '{}/{}'.format(self._path, self._diff_name)
            with open(patch, 'w') as f:
                self._run(cmd)
                f.write(self.result)
            # Replace windows endings to unix
            with open(patch, 'rb') as f:
                content = f.read().replace(b'\r\n', b'\n')
            with open(patch, 'wb') as f:
                f.write(content)
        else:
            return cmd

    def patch(self):
        """
        svn patch diff_file
        :return:
        """
        cmd = self._cmd.format('patch', self._diff_name)
        if self._local:
            self._run(cmd)
        else:
            return cmd

    def revert(self, files: List[str]):
        """
        svn revert files
        :param files: The reverted files.
        :return:
        """
        cmd = self._cmd.format('revert', ' '.join(files))
        if self._local:
            self._run(cmd)
        else:
            return cmd

    def summarize(self, files: List[str] = None):
        """
        svn diff --summarize files
        :param files: The summarized files.
        :return:
        """
        if files is None:
            files = ['']
        cmd = self._cmd.format('diff --summarize', ' '.join(files))
        if self._local:
            self._run(cmd)
        else:
            return cmd

    def _run(self, cmd: str):
        """
        Runs the svn commands locally and fill result with the output.
        Will raise SVNException on error.
        :param cmd: the svn cmd to be run
        :return:
        """
        process = subprocess.run(cmd, capture_output=True, text=True)
        if process.stderr:
            print(process.stdout)
            raise SVNException(cmd, process.stderr)
        else:
            self.result = process.stdout
