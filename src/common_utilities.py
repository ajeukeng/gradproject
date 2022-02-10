import os


def check_path(path_name):
    if os.path.exists(path_name):
        return True
    else:
        return False
