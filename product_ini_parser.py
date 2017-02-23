# coding:utf-8

import os
from ConfigParser import ConfigParser
from productinfo import ProductInfo


class ProductIniParser:
    def __init__(self):
        self.config_parser = ConfigParser()
        self.ini_file_path = os.path.join(os.path.dirname(
            os.path.abspath(__file__)), 'product_svn_relationship.ini')
        self.config_parser.read(self.ini_file_path)

    def get_product_info_list(self):
        product_section_list = self.config_parser.sections()
        product_info_list = []

        for product_section in product_section_list:
            product_title = self.config_parser.get(product_section, 'title')
            product_svn_url = self.config_parser.get(product_section, 'svn_url')

            product_info = ProductInfo(product_title, product_svn_url)
            product_info_list.append(product_info)

        return product_info_list
