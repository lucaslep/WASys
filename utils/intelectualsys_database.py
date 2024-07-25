import firebirdsql, sys, logging
from utils import IniFile, Helpers
from constants.error_messages import DB_CONNECTION_ERROR

logger = logging.getLogger("main")


class IntelectualSysDB:
    def __init__(self, database_path=None):
        try:
            self.connection = None

            self.path = self.get_path(database_path)
            self.host = self.get_host(database_path)
            self.port = self.get_port(database_path)

        except Exception as e:
            msg = Helpers.format_error_message(DB_CONNECTION_ERROR, [str(e)])
            logger.error(msg)
            sys.exit(msg)

    def get_path(self, database_path):
        start_pos = database_path.find(":") + 1
        end_pos = len(database_path)
        return database_path[start_pos:end_pos]

    def get_host(self, database_path):
        start_pos = 0
        end_pos = database_path.find(":")
        host = database_path[start_pos:end_pos]

        if "/" in host:
            start_pos = 0
            end_pos = host.find("/")
            host = host[start_pos:end_pos]

        return host

    def get_port(self, database_path):
        port = None

        start_pos = 0
        end_pos = database_path.find(":")
        host = database_path[start_pos:end_pos]

        if "/" in host:
            start_pos = host.find("/") + 1
            end_pos = len(host)
            port = int(host[start_pos:end_pos])

        # Retorna a porta padrão do firebird caso não tenha nenhuma no ini.
        return port or 3050

    def connect(self):
        self.connection = None
        try:
            self.connection = firebirdsql.connect(
                user="SYSDBA",
                password="masterkey",
                database=rf"{self.path}",
                host=rf"{self.host}",
                port=rf"{self.port}",
            )

            return self.connection

        except Exception as e:
            msg = Helpers.format_error_message(DB_CONNECTION_ERROR, [str(e)])
            logger.error(msg)
            sys.exit(msg)

    def disconnect(self):
        if self.connection is not None:
            self.connection.close()
