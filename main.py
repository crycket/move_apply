import pathlib
from checkForModifiedFiles import check_modified_files_against_timestamp
from svn_commands import svn_di_summarize, svn_di_to_file
from move import revert_and_remove, put_diff, apply_diff, add_to_svn, connect_to_esling
from typing import List


def get_files_and_create_patch(localpath: str) -> List[str]:
    """
    The function will create the patch with the latest modifications.
    :param localpath: str - svn repository
    :return: None
    """
    files = svn_di_summarize(localpath)
    files = check_modified_files_against_timestamp(files)
    err = svn_di_to_file(localpath, files)
    files = [pathlib.Path(file).as_posix() for file in files]
    print('get_files_and_create_patch: files ', files)
    if err:
        print(err)
        raise Exception
    return files


def revert_and_apply(files, localpath, remotepath):
    patch = 'patch.diff'
    files = [file[len(localpath.as_posix())+1:] for file in files]
    revert_and_remove(files)
    put_diff(connect_to_esling(), localpath / patch, remotepath / patch)
    apply_diff(patch[1:])
    if files:
        add_to_svn(files)


def start():
    localpath = pathlib.Path(r'C:\Users\crmocan\Desktop\svn')
    remotepath = pathlib.Path('/var/fpwork/crmocan/trunk_dem/dem')
    files = get_files_and_create_patch(localpath)
    revert_and_apply(files, localpath, remotepath)


def start2():
    import json
    settings_path = r'C:\Users\crmocan\Desktop\pyBuildforSublime\move_apply\.localsettings.json'
    f = open(settings_path, 'r')
    settings = json.load(f)
    if settings is None:
        print('Settings are empty')
        return
    import svn_commands2
    local_svn = svn_commands2.SVN(path=settings['local_path'], local=True)
    local_svn.summarize()
    results = local_svn.result.split()
    statuses, files = results[0::2], results[1::2]
    files = check_modified_files_against_timestamp(files)
    if not files:
        print('No changes to send')
        return
    local_svn.diff_to_file(files)

    # Remote work
    import ssh
    ssh_client = ssh.SSH(**settings)
    # send diff to esling
    ssh_client.send_file('patch.diff')

    remote_svn = svn_commands2.SVN(path=settings['remote_path'], local=False)
    import pathlib
    files = [pathlib.PurePath(file).as_posix() for file in files]
    results = ssh_client.send_command(remote_svn.summarize(files))
    if results is None:
        print('Nothing to summarize')
    else:
        results = results.split()
        results = list(zip(results[0::2], results[1::2]))

        # Revert, remove
        removed_files, reverted_files = [], []
        for status, file in results:
            if status == 'A':
                removed_files.append(file)
                reverted_files.append(file)
            if status == 'M':
                reverted_files.append(file)
        if reverted_files:
            ssh_client.send_command(remote_svn.revert(reverted_files))
        if removed_files:
            ssh_client.delete_files(removed_files)

    # Patch
    ssh_client.send_command(remote_svn.patch())


start2()
