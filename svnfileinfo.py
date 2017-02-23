# coding:utf-8


class SvnFileInfo:
    def __init__(self):
        self._total_files = ''
        self._average_file_size = ''
        self._average_revision_per_file = ''
        self._file_types_summary_dict_list = []
        self._largest_files_detail_dict_list = []
        self._files_with_most_revisions_dict_list = []

    def get_total_files(self):
        return self._total_files

    def set_total_files(self, total_files):
        self._total_files = total_files

    def get_average_file_size(self):
        return self._average_file_size

    def set_average_file_size(self, average_file_size):
        self._average_file_size = average_file_size

    def get_average_revision_per_file(self):
        return self._average_revision_per_file

    def set_average_revision_per_file(self, average_revision_per_file):
        self._average_revision_per_file = average_revision_per_file

    def get_file_types_summary_dict_list(self):
        return self._file_types_summary_dict_list

    def set_file_types_summary_dict_list(self, file_type_summary_dict_list):
        self._file_types_summary_dict_list = file_type_summary_dict_list

    def get_largest_files_detail_dict_list(self):
        return self._largest_files_detail_dict_list

    def set_largest_files_detail_dict_list(self, largest_files_detail_dict_list):
        self._largest_files_detail_dict_list = largest_files_detail_dict_list

    def get_files_with_most_revisions_dict_list(self):
        return self._files_with_most_revisions_dict_list

    def set_files_with_most_revisions_dict_list(self, files_with_most_revisions_dict_list):
        self._files_with_most_revisions_dict_list = files_with_most_revisions_dict_list
