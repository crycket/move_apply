import datetime as dt

__author__ = 'crmocan'
__date__ = '2019-03-19'
__version__ = 0.01
__description__ = 'Create time_file with current timestamp the script was used.\
    Or get timestamp of the last time it was used.'


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
