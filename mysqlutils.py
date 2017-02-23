# coding:utf-8

import MySQLdb


class MySqlDBUtil:
    def __init__(self, host, username, password, db_name, port=3306):
        self._host_ip = host
        self._username = username
        self._password = password
        self._db_name = db_name
        self._host_port = port

        self._db = None
        self._cursor = None

    def connect(self):
        self._db = MySQLdb.connect(self._host_ip, self._username, self._password, self._db_name,
                                   self._host_port, charset='utf8')
        self._cursor = self._db.cursor()

    def close(self):
        if self._db is not None:
            self._db.close()

    def query(self, query_cmd_text):
        self._cursor.execute(query_cmd_text)

        results = self._cursor.fetchall()
        return results

    def query_one_with_param_list(self, query_cmd_text, params_list):
        self._cursor.execute(query_cmd_text, params_list)
        result = self._cursor.fetchone()

        return result

    def query_with_param_list(self, query_cmd_text, params_list):
        self._cursor.execute(query_cmd_text, params_list)

        results = self._cursor.fetchall()
        return results

    def execute(self, sql_cmd_text):
        try:
            self._cursor.execute(sql_cmd_text)
            self._db.commit()
        except MySQLdb.Error, e:
            print "MySql Error: %s" % str(e)
            self._db.rollback()

    def execute_with_param_list(self, sql_cmd_text, params_list):
        try:
            self._cursor.execute(sql_cmd_text, params_list)
            self._db.commit()
        except MySQLdb.Error, e:
            print "MySql Error: %s" % str(e)
            self._db.rollback()

    def execute_with_param_list_and_return_value(self, sql_cmd_text, params_list):
        insert_id = 0

        try:
            self._cursor.execute(sql_cmd_text, params_list)
            insert_id = self._db.insert_id()
            self._db.commit()
        except MySQLdb.Error, e:
            print "MySql Error: %s" % str(e)
            self._db.rollback()

        return insert_id

    def get_insert_id(self):
        return self._db.insert_id()
