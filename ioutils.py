# coding:utf-8

import os


class IOUtils:
    def __init__(self):
        pass

    @staticmethod
    def make_dirs(path):
        os.makedirs(path)

    @staticmethod
    def get_full_config_file_path(config_file_name):
        return os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            config_file_name)

    @staticmethod
    def is_exists_dir(path):
        return os.path.isdir(path)

    @staticmethod
    def list_dirs(path):
        return os.listdir(path)
