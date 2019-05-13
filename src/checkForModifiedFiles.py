import os
from src.stampTimeOnFile import stamp_time_on_file
from typing import List

__author__ = 'crmocan'
__date__ = '2019-03-19'
__version__ = 0.01
__description__ = 'Check for modified source files and return a list with them'


def check_modified_files_against_timestamp(files: List[str], timestamp_file: str = None) -> List[str]:
    """
    The function will check the provided files, that are cpp/hpp/py, last modification date.
    And will return those that are newer than the timestamp.
    :param List[str] files: Files to be checked
    :param str timestamp_file: Files to be checked
    :return: List[str] - Files modified after timestamp
    """
    m_files = []
    if timestamp_file is None:
        timestamp = stamp_time_on_file()
    else:
        timestamp = stamp_time_on_file(timestamp_file)
    for file in files:
        if os.path.isfile(file):
            file_extension = os.path.splitext(file)[1]
            if file_extension in ['.cpp', '.hpp', '.py']:
                m_time = os.path.getmtime(file)
                if m_time > timestamp:
                    m_files.append(file)
            else:
                print('Wrong file extension {}'.format(file_extension))
    return m_files
