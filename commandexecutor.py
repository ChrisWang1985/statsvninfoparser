# coding:utf-8

from threading import Thread
from svnoperatorhelper import SvnOperatorHelper
from configdictionary import ConfigDict
from commandutils import CommandUtils
from productinfo import ProductInfo

import time
import ConfigParser
import os


class CommandExecutor(Thread):
    def __init__(self, thread_name, queue):
        Thread.__init__(self, name=thread_name)
        self.thread_name = thread_name
        self.task_queue = queue

    def run(self):
        cmd_text_flow_list = self.task_queue.get(1).get_cmd_flow_list()
        for cmd_index in range(len(cmd_text_flow_list)):
            CommandUtils.run_command(cmd_text_flow_list[cmd_index])
            time.sleep(3)


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

    svn_helper = SvnOperatorHelper(product_info_list)
    svn_helper.create_source_dir()
    cmd_queue = svn_helper.fill_cmd_text_to_queue()

    while cmd_queue.qsize() > 0:
        executor_list = []

        for i in range(ConfigDict.get_best_thread_number()):
            if cmd_queue.qsize() > 0:
                cmd_executor = CommandExecutor('cmd_executor_' + str(i), cmd_queue)
                executor_list.append(cmd_executor)
                cmd_executor.start()
            else:
                break

        for j in range(len(executor_list)):
            executor_list[j].join()

    print 'done!'
