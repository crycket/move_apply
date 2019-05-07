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
    if err:
        print(err)
        raise Exception
    return files


def revert_and_apply(files, localpath, remotepath):
    patch = '/patch.diff'
    revert_and_remove(files)
    put_diff(connect_to_esling(), localpath + patch, remotepath + patch)
    apply_diff(patch[1:])
    if files:
        add_to_svn(files)


def start():
    localpath = r'C:\Users\crmocan\Desktop\svn'
    remotepath = '/var/fpwork/crmocan/trunk_dem/dem'
    files = get_files_and_create_patch(localpath)
    revert_and_apply(files, localpath, remotepath)


start()
