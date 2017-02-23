# coding:utf-8

from bs4 import BeautifulSoup
from svnsummaryinfo import SvnSummaryInfo
import io


class HtmlSummaryParser:
    def __init__(self, summary_file_path):
        self.summary_file_path = summary_file_path
        self.html_content = ''
        self.soup = None
        self.svn_summary_info = SvnSummaryInfo()
        self._load_file()

    def _load_file(self):
        with io.open(self.summary_file_path, 'r', encoding='utf-8') as f:
            self.html_content = f.read()

        self.soup = BeautifulSoup(self.html_content, 'html.parser', from_encoding='utf-8')

    def _parse_top_10_dev_table(self):
        _el_top_10_table_body = self.soup.select('table')[0].find('tbody')
        _el_top_10_tr_list = _el_top_10_table_body.find_all('tr')
        _result_dict_list = []

        for i in range(len(_el_top_10_tr_list)):
            _result_dict = {}
            _result_dict["author"] = _el_top_10_tr_list[i].find('th').text
            _result_dict["loc"] = _el_top_10_tr_list[i].find('td').text
            _result_dict_list.append(_result_dict)

        return _result_dict_list

    def get_svn_summary_info(self):
        _el_title = self.soup.select('h1')[0]
        _attr_dd_list = self.soup.select('dl.attributes dd')

        _el_title_text = _el_title.text
        _title = _el_title_text[_el_title_text.rfind('/'):]

        _generated_time = _attr_dd_list[0].text
        _head_revision = _attr_dd_list[1].text

        _el_report_period = _attr_dd_list[2]

        _report_period_start_time = _el_report_period.find_all('span')[0].text
        _report_period_end_time = _el_report_period.find_all('span')[1].text
        _total_files = _attr_dd_list[3].text
        _total_loc = _attr_dd_list[4].text
        _developers = _attr_dd_list[5].text

        self.svn_summary_info.set_product_title(_title)
        self.svn_summary_info.set_generate_time(_generated_time)
        self.svn_summary_info.set_head_revision(_head_revision)
        self.svn_summary_info.set_report_period_start_time(_report_period_start_time)
        self.svn_summary_info.set_report_period_end_time(_report_period_end_time)
        self.svn_summary_info.set_total_files(_total_files)
        self.svn_summary_info.set_total_line_of_codes(_total_loc)
        self.svn_summary_info.set_developers(_developers)
        self.svn_summary_info.set_top_10_dev_dict(
            self._parse_top_10_dev_table()
        )

        return self.svn_summary_info

if __name__ == '__main__':
    summary_parser = HtmlSummaryParser(r'E:\project\opensource\codecount\statsvn\boss\index.html')
    svn_summary_info = summary_parser.get_svn_summary_info()
