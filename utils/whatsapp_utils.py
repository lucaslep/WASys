# Libs.
import os, time, logging
from datetime import datetime
from typing import List

from constants import whatsapp_constants as wpp_constants
from constants.error_messages import (
    ATTACHMENT_NOT_FOUND_ERROR,
    INVALID_NUMBER_ERROR,
)
from repositories.attachments_repository import (
    AttachmentRepository,
)
from utils import Helpers, WhatsappMessage
from pages.chat_page import ChatPage
from repositories.whatsapp_repository import WhatsappRepository
from exceptions import InvalidAttachmentException, InvalidNumberException


logger = logging.getLogger("main")


def handle_invalid_attachment(
    message_id: int, attachment_id: int, attachment_sequence: int, file_name: str
):
    logger.error(
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
        logger.error(
            Helpers.format_error_message(INVALID_NUMBER_ERROR, [message_id, number])
        )

        WhatsappRepository.update_message_error(
            message_id,
            wpp_constants.INVALID_NUMBER_ERROR_CODE,
            wpp_constants.INVALID_NUMBER_MESSAGE,
        )

    except Exception as e:
        logger.error(e)


def handle_unknown_exception(message_id, number):
    logger.error(
        Helpers.format_error_message(wpp_constants.UNKNOWN_ERROR_MSG, [number])
    )
    WhatsappRepository.update_message_error(
        message_id, wpp_constants.UNKNOWN_ERROR_CODE, wpp_constants.UNKNOWN_ERROR_MSG
    )


def mark_message_as_sent(messageId):
    send_time = datetime.now()
    send_time = send_time.strftime("%d.%m.%Y %H:%M:%S")

    try:
        WhatsappRepository.update_message_send(messageId, send_time)
    except Exception as e:
        logger.error(str(e))


def send_whatsapp_messages(driver, messages: List[WhatsappMessage], delay: int = 5):
    for message in messages:
        try:
            if message.number is None:
                logger.error(f"Número inválido para a mensagem: {message.message_id}")
                continue

            chat_page = ChatPage(driver, message.number, message.message)
            chat_page.send_message()

            if message.has_attachment():
                if message.attachments is None or len(message.attachments) == 0:
                    logger.warning(
                        f"Nenhum anexo encontrado para a mensagem: {message.message_id}"
                    )
                else:
                    attachments_sent_successfully = chat_page.send_all_attachments(message.attachments)

            logger.info(f"Mensagem e anexo para o número {message.number} enviada com sucesso!")
            mark_message_as_sent(message.message_id)

        except InvalidNumberException as e:
            handle_invalid_number_exception(message.message_id, message.number)
            continue

        except InvalidAttachmentException as e:
            logger.error(f"Erro ao enviar anexo para a mensagem: {message.message_id}")
            continue

        except Exception as e:
            logger.error(f"Erro desconhecido ao enviar mensagem: {str(e)}")
            handle_unknown_exception(message.message_id, message.number)
            continue

        finally:
            # Garante que o delay seja um valor válido
            if isinstance(delay, int) and delay > 0:
                time.sleep(delay)
            else:
                logger.error(
                    "Delay deve ser um valor inteiro positivo. Usando padrão de 5 segundos."
                )
                time.sleep(5)


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
        logger.error(str(e))
