# coding:utf-8

from bs4 import BeautifulSoup
from svnfileinfo import SvnFileInfo
import io


class FileSizeAndFileCountInfoParser:
    def __init__(self, file_size_and_file_count_info_file_path):
        self._svn_file_info_file_path = file_size_and_file_count_info_file_path
        self._soup = None
        self._html_content = ''
        self._svn_file_info = SvnFileInfo()
        self._load_file()

    def _load_file(self):
        with io.open(self._svn_file_info_file_path, 'r', encoding='utf-8') as f:
            self._html_content = f.read()

        self._soup = BeautifulSoup(self._html_content, 'html.parser', from_encoding='utf-8')

    def _parse_file_size_info_summary(self):
        _el_svn_file_size_summary_dl = self._soup.select('dl.attributes')[0]
        _total_files = _el_svn_file_size_summary_dl.find_all('dd')[0].text
        _average_file_size = _el_svn_file_size_summary_dl.find_all('dd')[1].text
        _average_revision_per_file = _el_svn_file_size_summary_dl.find_all('dd')[2].text

        self._svn_file_info.set_total_files(_total_files)
        self._svn_file_info.set_average_file_size(_average_file_size)
        self._svn_file_info.set_average_revision_per_file(_average_revision_per_file)

    def _parse_file_types_summary_info(self):
        _el_file_types_summary_tbody = self._soup.select('div.section')[0].find_all('tbody')[0]
        _el_file_types_summary_tr_list = _el_file_types_summary_tbody.find_all('tr')
        _file_types_dict_list = []

        for i in range(len(_el_file_types_summary_tr_list)):
            _file_types_dict = {}
            _file_types_dict['type'] = _el_file_types_summary_tr_list[i].find_all('th')[0].text
            _file_types_dict['files'] = _el_file_types_summary_tr_list[i].find_all('td')[0].text
            _file_types_dict['loc'] = _el_file_types_summary_tr_list[i].find_all('td')[1].text
            _file_types_dict['loc_per_file'] = _el_file_types_summary_tr_list[i].find_all('td')[2].text

            _file_types_dict_list.append(_file_types_dict)

        self._svn_file_info.set_file_types_summary_dict_list(_file_types_dict_list)

    def _parse_largest_file_detail_info(self):
        _el_largest_file_detail_tbody = self._soup.select('div.section')[1].find_all('tbody')[0]
        _el_largest_file_detail_tr_list = _el_largest_file_detail_tbody.find_all('tr')
        _largest_file_detail_dict_list = []

        for i in range(len(_el_largest_file_detail_tr_list)):
            _largest_file_detail_dict = {}
            _largest_file_detail_dict['file'] = _el_largest_file_detail_tr_list[i].find('th').text
            _largest_file_detail_dict['loc'] = _el_largest_file_detail_tr_list[i].find('td').text

            _largest_file_detail_dict_list.append(_largest_file_detail_dict)

        self._svn_file_info.set_largest_files_detail_dict_list(_largest_file_detail_dict_list)

    def _parse_files_with_most_revisions_info(self):
        _el_files_with_most_revisions_tbody = self._soup.select('div.section')[2].find_all('tbody')[0]
        _el_files_with_most_revisions_tr_list = _el_files_with_most_revisions_tbody.find_all('tr')
        _files_with_most_revisions_dict_list = []

        for i in range(len(_el_files_with_most_revisions_tr_list)):
            _files_with_most_revisions_dict = {}
            _files_with_most_revisions_dict['file'] = _el_files_with_most_revisions_tr_list[i].find('th').text
            _files_with_most_revisions_dict['revisions'] = _el_files_with_most_revisions_tr_list[i].find('td').text

            _files_with_most_revisions_dict_list.append(_files_with_most_revisions_dict)

        self._svn_file_info.set_files_with_most_revisions_dict_list(_files_with_most_revisions_dict_list)

    def get_svn_file_info(self):
        self._parse_file_size_info_summary()
        self._parse_file_types_summary_info()
        self._parse_largest_file_detail_info()
        self._parse_files_with_most_revisions_info()

        return self._svn_file_info


if __name__ == '__main__':
    svn_file_info_parser = FileSizeAndFileCountInfoParser(
        r'E:\project\opensource\codecount\statsvn\boss\file_sizes.html')
    svn_file_info = svn_file_info_parser.get_svn_file_info()
    print svn_file_info
