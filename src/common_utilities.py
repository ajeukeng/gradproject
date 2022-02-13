import os


def check_path(path_name):
    if os.path.exists(path_name):
        return True
    else:
        return False


def get_file_from_path(filename, calling_file):
    return os.path.join(os.path.dirname(os.path.realpath(calling_file)), filename)
