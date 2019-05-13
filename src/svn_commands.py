import subprocess
from typing import List


__author__ = 'crmocan'
__date__ = '2019-03-22'
__version__ = 0.01
__description__ = ''


def svn_di_summarize(path: str) -> List[str]:
    """
    Returns a list of added and modified files from svn.
    :param path: str - the svn directory
    :return:
    """
    cmd = 'svn di --summarize '
    if path:
        cmd += str(path)
    else:
        cmd += '.'
    process = subprocess.run(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
    stdout = process.stdout.split()  # [1::2]
    return stdout


def svn_di_to_file(path: str, files: List[str]) -> str:
    """
    Creates a patch.diff with the provided files.
    :param path:
    :param files:
    :return:
    """
    cmd = 'svn di '
    if files:
        for file in files:
            cmd += file + ' '
    else:
        cmd += path
    with open(path + '/patch.diff', 'w') as patch_file:
        process = subprocess.run(cmd, stderr=subprocess.PIPE, stdout=patch_file, text=True)
        stderr = process.stderr
        return stderr


def svn_revert(files: List[str]):
    """
    Reverts files to original state.
    :param files:
    :return:
    """
    cmd = 'svn revert '
    for file in files:
        cmd += file + ' '
