import datetime as dt
import paramiko
from typing import List

__author__ = 'crmocan'
__date__ = '2019-03-19'
__version__ = 0.01
__description__ = 'This script connects to server through ssh and executes a series of commands'


def connect_to_esling():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # (paramiko.WarningPolicy())
    client.connect('esling43.emea.nsn-net.net', username='crmocan', key_filename='C:/Users/crmocan/Desktop/id_rsa')
    return client


def send_command(command):
    client = connect_to_esling()
    print("send_command: cmd", command)
    alldata = None
    if client:
        stdin, stdout, stderr = client.exec_command(command)
        while not stdout.channel.exit_status_ready():
            # Print data when available
            if stdout.channel.recv_ready():
                alldata = stdout.channel.recv(1024)
                prevdata = b"1"
                while prevdata:
                    prevdata = stdout.channel.recv(1024)
                    alldata += prevdata
                print("send_command: alldata", str(alldata, "utf8"))
    else:
        print("Connection not opened.")
    return alldata


def put_diff(client, localpath, remotepath):
    s = client.open_sftp()
    s.put(localpath, remotepath)
    s.close()


def revert_and_remove(files: List[str]):
    """
    Reverts and removes the files if present on the remote location.
    :param files: List[str] Files to be reverted and removed.
    :return: None
    """
    cmd = 'cd /var/fpwork/crmocan/trunk_dem/dem && {}'
    summarize = files[::]
    summarize.insert(0, 'svn di --summarize')
    summarize = ' '.join(summarize)
    results = send_command(cmd.format(summarize))
    if results is None:
        print('revert_and_remove: Nothing to do')
        return
    sp = str(results, 'utf8').split()
    results = list(zip(sp[0::2], sp[1::2]))
    remove = 'rm'
    revert = 'svn revert'
    for result in results:
        status, file_name = result
        if status == 'A':
            remove = '{} {}'.format(remove, file_name)
            revert = '{} {}'.format(revert, file_name)
        elif status == 'M':
            revert = '{} {}'.format(revert, file_name)
    revertedres = send_command(cmd.format(revert))
    if revertedres:
        print('revert_and_remove: ', str(revertedres, 'utf8'))
    removedres = send_command(cmd.format(remove))
    if removedres:
        print('revert_and_remove: ', str(removedres, 'utf8'))


def apply_diff(file_name: str):
    cmd = 'cd /var/fpwork/crmocan/trunk_dem/dem && {}'
    patch = 'patch -p5 -i {}'.format(file_name)
    results = send_command(cmd.format(patch))
    print('apply_diff: ', results)


def add_to_svn(files: List[str]):
    cmd = 'cd /var/fpwork/crmocan/trunk_dem/dem && {}'
    files.insert(0, 'svn add')
    add = ' '.join(files)
    results = send_command(cmd.format(add))
    print(results)
