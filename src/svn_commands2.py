import subprocess
from typing import List


__author__ = 'crmocan'
__date__ = '2019-05-06'
__version__ = 0.02
__description__ = ''


class SVNException(Exception):
    """
    Exception raised when svn has unexpected behavior.
    """
    def __init__(self, message):
        self.message = message
        print(self.message)


class SVN(object):
    def __init__(self, path: str, local: bool = None):
        """
        :param path: str - Location of local repository.
        :param local: bool - Execute it locally or send it to remote.
        """
        self._path = path
        self._local = True if local is None else False
        self._diff_name = 'patch.diff'
        self._cmd = 'svn {} {}'
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

    def diff_to_file(self, files: List[str] = '.'):
        """
        svn diff files
        :param files: The diffed files.
        :return:
        """
        cmd = self._cmd.format('diff', ' '.join(files))
        if self._local:
            with open('{}/{}'.format(self._path, self._diff_name)) as f:
                f.write(self._run(cmd))
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
        cmd = self._cmd.format('di --summarize', self._path if files is None else files)
        if self._local:
            self._run(cmd)
            self.result = self.result.split()
        else:
            return cmd

    def _run(self, cmd: str):
        """
        Runs the svn commands locally and fill result with the output.
        Will raise SVNException on error.
        :param cmd: the svn cmd to be run
        :return:
        """
        process = subprocess.run(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
        if process.stderr:
            print(process.stdout)
            raise SVNException(process.stderr)
        else:
            self.result = process.stdout
