# coding:utf-8


class ReportInfo:
    def __init__(self, product_name):
        self._product_name = product_name
        self._project_info_list = []

    def add_project_info(self, project_svn_info):
        self._project_info_list.append(project_svn_info)

    def get_project_info_list(self):
        return self._project_info_list

    def get_product_name(self):
        return self._product_name
