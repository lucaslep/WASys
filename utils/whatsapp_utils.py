# Libs.
import os
from datetime import datetime
import time

from constants import whatsapp_constants as wpp_constants
from constants.error_messages import ATTACHMENT_NOT_FOUND_ERROR, INVALID_NUMBER_ERROR
from repositories.attachments_repository import (
    AttachmentRepository,
)
from utils import Helpers, log_and_print
from pages.chat_page import ChatPage
from repositories.whatsapp_repository import WhatsappRepository
from exceptions import InvalidAttachmentException, InvalidNumberException


def handle_invalid_attachment(
    message_id: int, attachment_id: int, attachment_sequence: int, file_name: str
):

    log_and_print(
        Helpers.format_error_message(
            ATTACHMENT_NOT_FOUND_ERROR, [message_id, file_name]
        )
    )

    WhatsappRepository.update_message_error(
        message_id, wpp_constants.ANEXOS_ERROR_CODE, wpp_constants.ANEXOS_ERROR_MESSAGE
    )
    AttachmentRepository.update_attachment_error(attachment_id, attachment_sequence)


def handle_invalid_number_exception(message_id, number):
    try:
        log_and_print(
            Helpers.format_error_message(INVALID_NUMBER_ERROR, [message_id, number])
        )

        WhatsappRepository.update_message_error(
            message_id,
            wpp_constants.INVALID_NUMBER_ERROR_CODE,
            wpp_constants.INVALID_NUMBER_MESSAGE,
        )

    except Exception as e:
        log_and_print(e)


def mark_message_as_sent(messageId):
    send_time = datetime.now()
    send_time = send_time.strftime("%d.%m.%Y %H:%M:%S")

    try:
        WhatsappRepository.update_message_send(messageId, send_time)
    except Exception as e:
        log_and_print(str(e))


def send_whatsapp_messages(driver, messages):
    for message in messages:
        chat_page = ChatPage(driver, message.number, message.message)

        try:
            if not chat_page.is_number_valid():
                raise InvalidNumberException(message.message_id, message.number)

            if message.has_attachment():
                attachments = AttachmentRepository.get_attachments_by_id(
                    message.attachment_id
                )
                for attachment in attachments:
                    if not os.path.isfile(rf"{attachment.file_path}"):
                        raise InvalidAttachmentException(
                            message.message_id,
                            attachment.attachment_id,
                            attachment.sequence,
                            attachment.file_name,
                        )

            chat_page.send_message()
            if message.has_attachment():
                chat_page.send_attachments(attachments)

            log_and_print(
                f"Mensagem para o número {message.number} enviada com sucesso!"
            )
            time.sleep(3)
            mark_message_as_sent(message.message_id)

        except InvalidNumberException as e:
            handle_invalid_number_exception(e.message_id, e.number)
            continue

        except InvalidAttachmentException as e:
            handle_invalid_attachment(
                e.message_id, e.attachment_id, e.attachment_sequence, e.file_name
            )
            continue


def update_whatsapp_waiting_qrcode(value="N"):
    if value is None:
        raise Exception(
            'Nenhum valor informado para atualizar o campo "WHATSAPP_AGUARDANDO_QRCODE" '
        )

    value = value.upper()

    if value not in ["S", "N"]:
        raise Exception(
            'Valore do campo "WHATSAPP_AGUARDANDO_QRCODE" é inválido, a opção deve estar entre "S" ou "N"'
        )

    try:
        WhatsappRepository.update_waiting_qrcode(value)
    except Exception as e:
        log_and_print(str(e))
