from constants.error_messages import DB_CONNECTION_ERROR, SQL_ERROR
from utils import Helpers
import sys, logging

logger = logging.getLogger("main")


class SQLHandler:
    def __init__(self, connection):
        try:
            self.connection = connection
            self.cur = connection.cursor()
        except Exception as e:
            msg = Helpers.format_error_message(DB_CONNECTION_ERROR, [str(e)])
            logger.error(msg)
            raise ConnectionError(msg)

    def close(self):
        if self.cur:
            self.cur.close()
        self.connection = None

    def exec_query(self, sql, params=None):
        try:
            self.connection.begin()
            if params:
                self.cur.execute(sql, params)
            else:
                self.cur.execute(sql)
            self.connection.commit()
        except Exception as e:
            msg = Helpers.format_error_message(SQL_ERROR, [str(e)])
            logger.error(f"SQL Error: {msg} | Query: {sql} | Params: {params}")
            raise Exception(msg)

    def fetchall(self, sql, params=None):
        try:
            if params:
                self.cur.execute(sql, params)
            else:
                self.cur.execute(sql)
            return self.cur.fetchall()
        except Exception as e:
            msg = Helpers.format_error_message(SQL_ERROR, [str(e)])
            logger.error(f"SQL Error: {msg} | Query: {sql} | Params: {params}")
            raise Exception(msg)

    def fetchone(self, sql, params=None):
        try:
            if params:
                self.cur.execute(sql, params)
            else:
                self.cur.execute(sql)
            return self.cur.fetchone()
        except Exception as e:
            msg = Helpers.format_error_message(SQL_ERROR, [str(e)])
            logger.error(f"SQL Error: {msg} | Query: {sql} | Params: {params}")
            raise Exception(msg)
