# coding:utf-8


class SvnSummaryInfo:
    def __init__(self):
        self._product_title = ''
        self._generate_time = ''
        self._head_revision = ''
        self._report_period_start_time = ''
        self._report_period_end_time = ''
        self._total_files = ''
        self._total_line_of_codes = ''
        self._developers = ''
        self._top_10_dev_dict = []

    def get_product_title(self):
        return self._product_title

    def set_product_title(self, title):
        self._product_title = title

    def get_generate_time(self):
        return self._generate_time

    def set_generate_time(self, generate_time):
        self._generate_time = generate_time

    def get_head_revision(self):
        return self._head_revision

    def set_head_revision(self, head_revision):
        self._head_revision = head_revision

    def get_report_period_start_time(self):
        return self._report_period_start_time

    def set_report_period_start_time(self, start_time):
        self._report_period_start_time = start_time

    def get_report_period_end_time(self):
        return self._report_period_end_time

    def set_report_period_end_time(self, end_time):
        self._report_period_end_time = end_time

    def get_total_files(self):
        return self._total_files

    def set_total_files(self, total_files):
        self._total_files = total_files

    def get_total_line_of_codes(self):
        return self._total_line_of_codes

    def set_total_line_of_codes(self, total_loc):
        self._total_line_of_codes = total_loc

    def get_developers(self):
        return self._developers

    def set_developers(self, developers):
        self._developers = developers

    def get_top_10_dev_dict(self):
        return self._top_10_dev_dict

    def set_top_10_dev_dict(self, top_10_dict):
        self._top_10_dev_dict = top_10_dict
