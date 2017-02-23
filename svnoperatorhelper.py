# coding:utf-8

from ioutils import IOUtils
from commandwarp import CommandWarp
from Queue import Queue


class SvnOperatorHelper:
    def __init__(self, product_info_list):
        self.product_info_list = product_info_list
        self.cmd_task_queue = Queue()

    def create_source_dir(self):
        for i in range(len(self.product_info_list)):
            product_info_dict_list = self.product_info_list[i].get_product_path_dict_list()

            for j in range(len(product_info_dict_list)):
                product_info_dict = product_info_dict_list[j]

                src_dir = product_info_dict['src']
                log_dir = product_info_dict['log']
                report_dir = product_info_dict['report']

                if IOUtils.is_exists_dir(src_dir) is False:
                    IOUtils.make_dirs(src_dir)

                if IOUtils.is_exists_dir(log_dir) is False:
                    IOUtils.make_dirs(log_dir)

                if IOUtils.is_exists_dir(report_dir) is False:
                    IOUtils.make_dirs(report_dir)

    def _parse_svn_sync_cmd_text(self, svn_url_list, src_dir_list):
        cmd_text = ''

        for j in range(len(svn_url_list)):
            svn_url = svn_url_list[j]
            src_dir = src_dir_list[j]

            if len(IOUtils.list_dirs(src_dir)) > 0:
                src_dir = src_dir + '/' + svn_url[svn_url.rfind('/') + 1:]
                cmd_text = "svn up %s --username xuwenlong --password xuwenlong1" % src_dir
            else:
                cmd_text = "svn co %s %s --username xuwenlong --password xuwenlong1" % \
                           (svn_url, src_dir)

        return cmd_text

    # def sync_source_from_server(self):
    #     for i in range(len(self.product_info_list)):
    #         product_info = self.product_info_list[i]
    #         svn_url_list = product_info.get_svn_url_list()
    #         src_dir_list = product_info.get_source_code_path_list()
    #
    #         CommandUtils.run_command(self._parse_svn_sync_cmd_text(svn_url_list, src_dir_list))

    def fill_cmd_text_to_queue(self):
        for i in range(len(self.product_info_list)):
            product_info = self.product_info_list[i]
            command_warpper = CommandWarp(product_info)

            self.cmd_task_queue.put(command_warpper)

        return self.cmd_task_queue


if __name__ == '__main__':
    svn_helper = SvnOperatorHelper()
    svn_helper.create_source_dir()
    svn_helper.fill_cmd_text_to_queue()
