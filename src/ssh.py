from typing import List

from fabric2 import Connection

__author__ = 'crmocan'
__date__ = '2019-05-15'
__version__ = 0.03
__description__ = 'This script connects to server through ssh and executes a series of commands'


class SSH(object):
    def __init__(self, host=None, user=None, key_file=None, local_path=None, remote_path=None):
        self.host = host if host else 'esling43.emea.nsn-net.net'
        self.user = user if user else 'crmocan'
        self.key_file = key_file if key_file else 'C:/Users/crmocan/Desktop/id_rsa'
        self.localpath = local_path
        self.remotepath = remote_path
        self._connection = Connection(host=self.host, user=self.user, connect_kwargs={'key_filename': self.key_file})

    def send_command(self, cmd: str) -> str:
        print('cmd: ', cmd)
        cmd = 'cd {} && {}'.format(self.remotepath, cmd)
        result = self._connection.run(cmd)#, hide='both')
        return result.stdout

    def send_file(self, file_name: str):
        """
        Send file_name to server.
        :param file_name: Name of file to send.
        :return:
        """
        local = '{}/{}'.format(self.localpath, file_name)
        remote = '{}/{}'.format(self.remotepath, file_name)
        result = self._connection.put(local, remote)
        # return result

    def delete_files(self, files: List[str]) -> str:
        """
        Delete remote file.
        :param str files: The file names to be deleted.
        :return str: Output of delete operation.
        :raises Exception: No files to delete.
        """
        if files is None:
            raise Exception('No files to delete.')
        cmd = 'rm {}'.format(' '.join(files))
        return self.send_command(cmd)
