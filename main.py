# LOCAL SOURCE
from exceptions.driver_init_exception import DriverInitException
from pages import WhatsappPage
from repositories.attachments_repository import AttachmentRepository
from repositories.whatsapp_repository import WhatsappRepository
from repositories.config_repository import ConfigRepository
from utils import (
    send_whatsapp_messages,
    IntelectualSysDB,
    start_webdriver,
    setup_logger,
    Helpers,
    update_whatsapp_waiting_qrcode,
)
from config.globals import set_db_connection, set_app_path, get_app_dir
import time, os, logging, sys
from utils.ini_file import IniFile
from utils.whatsapp_utils import handle_invalid_attachment

if __name__ == "__main__":
    set_app_path(__file__)
    setup_logger()
    os.environ["WDM_LOG"] = str(logging.NOTSET)  # Desativa o log do webdriver manager

    logger = logging.getLogger("main")
    logger.info(
        "Bem vindo! " + "Iniciando WaSys ... " + "Powered By Sóftica Informática ©"
    )
    driver = None
    try:
        ini_path = rf"{get_app_dir()}/IntelectualSys.ini"
        ini = IniFile(ini_path)

        logger.info("Conectando ao Banco de dados...")
        db_path = Helpers.decrypt(ini.get_value("DBCnxSystem"))
        database = IntelectualSysDB(db_path)
        con = database.connect()
        set_db_connection(con)
        logger.info("Conexão com o banco efetuada com sucesso!")

        while Helpers.has_internet_connection() == False:
            logger.error("Sem conexão com a internet")
            time.sleep(10)
            pass

        browser_visible = ini.get_value("WASYS_NAVEGADOR_VISIVEL")

        try:
            driver = start_webdriver(visible=browser_visible)
        except DriverInitException as e:
            # Encerra o processo do chrome caso esteja aberto
            if ConfigRepository.get_config_by_field("WEB", 2) != "S":
                Helpers.kill_process("chrome")

            # Tenta startar o navegador novamente
            driver = start_webdriver(visible=browser_visible)

        whatsapp_page = WhatsappPage(driver)
        if not whatsapp_page.is_logged():
            whatsapp_page.login()

        logger.info("Conectado ao whatsapp com sucesso!")
        update_whatsapp_waiting_qrcode("N")

        while True:
            if Helpers.has_internet_connection() == False:
                logger.error(
                    "A conexão com a internet caiu durante o envio, Aguardando conexão"
                )
                time.sleep(10)
                continue

            unsent_messages = WhatsappRepository.get_unsent_messages()
            messages_count = len(unsent_messages)

            for message in unsent_messages:
                if not message.has_attachment():
                    continue

                message.attachments = AttachmentRepository.get_attachments_by_id(
                    message.attachment_id
                )

            if messages_count <= 0:
                logger.info(
                    "Nenhuma mensagem a ser enviada ... Aguardando novas mensagens"
                )
                time.sleep(Helpers.minutes_to_seconds(1))
                continue

            logger.info(
                f"Foram encontradas {messages_count} mensagens a serem enviadas"
            )

            for i in reversed(range(len(unsent_messages))):
                message = unsent_messages[i]
                is_attachment_valid = True
                for attachment in message.attachments:
                    if not os.path.isfile(rf"{attachment.file_path}"):
                        is_attachment_valid = False
                        handle_invalid_attachment(
                            message.message_id,
                            attachment.attachment_id,
                            attachment.sequence,
                            attachment.file_name,
                        )

                if not is_attachment_valid:
                    unsent_messages.pop(i)

            if len(unsent_messages) > 0:
                send_whatsapp_messages(driver, unsent_messages)

            time.sleep(Helpers.minutes_to_seconds(1))

    except Exception as e:
        logger.error(str(e))

    finally:
        if driver is not None:
            driver.quit()

        database.disconnect()
        input("\nPressione qualquer tecla para encerrar ...")
        sys.exit("Encerrando módulo WhatsApp, até mais!")
