from config.globals import get_db_connection
from utils import SQLHandler
from utils import WhatsappMessage


class WhatsappRepository:
    @staticmethod
    def get_unsent_messages():
        unsent_messages = []
        try:
            sql_handler = SQLHandler(get_db_connection())
            result = sql_handler.fetchall(
                """
                SELECT ID, NUMERO, MENSAGEM, ID_ANEXO 
                FROM MENSAGENS_WHATSAPP 
                WHERE ENVIO IS NULL 
                AND COD_ERRO IS NULL 
                AND ERRO IS NULL
                """
            )

            for id, numero, mensagem, id_anexo in result:
                message = WhatsappMessage(id, numero, mensagem, id_anexo)
                unsent_messages.append(message)

        finally:
            sql_handler.close()

        return unsent_messages

    @staticmethod
    def update_message_error(message_id, error_code, error_message):
        try:
            sql_handler = SQLHandler(get_db_connection())
            sql_handler.exec_query(
                """
                UPDATE MENSAGENS_WHATSAPP SET
                    COD_ERRO = %i,
                    ERRO = '%s'
                WHERE 
                    ID = %i 
                """
                % (error_code, error_message, message_id)
            )
        finally:
            sql_handler.close()

    @staticmethod
    def update_message_send(message_id, send_time):
        try:
            sql_handler = SQLHandler(get_db_connection())
            sql_handler.exec_query(
                "UPDATE MENSAGENS_WHATSAPP SET ENVIO = '%s', COD_ERRO = NULL, ERRO = NULL WHERE ID = %i"
                % (send_time, message_id)
            )
        finally:
            sql_handler.close()

    @staticmethod
    def update_waiting_qrcode(value):
        try:
            sql_handler = SQLHandler(get_db_connection())
            sql_handler.exec_query(
                "UPDATE CONFIGURACOES2 SET WHATSAPP_AGUARDANDO_QRCODE = '%s' " % (value)
            )
        finally:
            sql_handler.close()
