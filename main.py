from exceptions.driver_init_exception import DriverInitException
from pages import WhatsappPage
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
from config.settings import settings
import time
import os
import logging
import sys

if __name__ == "__main__":
    set_app_path(__file__)
    setup_logger()
    os.environ["WDM_LOG"] = str(logging.NOTSET)

    logger = logging.getLogger("main")
    logger.info("WaSys Iniciado | Powered By Sóftica Informática ©")
    
    database = None
    driver = None
    
    try:
        logger.info("Conectando ao Banco de dados...")
        database = IntelectualSysDB(settings.db_path)
        set_db_connection(database.connect())
        logger.info("Banco de dados conectado!")

        while not Helpers.has_internet_connection():
            logger.error("Aguardando conexão com a internet...")
            time.sleep(10)

        try:
            driver = start_webdriver()
        except DriverInitException as e:
            logger.error(f"Falha crítica ao iniciar navegador: {e}")
            sys.exit(1)

        whatsapp_page = WhatsappPage(driver)
        if not whatsapp_page.is_logged():
            whatsapp_page.login()

        logger.info("WhatsApp conectado com sucesso!")
        update_whatsapp_waiting_qrcode("N")

        while True:
            if not Helpers.has_internet_connection():
                logger.error("Conexão perdida. Aguardando...")
                time.sleep(10)
                continue

            unsent_messages = WhatsappRepository.get_unsent_messages()
            
            if not unsent_messages:
                logger.info("Nenhuma mensagem pendente. Aguardando 1 minuto...")
                time.sleep(Helpers.minutes_to_seconds(1))
                continue

            logger.info(f"Enviando {len(unsent_messages)} mensagens...")
            send_whatsapp_messages(driver, unsent_messages)
            
            time.sleep(Helpers.minutes_to_seconds(1))

    except Exception as e:
        logger.error(f"Erro Fatal: {e}")

    finally:
        if driver:
            driver.quit()
        if database:
            database.disconnect()
        
        input("\nPressione qualquer tecla para encerrar...")
        sys.exit(0)
