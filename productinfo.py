# coding:utf-8

import os
import ConfigParser
from configdictionary import ConfigDict
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class ProductInfo:
    def __init__(self, title, svn_url):
        self.product_title = title
        self.product_svn_url_list = [svn_url.decode('utf-8') for svn_url in svn_url.split(';')]
        self.product_path_dict_list = []
        self._base_src_path = ConfigDict.get_source_code_base_path() + self.product_title + os.path.sep
        self._base_svn_log_path = ConfigDict.get_svn_log_path() + self.product_title + os.path.sep
        self._base_svn_report_path = ConfigDict.get_svn_report_path() + self.product_title + os.path.sep

        self._parse_info()

    def _parse_info(self):
        for i in range(len(self.product_svn_url_list)):
            svn_url = self.product_svn_url_list[i]
            product_svn_name = svn_url[svn_url.rfind('/') + 1:]
            product_src_path = self._base_src_path + product_svn_name + os.path.sep
            product_log_path = self._base_svn_log_path + product_svn_name + os.path.sep
            product_report_path = self._base_svn_report_path + product_svn_name + os.path.sep

            path_info_dict = {
                'name': product_svn_name,
                'src': product_src_path,
                'log': product_log_path,
                'report': product_report_path,
                'url': svn_url,
                'product': self.product_title,
                'base_src': self._base_src_path,
                'base_log': self._base_svn_log_path,
                'base_report': self._base_svn_log_path,
                'log_full_path': product_log_path + product_svn_name + '.log',
            }

            self.product_path_dict_list.append(path_info_dict)

    def get_product_path_dict_list(self):
        return self.product_path_dict_list

    def get_product_title(self):
        return self.product_title

    def get_product_svn_url_list(self):
        return self.product_svn_url_list

    def get_product_base_svn_src_path(self):
        return self._base_src_path

    def get_product_base_svn_log_path(self):
        return self._base_svn_log_path

    def get_product_base_svn_report_path(self):
        return self._base_svn_report_path


if __name__ == '__main__':
    config_parser = ConfigParser.ConfigParser()

    product_svn_relationship_ini_path = os.path.join(os.path.dirname(
        os.path.abspath(__file__)), 'product_svn_relationship.ini')
    config_parser.read(product_svn_relationship_ini_path)

    product_section_list = config_parser.sections()

    product_info_list = []

    for product_section in product_section_list:
        product_title = config_parser.get(product_section, 'title')
        product_svn_url = config_parser.get(product_section, 'svn_url')
        product_info = ProductInfo(product_title, product_svn_url)

        product_info_list.append(product_info)

    for index in range(len(product_info_list)):
        path_dict_list = product_info_list[index].get_product_path_dict_list()

        for j in range(len(path_dict_list)):
            path_dict = path_dict_list[j]
            print 'Product:%s' % path_dict['product']
            print 'Url:%s' % path_dict['url']
            print 'Name:%s' % path_dict['name']
            print 'Base_Src:%s' % path_dict['base_src']
            print 'Src:%s' % path_dict['src']
            print 'Base_Log:%s' % path_dict['base_log']
            print 'Log:%s' % path_dict['log']
            print 'Base_Report:%s' % path_dict['base_report']
            print 'Report:%s' % path_dict['report']

            print '============================================'
