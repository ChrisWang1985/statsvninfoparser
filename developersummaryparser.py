# coding:utf-8

from bs4 import BeautifulSoup
from svndevinfo import SvnDevInfo
import io
import time


class DeveloperSummaryParser:
    def __init__(self, developer_summary_file_path):
        self._dev_summary_file_path = developer_summary_file_path
        self._svn_dev_info = SvnDevInfo()
        self._dev_summary_html_content = ''
        self._soup = None
        self._load_dev_summary_file()

    def _load_dev_summary_file(self):
        with io.open(self._dev_summary_file_path, 'r', encoding='utf-8') as f:
            self._dev_summary_html_content = f.read()

        self._soup = BeautifulSoup(self._dev_summary_html_content,
                                   'html.parser', from_encoding='utf-8')

    def _parse_developer_detail_info_table(self):
        _el_dev_detail_info_tbody = self._soup.select('table')[0].find('tbody')
        _el_dev_detail_info_tr_list = _el_dev_detail_info_tbody.find_all('tr')
        _result_dict_list = []

        for i in range(len(_el_dev_detail_info_tr_list)):
            _result_dict = {}
            _result_dict['author'] = _el_dev_detail_info_tr_list[i].find('th').text
            _result_dict['author_id'] = _el_dev_detail_info_tr_list[i].find_all('td')[0].text
            _result_dict['changes'] = _el_dev_detail_info_tr_list[i].find_all('td')[1].text
            _result_dict['loc'] = _el_dev_detail_info_tr_list[i].find_all('td')[2].text
            _result_dict['lpc'] = _el_dev_detail_info_tr_list[i].find_all('td')[3].text

            _result_dict_list.append(_result_dict)

        return _result_dict_list

    @staticmethod
    def generate_last_m_months_str_list(m):
        now = time.localtime()
        _last_n_months_str_list = []
        _last_n_months_tuple_list = [
            time.localtime(
                time.mktime(
                    (now.tm_year, now.tm_mon - n, 1, 0, 0, 0, 0, 0, 0)
                )
            )[:2]
            for n in range(m)
        ]

        for i in range(len(_last_n_months_tuple_list) - 1):
            _year_str = str(_last_n_months_tuple_list[i][0])
            _month_str = str(_last_n_months_tuple_list[i][1])

            _result_str = _month_str + '/' + _year_str
            _last_n_months_str_list.append(_result_str)

        _13_months_ago_year_str = str(
            _last_n_months_tuple_list[len(_last_n_months_tuple_list) - 1][0])
        _13_months_ago_month_str = str(
            _last_n_months_tuple_list[len(_last_n_months_tuple_list) - 1][1])
        _13_months_ago_result_str = 'Up to ' + _13_months_ago_month_str + '/' \
                                    + _13_months_ago_year_str
        _last_n_months_str_list.append(_13_months_ago_result_str)

        return list(reversed(_last_n_months_str_list))

    def _parse_last_13_months_dev_info(self):
        _last_13_months_title_list = self.generate_last_m_months_str_list(13)
        _last_13_months_dev_info_tbody = self._soup.select('div.section')[0].find('tbody')
        _el_last_13_months_dev_info_tr_list = _last_13_months_dev_info_tbody.find_all('tr')
        _result_dict_list = []

        for i in range(len(_el_last_13_months_dev_info_tr_list)):
            _result_dict = {}
            _result_dict['author'] = _el_last_13_months_dev_info_tr_list[i].find('th').text
            _result_dict[_last_13_months_title_list[12]] = _el_last_13_months_dev_info_tr_list[i].find_all('td')[0].text
            _result_dict[_last_13_months_title_list[11]] = _el_last_13_months_dev_info_tr_list[i].find_all('td')[1].text
            _result_dict[_last_13_months_title_list[10]] = _el_last_13_months_dev_info_tr_list[i].find_all('td')[2].text
            _result_dict[_last_13_months_title_list[9]] = _el_last_13_months_dev_info_tr_list[i].find_all('td')[3].text
            _result_dict[_last_13_months_title_list[8]] = _el_last_13_months_dev_info_tr_list[i].find_all('td')[4].text
            _result_dict[_last_13_months_title_list[7]] = _el_last_13_months_dev_info_tr_list[i].find_all('td')[5].text
            _result_dict[_last_13_months_title_list[6]] = _el_last_13_months_dev_info_tr_list[i].find_all('td')[6].text
            _result_dict[_last_13_months_title_list[5]] = _el_last_13_months_dev_info_tr_list[i].find_all('td')[7].text
            _result_dict[_last_13_months_title_list[4]] = _el_last_13_months_dev_info_tr_list[i].find_all('td')[8].text
            _result_dict[_last_13_months_title_list[3]] = _el_last_13_months_dev_info_tr_list[i].find_all('td')[9].text
            _result_dict[_last_13_months_title_list[2]] = _el_last_13_months_dev_info_tr_list[i].find_all('td')[10].\
                text
            _result_dict[_last_13_months_title_list[1]] = _el_last_13_months_dev_info_tr_list[i].find_all('td')[11].\
                text
            _result_dict[_last_13_months_title_list[0]] = _el_last_13_months_dev_info_tr_list[i].find_all('td')[12].\
                text

            _result_dict_list.append(_result_dict)

        return _result_dict_list

    def get_svn_developer_info(self):
        _total_developers = self._soup.select('dl.attributes dd')[0].text

        self._svn_dev_info.set_total_developers(_total_developers)
        self._svn_dev_info.set_dev_summary_info_dict_list(
            self._parse_developer_detail_info_table()
        )
        self._svn_dev_info.set_dev_last_12_months_info_dict_list(
            self._parse_last_13_months_dev_info()
        )

        return self._svn_dev_info


if __name__ == '__main__':
    _svn_dev_summary_info_parser = DeveloperSummaryParser(
        r'E:\project\opensource\codecount\statsvn\boss\developers.html')
    _svn_dev_summary_info = _svn_dev_summary_info_parser.get_svn_developer_info()
    print _svn_dev_summary_info
