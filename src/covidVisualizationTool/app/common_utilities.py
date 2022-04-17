import logging
import os
from datetime import date


def check_path(path_name):
    if os.path.exists(path_name):
        return True
    else:
        return False


def get_file_from_path(filename, calling_file):
    return os.path.join(os.path.dirname(os.path.realpath(calling_file)), filename)


class CommonUtilities:
    def __init__(self):
        self.date = date.today()
        log_filename = os.path.join('../../../logs', f'cvt{self.date}.log')
        logging.basicConfig(filename=get_file_from_path(log_filename, __file__),
                            filemode='w', format='%(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
        self.logger = logging.getLogger()

    def cvt_logger(self):
        self.logger.setLevel(logging.DEBUG)
        return self.logger
