import os
from datetime import datetime as dt

__author__ = 'crmocan'
__date__ = '2019-05-17'
__version__ = 0.03
__description__ = 'Check for newly added, modified and deleted source files and statuses. Return a dict with them'


class RevertTimestamp(Exception):
    pass


class CheckFilesTimestamp(object):
    def __init__(self, file_name: str = 'timestamp'):
        """
        Keeps track of last time the script was run with success.
        By creating local file with last timestamp.
        :param str file_name: name of file with the timestamp
        """
        self.file_name = file_name
        self.old_time = 0.0

    def revert_to_old_time(self):
        """
        Timestamp reverts to old_time. Should be used when the script fails.
        :return:
        """
        with open(self.file_name, 'wb') as f:
            f.write(str(self.old_time).encode('utf8'))
        print('{} file reverted to old time {}.'.format(self.file_name, self.old_time))

    def check_files_against_timestamp(self, files: dict) -> dict:
        """
        The function will check the provided files and statuses, last modification date.
        File extensions currently supported:  cpp/hpp/py,
        And will return those that are newer than the timestamp.
        :param dict files: Files and statuses to be checked
        :return: dict - Files modified or deleted after timestamp.
        """
        supported_extensions = ['.cpp', '.hpp', '.py']
        m_files = dict()
        timestamp = self._stamp_time_on_file()
        for file in files.keys():
            if os.path.isfile(file):
                file_extension = os.path.splitext(file)[1]
                if file_extension in supported_extensions:
                    m_time = os.path.getmtime(file)
                    if m_time > timestamp:
                        m_files[file] = files[file]
                else:
                    print('File {} wasn\'t added has unsupported extension {}'.format(file, file_extension))
            # Adding deleted file to dict.
            elif files[file].startswith('D'):
                m_files[file] = files[file]
        return m_files

    def _stamp_time_on_file(self) -> float:
        """
        Create time_file with current timestamp the script was used.
        Or get timestamp of the last time it was used.
        :return: float - timestamp inside file
        """
        time = dt.now().timestamp()
        try:
            with open(self.file_name, 'x'):
                pass
        except FileExistsError:
            with open(self.file_name, 'rb') as f:
                try:
                    self.old_time = float(f.read())
                except ValueError:
                    self.old_time = 0.0
        finally:
            with open(self.file_name, 'wb') as f:
                f.write(str(time).encode('utf8'))
                return self.old_time
