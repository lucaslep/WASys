# LOCAL SOURCE
from pages import WhatsappPage
from utils import (
    send_whatsapp_messages,
    log_and_print,
    exit_with_log,
    IntelectualSysDB,
    start_webdriver,
)
from config.globals import (
    set_db_connection,
    set_app_path,
)
from repositories.whatsapp_repository import WhatsappRepository
import time

log_and_print(
    "Bem vindo! " + "Iniciando WaSys ... " + "Powered By Sóftica Informática ©"
)
log_and_print("Conectando ao Banco de dados...")
try:
    set_app_path(__file__)

    database = IntelectualSysDB()
    con = database.connect()
    set_db_connection(con)

    log_and_print("Conexão com o banco efetuada com sucesso!")

    driver = start_webdriver(visible=False)
    whatsapp_page = WhatsappPage(driver)
    if not whatsapp_page.is_logged():
        whatsapp_page.login()

    while True:
        unsent_messages = WhatsappRepository.get_unsent_messages()
        messages_count = len(unsent_messages)

        if messages_count > 0:
            log_and_print(
                f"Foram encontradas {messages_count} mensagens a serem enviadas"
            )
            send_whatsapp_messages(driver, unsent_messages)
        else:
            log_and_print(
                "Nenhuma mensagem a ser enviada ... Aguardando novas mensagens"
            )

        time.sleep(10)

except Exception as e:
    log_and_print(str(e))

finally:
    driver.quit()
    database.disconnect()
    exit_with_log("Encerrando módulo WhatsApp, até mais!")
