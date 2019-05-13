import concurrent.futures
import os
from typing import List

import paramiko

__author__ = 'crmocan'
__date__ = '2019-05-06'
__version__ = 0.02
__description__ = 'This script connects to server through ssh and executes a series of commands'


class SSH(object):
    def __init__(self, server=None, user=None, key_file=None, local_path=None, remote_path=None):
        self.server = server if server else 'esling43.emea.nsn-net.net'
        self.user = user if user else 'crmocan'
        self.key_file = key_file if key_file else 'C:/Users/crmocan/Desktop/id_rsa'
        self.localpath = local_path
        self.remotepath = remote_path

    def _connect_to_esling(self):
        client = paramiko.SSHClient()
        client.load_host_keys(os.path.expanduser("~/.ssh/known_hosts"))
        # client.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # (paramiko.WarningPolicy())
        client.connect(self.server, username=self.user, key_filename=self.key_file)
        return client

    def send_command(self, cmd: str) -> str:
        print('cmd: ', cmd)
        cmd = 'cd {} && {}'.format(self.remotepath, cmd)
        client = self._connect_to_esling()
        out, err = None, None
        if client:
            stdin, stdout, stderr = client.exec_command(cmd)

            def _receive(output):
                alldata = None
                while not output.channel.exit_status_ready():
                    # Print data when available
                    if output.channel.recv_ready():
                        alldata = output.channel.recv(1024*4)
                        prevdata = b"1"
                        while prevdata:
                            prevdata = output.channel.recv(1024*4)
                            alldata += prevdata
                if alldata:
                    alldata = str(alldata, 'utf8')
                return alldata

            def receive_err(err_out):
                alldata = None
                while not err_out.channel.exit_status_ready():
                    # Print data when available
                    if err_out.channel.recv_stderr_ready():
                        alldata = err_out.channel.recv_stderr(1024*4)
                        prevdata = b"1"
                        while prevdata:
                            prevdata = err_out.channel.recv_stderr(1024*4)
                            alldata += prevdata
                if alldata:
                    alldata = str(alldata, 'utf8')
                return alldata

            with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
                # Start the load operations and mark each future with its URL
                future_err = executor.submit(receive_err, stderr)
                # future_out_err = executor.submit(_receive, stderr)
                future_out = executor.submit(_receive, stdout)
                out = future_out.result()
                print('out: ', out)
                # out_err = future_out_err.result()
                # print('out: ', out_err)
                err = future_err.result()
                print('err: ', err)
            # while not stdout.channel.exit_status_ready():
            #     # Print data when available
            #     if stdout.channel.recv_ready():
            #         alldata = stdout.channel.recv(1024)
            #         prevdata = b"1"
            #         while prevdata:
            #             prevdata = stdout.channel.recv(1024)
            #             alldata += prevdata
            #         print(str(alldata, "utf8"))
        else:
            print('Connection not opened.')
        # if alldata is not None:
        #     alldata = str(alldata, 'utf8')
        return out

    def send_file(self, file_name: str):
        """
        Send file_name to server.
        :param file_name: Name of file to send.
        :return:
        """
        client = self._connect_to_esling()
        sftp_client = client.open_sftp()
        sftp_client.put('{}/{}'.format(self.localpath, file_name), '{}/{}'.format(self.remotepath, file_name))
        sftp_client.close()

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
