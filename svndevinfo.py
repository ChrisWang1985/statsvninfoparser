# coding:utf-8


class SvnDevInfo:
    def __init__(self, ):
        self._total_developers = ''
        self._dev_summary_info_dict_list = []
        self._dev_last_12_months_info_dict_list = []

    def get_total_developers(self):
        return self._total_developers

    def set_total_developers(self, total_devs):
        self._total_developers = total_devs

    def get_dev_summary_info_dict_list(self):
        return self._dev_summary_info_dict_list

    def set_dev_summary_info_dict_list(self, dev_summary_info_dict_list):
        self._dev_summary_info_dict_list = dev_summary_info_dict_list

    def get_dev_last_12_months_info_dict_list(self):
        return self._dev_last_12_months_info_dict_list

    def set_dev_last_12_months_info_dict_list(self, dev_last_12_months_info_dict_list):
        self._dev_last_12_months_info_dict_list = dev_last_12_months_info_dict_list

    def get_dev_last_12_months_info_by_author(self, author_id):
        for i in range(len(self._dev_last_12_months_info_dict_list)):
            if self._dev_last_12_months_info_dict_list[i].get('author') == author_id:
                return self._dev_last_12_months_info_dict_list[i]
