from utils import SQLHandler
from config.globals import get_db_connection


class ConfigRepository:
    @staticmethod
    def get_config_by_field(fieldname: str, config_table_number: int = 1) -> str:
        sql_handler = SQLHandler(get_db_connection())

        if config_table_number == 1:
            table_name = "CONFIGURACOES"
        else:
            table_name = "CONFIGURACOES2"

        result = sql_handler.fetchone(
            f"""
            SELECT {fieldname}
            FROM {table_name}
            """
        )

        return result[0]
