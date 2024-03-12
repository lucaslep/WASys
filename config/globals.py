import os
from utils import get_current_path

# DatBase connection
CONNECTION = None
PATH = None
DIR = None


def set_app_path(file):
    global PATH
    global DIR
    PATH = get_current_path()
    DIR = os.path.dirname(PATH)


def get_app_path():
    return PATH


def get_app_dir():
    return os.path.dirname(PATH)


def set_db_connection(conn):
    global CONNECTION
    CONNECTION = conn


def get_db_connection():
    return CONNECTION
