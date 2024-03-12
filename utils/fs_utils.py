import os
import sys


def get_current_path():
    if getattr(sys, "frozen", False):
        return os.path.abspath(sys.executable)
    else:
        return os.path.abspath(os.path.dirname(__file__))


def get_current_disk():
    return os.path.abspath(os.sep)
