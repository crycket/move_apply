import datetime as dt
import os

__author__ = 'crmocan'
__date__ = '2019-05-14'
__version__ = 0.02
__description__ = 'Check for newly added, modified and deleted source files and statuses. Return a dict with them'


def stamp_time_on_file(file_name: str = 'timestamp') -> float:
    """
    Create time_file with current timestamp the script was used.
    Or get timestamp of the last time it was used.
    :param str file_name: name of file with the timestamp
    :return: float - timestamp inside file
    """
    timestamp = dt.datetime.now().timestamp()
    f_timestamp = 0.0
    try:
        with open(file_name, 'x'):
            pass
        # f_timestamp = timestamp
    except FileExistsError:
        with open(file_name, 'r') as f:
            f_timestamp = float(f.read())
    finally:
        with open(file_name, 'w') as f:
            f.write(str(timestamp))
            return f_timestamp


def check_files_against_timestamp(files: dict, timestamp_file: str = None) -> dict:
    """
    The function will check the provided files and statuses,
    that are cpp/hpp/py, last modification date.
    And will return those that are newer than the timestamp.
    :param dict files: Files and statuses to be checked
    :param str timestamp_file: File with timestamp in it.
    :return: dict - Files modified or deleted after timestamp.
    """
    m_files = dict()
    if timestamp_file is None:
        timestamp = stamp_time_on_file()
    else:
        timestamp = stamp_time_on_file(timestamp_file)
    for file in files.keys():
        if os.path.isfile(file):
            file_extension = os.path.splitext(file)[1]
            if file_extension in ['.cpp', '.hpp', '.py']:
                m_time = os.path.getmtime(file)
                if m_time > timestamp:
                    m_files[file] = files[file]
            else:
                print('Wrong file extension {}'.format(file_extension))
        # Adding deleted file to dict.
        elif files[file].startswith('D'):
            m_files[file] = files[file]
    return m_files
