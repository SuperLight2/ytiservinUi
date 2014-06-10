__author__ = 'gumerovif'

import MySQLdb


class DBRunner(object):
    def __init__(self, ):
        self.db = MySQLdb.connect(host="127.0.0.1", user="root", passwd="NEWPASSWORD", db="main", use_unicode=True)
        self.cursor = None
        self.success = None
        self.error = None

    def __del__(self):
        if self.db:
            self.db.close()

    def run(self, query):
        try:
            self.cursor = self.db.cursor(MySQLdb.cursors.DictCursor)
            self.cursor.execute(query)
            self.db.commit()
        except MySQLdb.Error, e:
            if self.db:
                self.db.rollback()
            self.success = False
            self.error = "Error %d: %s" % (e.args[0], e.args[1])
            raise BaseException(self.error)
        self.success = True
        return self

    def fetchone(self):
        return self.cursor.fetchone()

    def get_results_count(self):
        return self.cursor.rowcount

    def get_only_result(self):
        if self.get_results_count() != 1:
            raise BaseException("Waiting exactly one row")
        return self.fetchone()

    def get_only_or_none_result(self):
        if self.get_results_count() > 1:
            raise BaseException("Waiting exactly one or zero rows")
        if self.get_results_count() == 0:
            return None
        return self.get_only_result()

    def was_success(self):
        return self.success

    def get_error_message(self):
        return self.error