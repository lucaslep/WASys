import firebirdsql, sys, logging
from utils import IniFile, Helpers
from constants.error_messages import DB_CONNECTION_ERROR

logger = logging.getLogger("main")


class IntelectualSysDB:
    def __init__(self):
        try:
            self.connection = None
            self.full_path = self.get_full_path()
            self.path = self.get_path(self.full_path)
            self.host = self.get_host(self.full_path)
            self.port = self.get_port(self.full_path)

        except Exception as e:
            msg = Helpers.format_error_message(DB_CONNECTION_ERROR, [str(e)])
            logger.error(msg)
            sys.exit(msg)

    def get_path(self, full_path):
        start_pos = full_path.find(":") + 1
        end_pos = len(full_path)
        return full_path[start_pos:end_pos]

    def get_host(self, full_path):
        start_pos = 0
        end_pos = full_path.find(":")
        host = full_path[start_pos:end_pos]

        if "/" in host:
            start_pos = 0
            end_pos = host.find("/")
            host = host[start_pos:end_pos]

        return host

    def get_port(self, full_path):
        port = None

        start_pos = 0
        end_pos = full_path.find(":")
        host = full_path[start_pos:end_pos]

        if "/" in host:
            start_pos = host.find("/") + 1
            end_pos = len(host)
            port = int(host[start_pos:end_pos])

        # Retorna a porta padrão do firebird caso não tenha nenhuma no ini.
        return port or 3050

    def get_full_path(self):
        ini = IniFile()
        return Helpers.decrypt(ini.get_value("DBCnxSystem"))

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
