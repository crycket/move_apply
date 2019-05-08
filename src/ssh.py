import json
import os
import paramiko

__author__ = 'crmocan'
__date__ = '2019-05-06'
__version__ = 0.02
__description__ = 'This script connects to server through ssh and executes a series of commands'


class SSH(object):
    def __init__(self, server=None, user=None, key_file=None, localpath=None, remotepath=None):
        self.server = server if server else 'esling43.emea.nsn-net.net'
        self.user = user if user else 'crmocan'
        self.key_file = key_file if key_file else 'C:/Users/crmocan/Desktop/id_rsa'
        self.localpath = localpath
        self.remotepath = remotepath

    def _connect_to_esling(self):
        client = paramiko.SSHClient()
        client.load_host_keys(os.path.expanduser("~/.ssh/known_hosts"))
        # client.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # (paramiko.WarningPolicy())
        client.connect(self.server, username=self.user, key_filename=self.key_file)
        return client

    def send_command(self, cmd: str):
        client = self._connect_to_esling()
        alldata = None
        if client:
            stdin, stdout, stderr = client.exec_command(cmd)
            while not stdout.channel.exit_status_ready():
                # Print data when available
                if stdout.channel.recv_ready():
                    alldata = stdout.channel.recv(1024)
                    prevdata = b"1"
                    while prevdata:
                        prevdata = stdout.channel.recv(1024)
                        alldata += prevdata
                    print(str(alldata, "utf8"))
        else:
            print("Connection not opened.")
        return alldata

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
