# coding:utf-8

import datetime
from configdictionary import ConfigDict
from product_ini_parser import ProductIniParser
from ioutils import IOUtils


class CommandWarp:
    def __init__(self, product_info_obj):
        self._cmd_flow_list = []
        self._product_info = product_info_obj

    def _get_sync_code_command_text(self, product_path_dict):
        src_dir = product_path_dict['src']
        svn_url = product_path_dict['url']

        if len(IOUtils.list_dirs(src_dir)) > 0:
            _sync_code_cmd_text = \
                'cd %s;svn up --username xuwenlong --password xuwenlong1' % src_dir
        else:
            _sync_code_cmd_text = \
                'svn co %s %s --username xuwenlong --password xuwenlong1' % (svn_url, src_dir)

        return _sync_code_cmd_text

    def _get_svn_log_command_text(self, product_info_dict):
        date_time_template = '%Y-%m-%d'
        today_date = datetime.datetime.strftime(datetime.datetime.now(), date_time_template)
        half_year_date = datetime.datetime.strftime(
            datetime.datetime.now() + datetime.timedelta(days=-180), date_time_template)
        log_name = product_info_dict['log_full_path']
        svn_src_path = product_info_dict['src']

        _svn_log_cmd_text = 'svn log %s -v --xml -r {%s}:{%s} > %s' % \
                            (
                                svn_src_path,
                                half_year_date,
                                today_date,
                                log_name
                            )

        return _svn_log_cmd_text

    def _get_stat_svn_command_text(self, product_info_dict):
        log_name = product_info_dict['log_full_path']
        svn_src_path = product_info_dict['src']
        report_path = product_info_dict['report']
        _stat_svn_cmd_text = \
            "java -jar %s %s %s -output-dir \"%s\" -charset utf-8 -disable-twitter-button -include " \
            "\"**/*.java:**/*.php:**/*.cs:**/*.js:**/*.aspx:**/*.ashx\"" % \
            (ConfigDict.get_stat_svn_path(), log_name, svn_src_path, report_path)

        return _stat_svn_cmd_text

    def get_cmd_flow_list(self):
        product_info_dict_list = self._product_info.get_product_path_dict_list()

        for i in range(len(product_info_dict_list)):
            product_info_dict = product_info_dict_list[i]

            _sync_src_cmd_text = self._get_sync_code_command_text(product_info_dict)
            _svn_log_cmd_text = self._get_svn_log_command_text(product_info_dict)
            _svn_report_cmd_text = self._get_stat_svn_command_text(product_info_dict)

            self._cmd_flow_list.append(_sync_src_cmd_text)
            self._cmd_flow_list.append(_svn_log_cmd_text)
            self._cmd_flow_list.append(_svn_report_cmd_text)

        return self._cmd_flow_list

if __name__ == '__main__':
    _ini_parser = ProductIniParser()
    _product_info_list = _ini_parser.get_product_info_list()
    _cmd_warp_list = []

    for index in range(len(_product_info_list)):
        cmd_warp = CommandWarp(_product_info_list[index])

        print cmd_warp.get_cmd_flow_list()
        _cmd_warp_list.append(cmd_warp)
