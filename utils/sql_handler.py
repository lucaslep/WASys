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
            sys.exit(msg)

    def close(self):
        self.cur.close()
        self.connection = None

    def exec_query(self, sql):
        try:
            self.connection.begin()
            self.cur.execute(sql)
            self.connection.commit()

        except Exception as e:
            msg = Helpers.format_error_message(SQL_ERROR, [str(e)])
            logger.error(msg)
            sys.exit(msg)

    def fetchall(self, sql):
        try:
            self.cur.execute(sql)
            return self.cur.fetchall()

        except Exception as e:
            msg = Helpers.format_error_message(SQL_ERROR, [str(e)])
            logger.error(msg)
            sys.exit(msg)

    def fetchone(self, sql):
        try:
            self.cur.execute(sql)
            return self.cur.fetchone()

        except Exception as e:
            msg = Helpers.format_error_message(SQL_ERROR, [str(e)])
            logger.error(msg)
            sys.exit(msg)
