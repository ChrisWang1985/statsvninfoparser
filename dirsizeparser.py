# coding:utf-8

from bs4 import BeautifulSoup
from svndirsizeinfo import SvnDirSizeInfo
import io
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class DirSizeParser:
    def __init__(self, dir_size_file_path):
        self._dir_size_file_path = dir_size_file_path
        self._html_content = ''
        self._soup = None
        self._svn_dir_size_info = SvnDirSizeInfo()
        self._load_file()

    def _load_file(self):
        with io.open(self._dir_size_file_path, 'r', encoding='utf-8') as f:
            self._html_content = f.read()

        self._soup = BeautifulSoup(self._html_content, 'html.parser', from_encoding='utf-8')

    def _parse_dir_statistics(self):
        _el_dir_stat_tbody = self._soup.select('div.section')[0].find('tbody')
        _el_dir_stat_tr_list = _el_dir_stat_tbody.find_all('tr')
        _dir_stat_dict_list = []

        for i in range(len(_el_dir_stat_tr_list)):
            _dir_stat_dict = {}
            _dir_stat_dict['dir'] = _el_dir_stat_tr_list[i].find('th').text
            _dir_stat_dict['change'] = _el_dir_stat_tr_list[i].find_all('td')[0].text
            _dir_stat_dict['loc'] = _el_dir_stat_tr_list[i].find_all('td')[1].text

            _dir_stat_dict_list.append(_dir_stat_dict)

        self._svn_dir_size_info.set_dir_statistics_dict_list(_dir_stat_dict_list)

    def get_dir_stat_info(self):
        _el_dir_size_total_num = self._soup.select('dl.attributes')[0]
        _total_dirs = _el_dir_size_total_num.find('dd').text

        self._svn_dir_size_info.set_total_dirs(_total_dirs)

        self._parse_dir_statistics()

        return self._svn_dir_size_info


if __name__ == "__main__":
    _svn_dir_stat_parser = DirSizeParser(r'E:\project\opensource\codecount\statsvn\boss\dir_sizes.html')
    _svn_dir_stat_info = _svn_dir_stat_parser.get_dir_stat_info()
    print _svn_dir_stat_info
