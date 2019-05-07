import json
import paramiko

__author__ = 'crmocan'
__date__ = '2019-05-06'
__version__ = 0.02
__description__ = 'This script connects to server through ssh and executes a series of commands'


class SSH(object):
    def __init__(self, settings, server, user, key_file, localpath, remotepath):
        if settings:
            with open(settings, 'r') as settings_file:
                data = json.load(settings_file)
                self.server = data['server']
                self.user = data['user']
                self.key_file = data['keyFile']
                self.localpath = data['localPath']
                self.remotepath = data['remotePath']
            # TODO: Set variables from json file.
            pass
        self.server = server if server else 'esling43.emea.nsn-net.net'
        self.user = user if user else 'crmocan'
        self.key_file = key_file if key_file else 'C:/Users/crmocan/Desktop/id_rsa'
        self.localpath = localpath
        self.remotepath = remotepath

    def _connect_to_esling(self):
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # (paramiko.WarningPolicy())
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
