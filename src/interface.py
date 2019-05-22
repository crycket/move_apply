import pathlib

import src.ssh as ssh
import src.svn as svn
from src.check_files import CheckFilesTimestamp


def create_patch(path: str, cft: CheckFilesTimestamp):
    local_svn = svn.SVN(path=path, local=True)
    try:
        local_svn.summarize()
    except svn.SVNException as e:
        return
    results = local_svn.result.split()
    files = dict(zip(results[1::2], results[0::2]))
    files = cft.check_files_against_timestamp(files)
    if not files:
        print('No changes to send')
        return
    local_svn.diff_to_file(list(files.keys()))
    return files


def start(settings):
    cft = CheckFilesTimestamp()
    files = create_patch(settings['local_path'], cft)
    # Remote work
    ssh_client = ssh.SSH(**settings)
    # send diff to esling
    ssh_client.send_file('modiff.diff')
    remote_svn = svn.SVN(path=settings['remote_path'], local=False)
    files = {pathlib.PurePath(file).as_posix(): files[file] for file in files.keys()}
    print(files)
    results = ssh_client.send_command(remote_svn.summarize())
    if results is None:
        print('No remote modifications. Apply patch.')
        ssh_client.send_command(remote_svn.patch())
        return
    else:
        results = results.split()
        results = dict(zip(results[1::2], results[0::2]))

        common = files.keys() & results.keys()
        removed_files, reverted_files = [], []
        # Revert, remove
        for file in common:
            if files[file].startswith('A'):
                removed_files.append(file)
                reverted_files.append(file)
            if files[file].startswith(('M', 'D')):
                reverted_files.append(file)
        if reverted_files:
            ssh_client.send_command(remote_svn.revert(reverted_files))
        if removed_files:
            ssh_client.delete_files(removed_files)

    # Patch
    ssh_client.send_command(remote_svn.patch())
