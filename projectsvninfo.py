# coding:utf-8


class ProjectSvnInfo:
    def __init__(self, project_name, svn_url, svn_summary_info,
                 svn_dev_info, svn_file_info, svn_dir_size_info):
        self._project_name = project_name
        self._svn_url = svn_url
        self._summary_info = svn_summary_info
        self._svn_dev_info = svn_dev_info
        self._svn_file_info = svn_file_info
        self._svn_dir_size_info = svn_dir_size_info

    def get_project_name(self):
        return self._project_name

    def get_svn_url(self):
        return self._svn_url

    def get_svn_summary_info(self):
        return self._summary_info

    def get_svn_dev_info(self):
        return self._svn_dev_info

    def get_svn_file_info(self):
        return self._svn_file_info

    def get_svn_dir_info(self):
        return self._svn_dir_size_info
