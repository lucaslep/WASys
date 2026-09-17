from config.globals import get_db_connection
from utils import SQLHandler
from utils import WhatsappMessage


class WhatsappRepository:
    @staticmethod
    def get_unsent_messages() -> list[WhatsappMessage]:
        unsent_messages = []
        try:
            sql_handler = SQLHandler(get_db_connection())
            result = sql_handler.fetchall(
                """
                SELECT ID, NUMERO, MENSAGEM
                FROM MENSAGENS_WHATSAPP 
                WHERE ENVIO IS NULL 
                AND COD_ERRO IS NULL 
                AND ERRO IS NULL
                """
            )

            for id, numero, mensagem in result:
                message = WhatsappMessage(id, numero, mensagem)
                unsent_messages.append(message)
        finally:
            sql_handler.close()

        return unsent_messages

    @staticmethod
    def update_message_error(message_id: int, error_code: int, error_message: str):
        try:
            sql_handler = SQLHandler(get_db_connection())
            sql_handler.exec_query(
                """
                UPDATE MENSAGENS_WHATSAPP SET
                    COD_ERRO = ?,
                    ERRO = ?
                WHERE 
                    ID = ? 
                """,
                (error_code, error_message, message_id)
            )
        finally:
            sql_handler.close()

    @staticmethod
    def update_message_send(message_id: int, send_time: str):
        try:
            sql_handler = SQLHandler(get_db_connection())
            sql_handler.exec_query(
                "UPDATE MENSAGENS_WHATSAPP SET ENVIO = ?, COD_ERRO = NULL, ERRO = NULL WHERE ID = ?",
                (send_time, message_id)
            )
        finally:
            sql_handler.close()

    @staticmethod
    def update_waiting_qrcode(value: str):
        try:
            sql_handler = SQLHandler(get_db_connection())
            sql_handler.exec_query(
                "UPDATE CONFIGURACOES2 SET WHATSAPP_AGUARDANDO_QRCODE = ?",
                (value,)
            )
        finally:
            sql_handler.close()
