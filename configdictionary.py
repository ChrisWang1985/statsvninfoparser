from multiprocessing import cpu_count


class ConfigDict:
    def __init__(self):
        pass

    @staticmethod
    def get_source_code_base_path():
        return u'E:\\product_code\\'

    @staticmethod
    def get_svn_log_path():
        return u"E:\\svn_log\\"

    @staticmethod
    def get_svn_report_path():
        return u"E:\\svn_report\\"

    @staticmethod
    def get_best_thread_number():
        #return cpu_count() * 2
        return 1

    @staticmethod
    def get_stat_svn_path():
        return u"E:\\project\\opensource\\codecount\\statsvn\\statsvn-0.7.0\\statsvn.jar"

    @staticmethod
    def get_db_host():
        return u'172.18.21.17'

    @staticmethod
    def get_db_username():
        return u'root'

    @staticmethod
    def get_db_password():
        return u'jkzl123456'

    @staticmethod
    def get_db_name():
        return u'dailybuild'

    @staticmethod
    def get_db_port():
        return 18089


if __name__ == '__main__':
    print ConfigDict.get_source_code_base_path()
