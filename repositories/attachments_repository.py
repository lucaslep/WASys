from config.globals import get_db_connection
from utils import SQLHandler
from typing import List


class Attachment:
    def __init__(self, attachment_id, sequence, file_name, file_path, error):
        self.attachment_id = attachment_id
        self.sequence = sequence
        self.file_name = file_name
        self.file_path = file_path
        self.error = error


class AttachmentRepository:
    @staticmethod
    def get_attachments_by_id(id_attachment) -> List[Attachment]:
        attachments = []
        try:
            sql_handler = SQLHandler(get_db_connection())
            result = sql_handler.fetchall(
                "SELECT ID, SEQ, NOME_ARQUIVO, ARQUIVO, ERRO FROM ANEXOS_WHATSAPP WHERE ID = %i"
                % (id_attachment)
            )

            for attachment_id, sequence, file_name, file_path, error in result:
                attachments.append(
                    Attachment(attachment_id, sequence, file_name, file_path, error)
                )

        finally:
            sql_handler.close()

        return attachments

    @staticmethod
    def update_attachment_error(attachment_id, attachment_sequence):
        try:
            sql_handler = SQLHandler(get_db_connection())
            sql_handler.exec_query(
                """
                UPDATE ANEXOS_WHATSAPP SET
                    ERRO = 1
                WHERE 
                    ID = %i AND 
                    SEQ = %i 
                """
                % (attachment_id, attachment_sequence)
            )
        finally:
            sql_handler.close()
