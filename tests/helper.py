from os import remove
from time import sleep


def add_files(checkout_dir):
    file_names = ['a.cpp', 'b.hpp', 'c.py']
    file_names = [str(checkout_dir / f) for f in file_names]
    for file in file_names:
        with open(file, 'x'):
            pass
    sleep(0.001)
    return file_names


def remove_files(checkout_dir):
    file_names = ['a.cpp', 'b.hpp', 'c.py']
    file_names = [str(checkout_dir / f) for f in file_names]
    for f in file_names:
        remove(f)
