# coding:utf-8


class SvnDirSizeInfo:
    def __init__(self):
        self._total_dirs = ''
        self._dir_statistics_dict_list = []

    def get_total_dirs(self):
        return self._total_dirs

    def set_total_dirs(self, total_dirs):
        self._total_dirs = total_dirs

    def get_dir_statistics_dict_list(self):
        return self._dir_statistics_dict_list

    def set_dir_statistics_dict_list(self, dir_statistics_dict_list):
        self._dir_statistics_dict_list = dir_statistics_dict_list
