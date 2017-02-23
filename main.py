# coding:utf-8

from svnoperatorhelper import SvnOperatorHelper
from configdictionary import ConfigDict
from commandexecutor import CommandExecutor
from Queue import Queue
from productinfo import ProductInfo
from ioutils import IOUtils

from htmlsummaryparser import HtmlSummaryParser
from developersummaryparser import DeveloperSummaryParser
from filesizeandfilecountinfoparser import FileSizeAndFileCountInfoParser
from dirsizeparser import DirSizeParser

from reportinfo import ReportInfo
from projectsvninfo import ProjectSvnInfo

from svninfodbhelper import SvnInfoDBHelper

import ConfigParser


class Main:
    def __init__(self):
        self.cmd_task_queue = Queue()
        self.product_info_list = []

        self._get_product_info_list()

    def _get_product_info_list(self):
        config_parser = ConfigParser.ConfigParser()
        config_parser.read(IOUtils.get_full_config_file_path('product_svn_relationship.ini'))

        product_section_list = config_parser.sections()

        for product_section in product_section_list:
            product_title = config_parser.get(product_section, 'title')
            product_svn_url = config_parser.get(product_section, 'svn_url')
            product_info = ProductInfo(product_title, product_svn_url)

            self.product_info_list.append(product_info)

    def run_command(self):
        svn_helper = SvnOperatorHelper(self.product_info_list)
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

    def _get_report_summary_info(self, file_name):
        html_summary_parser = HtmlSummaryParser(file_name)
        summary_info = html_summary_parser.get_svn_summary_info()

        return summary_info

    def _get_dev_summary_info(self, file_name):
        dev_summary_parser = DeveloperSummaryParser(file_name)
        dev_summary_info = dev_summary_parser.get_svn_developer_info()

        return dev_summary_info

    def _get_file_summary_info(self, file_name):
        file_summary_parser = FileSizeAndFileCountInfoParser(file_name)
        file_summary_info = file_summary_parser.get_svn_file_info()

        return file_summary_info

    def _get_dir_summary_info(self, file_name):
        dir_summary_parser = DirSizeParser(file_name)
        dir_summary_info = dir_summary_parser.get_dir_stat_info()

        return dir_summary_info

    def analyze_report(self):
        summary_file_name = 'index.html'
        dev_summary_file_name = 'developers.html'
        file_summary_file_name = 'file_sizes.html'
        dir_summary_file_name = 'dir_sizes.html'

        report_info_list = []

        for i in range(len(self.product_info_list)):
            product_info = self.product_info_list[i]
            product_info_dict_list = product_info.get_product_path_dict_list()
            report_info = ReportInfo(product_info.get_product_title())

            for j in range(len(product_info_dict_list)):

                product_info_dict = product_info_dict_list[j]
                project_name = product_info_dict['name']
                report_path = product_info_dict['report']
                svn_url = product_info_dict['url']

                if len(IOUtils.list_dirs(report_path)) > 0:
                    summary_file_path = report_path + summary_file_name
                    dev_summary_file_path = report_path + dev_summary_file_name
                    file_summary_file_path = report_path + file_summary_file_name
                    dir_summary_file_path = report_path + dir_summary_file_name

                    report_summary_info = self._get_report_summary_info(summary_file_path)
                    dev_summary_info = self._get_dev_summary_info(dev_summary_file_path)
                    file_summary_info = self._get_file_summary_info(file_summary_file_path)
                    dir_summary_info = self._get_dir_summary_info(dir_summary_file_path)

                    project_info = ProjectSvnInfo(project_name, svn_url, report_summary_info,
                                                  dev_summary_info, file_summary_info,
                                                  dir_summary_info)
                    report_info.add_project_info(project_info)

            report_info_list.append(report_info)

        return report_info_list


if __name__ == '__main__':
    main = Main()
    # main.run_command()
    report_info_list = main.analyze_report()
    svn_info_db_helper = None

    for i in range(len(report_info_list)):
        report_info = report_info_list[i]
        project_info_list = report_info.get_project_info_list()

        for j in range(len(project_info_list)):
            project_info_obj = project_info_list[j]
            project_name = project_info_obj.get_project_name()
            project_svn_url = project_info_obj.get_svn_url()
            svn_summary_info_obj = project_info_obj.get_svn_summary_info()
            svn_dev_info_obj = project_info_obj.get_svn_dev_info()
            svn_file_info_obj = project_info_obj.get_svn_file_info()
            svn_dir_info_obj = project_info_obj.get_svn_dir_info()

            print '========== Start =========='
            print 'product name: %s' % report_info.get_product_name()
            svn_info_db_helper = SvnInfoDBHelper(svn_summary_info_obj.get_generate_time())
            svn_info_db_helper.open()

            project_id = svn_info_db_helper.insert_svn_project_info(project_name, project_svn_url,
                                                                    report_info.get_product_name())
            svn_info_db_helper.insert_svn_project_summary_info(project_id, svn_summary_info_obj)
            svn_info_db_helper.insert_svn_project_dev_summary_info(project_id, svn_dev_info_obj)
            svn_info_db_helper.insert_svn_project_file_summary_info(project_id, svn_file_info_obj)
            svn_info_db_helper.insert_svn_project_dir_summary_info(project_id, svn_dir_info_obj)

            svn_info_db_helper.close()
            print '========== Project info =========='
            print 'project name: %s' % project_name
            print 'project url: %s' % project_svn_url
            print '========== Svn summary info =========='
            print 'project name: %s' % svn_summary_info_obj.get_product_title()
            print 'report generate time: %s' % svn_summary_info_obj.get_generate_time()
            print 'head reversion: %s' % svn_summary_info_obj.get_head_revision()
            print 'report period start time: %s' % svn_summary_info_obj.get_report_period_start_time()
            print 'report period end time: %s' % svn_summary_info_obj.get_report_period_end_time()
            print 'total files: %s' % svn_summary_info_obj.get_total_files()
            print 'line of codes: %s' % svn_summary_info_obj.get_total_line_of_codes()
            print 'developers: %s' % svn_summary_info_obj.get_developers()
            print 'top 10 dev: %s' % svn_summary_info_obj.get_top_10_dev_dict()
            print '========== Svn dev summary info =========='
            print 'total developers: %s' % svn_dev_info_obj.get_total_developers()
            print 'development summary info: %s' % svn_dev_info_obj.get_dev_summary_info_dict_list()
            print 'development last 12 months info: %s' % svn_dev_info_obj.get_dev_last_12_months_info_dict_list()
            print '========== Svn file summary info=========='
            print 'total files: %s' % svn_file_info_obj.get_total_files()
            print 'avg file size: %s' % svn_file_info_obj.get_average_file_size()
            print 'avg revision per file: %s' % svn_file_info_obj.get_average_revision_per_file()
            print 'file types: %s' % svn_file_info_obj.get_file_types_summary_dict_list()
            print 'large files: %s' % svn_file_info_obj.get_largest_files_detail_dict_list()
            print 'files with most revisions: %s' % svn_file_info_obj.get_files_with_most_revisions_dict_list()
            print '========== Svn dir summary info =========='
            print 'total dirs: %s' % svn_dir_info_obj.get_total_dirs()
            print 'dir statistics: %s' % svn_dir_info_obj.get_dir_statistics_dict_list()
            print '========== End =========='

        print
        print
        print
        print
        print
