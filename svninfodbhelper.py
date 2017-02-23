# coding:utf-8

from mysqlutils import MySqlDBUtil
from configdictionary import ConfigDict
from developersummaryparser import DeveloperSummaryParser


class SvnInfoDBHelper:
    def __init__(self, report_gen_time):
        self._db_host = ConfigDict.get_db_host()
        self._db_username = ConfigDict.get_db_username()
        self._db_password = ConfigDict.get_db_password()
        self._db_name = ConfigDict.get_db_name()
        self._db_port = ConfigDict.get_db_port()

        self._mysql_util = MySqlDBUtil(self._db_host, self._db_username, self._db_password,
                                       self._db_name, self._db_port)
        self._insert_time = report_gen_time

    def open(self):
        self._mysql_util.connect()

    def close(self):
        self._mysql_util.close()

    def query_svn_project_info_by_project_name(self, project_name):
        sql_cmd_text = "select * from svn_project_info WHERE projectName = %s"

        result = self._mysql_util.query_one_with_param_list(sql_cmd_text, (project_name, ))
        return result

    def insert_svn_project_info(self, project_name, svn_url, product_name):
        result = self.query_svn_project_info_by_project_name(project_name)

        if result is not None:
            return result[0]

        sql_cmd_text = "insert into svn_project_info(projectName, svnUrl, productName, insertTime) " \
                       "values(%s, %s, %s, %s)"
        return self._mysql_util.execute_with_param_list_and_return_value(
            sql_cmd_text, (project_name, svn_url, product_name, self._insert_time))

    def insert_svn_project_summary_info(self, project_id, svn_summary_info_obj):
        sql_cmd_text = "insert into svn_project_summary_info(projectId, projectSvnName, reportGenTime, " \
                       "headRevision, reportPeriodStartTime, reportPeriodEndTime, totalFiles, " \
                       "lineOfCodes, insertTime) values(%s, %s, %s, %s, %s, %s, %s, %s, %s)" \

        return self._mysql_util.execute_with_param_list_and_return_value(
            sql_cmd_text, (
                project_id,
                svn_summary_info_obj.get_product_title(),
                svn_summary_info_obj.get_generate_time(),
                svn_summary_info_obj.get_head_revision(),
                svn_summary_info_obj.get_report_period_start_time(),
                svn_summary_info_obj.get_report_period_end_time(),
                svn_summary_info_obj.get_total_files(),
                svn_summary_info_obj.get_total_line_of_codes(),
                self._insert_time
            )
        )

    def insert_svn_project_dev_summary_info(self, project_id, svn_dev_info_obj):
        sql_cmd_text = "insert into svn_project_dev_summary_info(projectId, authorId, author, loc, " \
                       "changes, lpc, monthlyCodeInfoId, insertTime) VALUES (%s, %s, %s, %s, " \
                       "%s, %s, %s, %s)"

        dev_summary_info_list = svn_dev_info_obj.get_dev_summary_info_dict_list()

        for i in range(len(dev_summary_info_list)):
            author_id = dev_summary_info_list[i].get("author_id")
            author = dev_summary_info_list[i].get("author")
            loc = dev_summary_info_list[i].get("loc")
            changes = dev_summary_info_list[i].get("changes")
            lpc = dev_summary_info_list[i].get("lpc")
            svn_dev_monthly_code_dict = svn_dev_info_obj.get_dev_last_12_months_info_by_author(author)
            monthly_code_info_id = self.insert_svn_project_dev_monthly_code_info(project_id, svn_dev_monthly_code_dict)

            self._mysql_util.execute_with_param_list(sql_cmd_text, (
                project_id, author_id, author, loc, changes, lpc, monthly_code_info_id,
                self._insert_time
            ))

    def insert_svn_project_dev_monthly_code_info(self, project_id, svn_dev_monthly_code_dict):
        monthly_dict_key_list = DeveloperSummaryParser.generate_last_m_months_str_list(13)

        author = svn_dev_monthly_code_dict.get('author')
        last_1_month_code = svn_dev_monthly_code_dict.get(monthly_dict_key_list[0])
        last_2_month_code = svn_dev_monthly_code_dict.get(monthly_dict_key_list[1])
        last_3_month_code = svn_dev_monthly_code_dict.get(monthly_dict_key_list[2])
        last_4_month_code = svn_dev_monthly_code_dict.get(monthly_dict_key_list[3])
        last_5_month_code = svn_dev_monthly_code_dict.get(monthly_dict_key_list[4])
        last_6_month_code = svn_dev_monthly_code_dict.get(monthly_dict_key_list[5])
        last_7_month_code = svn_dev_monthly_code_dict.get(monthly_dict_key_list[6])
        last_8_month_code = svn_dev_monthly_code_dict.get(monthly_dict_key_list[7])
        last_9_month_code = svn_dev_monthly_code_dict.get(monthly_dict_key_list[8])
        last_10_month_code = svn_dev_monthly_code_dict.get(monthly_dict_key_list[9])
        last_11_month_code = svn_dev_monthly_code_dict.get(monthly_dict_key_list[10])
        last_12_month_code = svn_dev_monthly_code_dict.get(monthly_dict_key_list[11])
        previous_years_code = svn_dev_monthly_code_dict.get(monthly_dict_key_list[12])

        sql_cmd_text = "insert into svn_project_dev_monthly_code_info(projectId, author, last1MonthCode," \
                       "last2MonthCode, last3MonthCode, last4MonthCode, last5MonthCode, last6MonthCode, " \
                       "last7MonthCode, last8MonthCode, last9MonthCode, last10MonthCode, last11MonthCode, " \
                       "last12MonthCode, previousYearsCode, insertTime) values(%s, %s, %s, %s, " \
                       "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

        return self._mysql_util.execute_with_param_list_and_return_value(sql_cmd_text, (
            project_id, author, last_1_month_code, last_2_month_code, last_3_month_code, last_4_month_code,
            last_5_month_code, last_6_month_code, last_7_month_code, last_8_month_code, last_9_month_code,
            last_10_month_code, last_11_month_code, last_12_month_code, previous_years_code,
            self._insert_time
        ))

    def insert_svn_project_file_summary_info(self, project_id, svn_file_info_obj):
        sql_cmd_text = "insert into svn_project_file_summary_info(projectId, totalFiles, " \
                       "avgFileSize, avgRevisionPerFile, insertTime) values(%s, %s, %s, %s, %s)"

        total_files = svn_file_info_obj.get_total_files()
        avg_file_size = svn_file_info_obj.get_average_file_size()
        avg_revision_per_file = svn_file_info_obj.get_average_revision_per_file()

        self._mysql_util.execute_with_param_list(sql_cmd_text, (
            project_id, total_files, avg_file_size, avg_revision_per_file, self._insert_time
        ))

        file_types_dict_list = svn_file_info_obj.get_file_types_summary_dict_list()
        large_files_dict_list = svn_file_info_obj.get_largest_files_detail_dict_list()
        file_with_most_revision_dict_list = svn_file_info_obj.get_files_with_most_revisions_dict_list()

        self.insert_svn_project_file_types_info(project_id, file_types_dict_list)
        self.insert_svn_project_large_file_info(project_id, large_files_dict_list)
        self.insert_svn_project_file_with_most_revisions_info(project_id, file_with_most_revision_dict_list)

    def insert_svn_project_file_types_info(self, project_id, file_types_dict_list):
        sql_cmd_text = "insert into svn_project_file_types_info(projectId, files, loc, type, " \
                       "locPerFile, insertTime) values(%s, %s, %s, %s, %s, %s)"

        for i in range(len(file_types_dict_list)):
            files = file_types_dict_list[i].get('files')
            loc = file_types_dict_list[i].get('loc')
            type_info = file_types_dict_list[i].get('type')
            loc_per_file = file_types_dict_list[i].get('loc_per_file')

            self._mysql_util.execute_with_param_list(sql_cmd_text, (
                project_id, files, loc, type_info, loc_per_file, self._insert_time
            ))

    def insert_svn_project_large_file_info(self, project_id, large_file_dict_list):
        sql_cmd_text = "insert into svn_project_large_file_info(projectId, loc, file, insertTime)" \
                       " values(%s, %s, %s, %s)"

        for i in range(len(large_file_dict_list)):
            loc = large_file_dict_list[i].get('loc')
            file_info = large_file_dict_list[i].get('file')

            self._mysql_util.execute_with_param_list(sql_cmd_text, (
                project_id, loc, file_info, self._insert_time
            ))

    def insert_svn_project_file_with_most_revisions_info(self, project_id, file_with_most_revision_dict_list):
        sql_cmd_text = "insert into svn_project_file_with_most_revisions_info(projectId, file, " \
                       "revisions, insertTime) values(%s, %s, %s, %s)"

        for i in range(len(file_with_most_revision_dict_list)):
            file_info = file_with_most_revision_dict_list[i].get('file')
            revisions = file_with_most_revision_dict_list[i].get('revisions')

            self._mysql_util.execute_with_param_list(sql_cmd_text, (
                project_id, file_info, revisions, self._insert_time
            ))

    def insert_svn_project_dir_summary_info(self, project_id, svn_dir_info_obj):
        sql_cmd_text = "insert into svn_project_dir_summary_info(projectId, loc, `change`, dir, " \
                       "insertTime) values(%s, %s, %s, %s, %s)"

        dir_statistics_dict_list = svn_dir_info_obj.get_dir_statistics_dict_list()

        for i in range(len(dir_statistics_dict_list)):
            loc = dir_statistics_dict_list[i].get('loc')
            change = dir_statistics_dict_list[i].get('change')
            dir_info = dir_statistics_dict_list[i].get('dir')

            self._mysql_util.execute_with_param_list(sql_cmd_text, (
                project_id, loc, change, dir_info, self._insert_time
            ))
