from constants.error_messages import DB_CONNECTION_ERROR, SQL_ERROR
from utils import Helpers
from utils import exit_with_log


class SQLHandler:
    def __init__(self, connection):
        try:
            self.connection = connection
            self.cur = connection.cursor()

        except Exception as e:
            exit_with_log(Helpers.format_error_message(DB_CONNECTION_ERROR, [str(e)]))

    def close(self):
        self.cur.close()
        self.connection = None

    def exec_query(self, sql):
        try:
            self.connection.begin()
            self.cur.execute(sql)
            self.connection.commit()

        except Exception as e:
            exit_with_log(Helpers.format_error_message(SQL_ERROR, [str(e)]))

    def fetchall(self, sql):
        try:
            self.cur.execute(sql)
            return self.cur.fetchall()

        except Exception as e:
            exit_with_log(Helpers.format_error_message(SQL_ERROR, [str(e)]))

    def fetchone(self, sql):
        try:
            self.cur.execute(sql)
            return self.cur.fetchone()

        except Exception as e:
            exit_with_log(Helpers.format_error_message(SQL_ERROR, [str(e)]))
