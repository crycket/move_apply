import pathlib

import src.ssh as ssh
import src.svn as svn


def start(settings):
    # import json
    # settings_path = r'C:\Users\crmocan\Desktop\pyBuildforSublime\move_apply\.localsettings.json'
    # f = open(settings_path, 'r')
    # settings = json.load(f)
    # if settings is None:
    #     print('Settings are empty')
    #     return
    local_svn = svn.SVN(path=settings['local_path'], local=True)
    local_svn.summarize()
    results = local_svn.result.split()
    files = dict(zip(results[1::2], results[0::2]))
    from src.check_files import check_files_against_timestamp
    files = check_files_against_timestamp(files)
    if not files:
        print('No changes to send')
        return
    local_svn.diff_to_file(list(files.keys()))

    # Remote work
    ssh_client = ssh.SSH(**settings)
    # send diff to esling
    ssh_client.send_file('patch.diff')

    remote_svn = svn.SVN(path=settings['remote_path'], local=False)
    files = {pathlib.PurePath(file).as_posix(): files[file] for file in files.keys()}
    print(files)
    results = ssh_client.send_command(remote_svn.summarize())
    if results is None:
        print('No remote modifications. Apply patch.')
        ssh_client.send_command(remote_svn.patch())
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
            pass
            ssh_client.send_command(remote_svn.revert(reverted_files))
        if removed_files:
            pass
            ssh_client.delete_files(removed_files)

    # Patch
    ssh_client.send_command(remote_svn.patch())
