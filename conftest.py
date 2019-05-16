import os
import shutil
import stat
import subprocess
import time

import pytest


@pytest.fixture(scope="session")
def checkout_dir(tmp_path_factory):
    svn_repo = tmp_path_factory.mktemp('svn_repo')
    checkout = tmp_path_factory.getbasetemp() / 'rep'
    subprocess.run('svnadmin create ' + str(svn_repo), shell=True)
    cmd = ''.join(['svn co ', svn_repo.as_uri(), ' ', str(checkout)])
    subprocess.run(cmd, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL, shell=True)
    yield checkout

    def remove_readonly(func, path, _):
        """Clear the readonly bit and reattempt the removal"""
        os.chmod(path, stat.S_IWRITE)
        func(path)
    shutil.rmtree(svn_repo, onerror=remove_readonly)
    shutil.rmtree(checkout, onerror=remove_readonly)


@pytest.fixture(scope='function')
def files_to_check(checkout_dir):
    file_names = ['a.cpp', 'b.hpp', 'c.py']
    file_names = [str(checkout_dir / f) for f in file_names]
    for file in file_names:
        with open(file, 'x'):
            pass
    time.sleep(0.001)
    yield file_names
    for f in file_names:
        os.remove(f)


@pytest.fixture(scope='function')
def svn_add(files_to_check):
    subprocess.run('svn add ' + ' '.join(files_to_check), stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
    yield None
    subprocess.run('svn revert -R ' + str(checkout_dir), stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
