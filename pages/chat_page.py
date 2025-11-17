from selenium.webdriver.support.ui import WebDriverWait
import selenium.webdriver.support.expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time, urllib, logging, os
from pages import BasePage
from components import Message
from exceptions import AttachmentTimeoutException, InvalidNumberException
from utils.ini_file import IniFile
from config.globals import get_app_dir

logger = logging.getLogger("main")


class ChatPage(BasePage):
    def __init__(self, driver, number: str, message: str):
        super().__init__(driver)

        config_path = os.path.join(get_app_dir(), 'config.ini')
        self.ini_config = IniFile(config_path)
        self.load_selectors()

        text = urllib.parse.quote(f"{message}")
        whatsapp_url = f"https://web.whatsapp.com/send?phone={number}&text={text}"
        self.driver.get(whatsapp_url)

        self.wait_load()

    def load_selectors(self):
        # Load selectors from config.ini

        self.send_btn_by = (
            By.XPATH,
            self.ini_config.get_value("SEND_BUTTON"),
        )
        self.attachment_btn_by = (
            By.XPATH,
            self.ini_config.get_value("ATTACHMENT_BUTTON"),
        )
        self.file_input_by = (
            By.XPATH,
            self.ini_config.get_value("FILE_INPUT_XPATH"),
        )
        self.send_file_btn_by = (
            By.XPATH,
            self.ini_config.get_value("SEND_ATTACHMENT_BUTTON_XPATH"),
        )

    def wait_load(self):
        wait = WebDriverWait(self.driver, 30)
        wait.until(EC.visibility_of_element_located((By.ID, "side")))

        chat_loaded = False
        while not chat_loaded:
            element = self.driver.find_elements(
                By.XPATH,
                '//*[@id="app"]/div/span[2]/div/span/div/div/div/div/div/div[1]',
            )

            if not element:
                chat_loaded = True



            time.sleep(1)
        time.sleep(1)

    def wait_upload_attachment(self, message_index, timeout):
        is_attachment_sent = False
        seconds_waited = 0
        while not is_attachment_sent:
            time.sleep(1)
            seconds_waited += 1
            if seconds_waited >= timeout:
                raise AttachmentTimeoutException("Timeout ao aguardar envio de anexo")

            last_message = self.get_message_out_by_index(message_index)
            is_attachment_sent = last_message.is_sent()

    def get_messages_out(self):
        return self.driver.find_elements(By.CSS_SELECTOR, "div.message-out")

    def get_last_message_sent(self):
        messages = self.get_messages_out()
        return Message(messages[-1])

    def get_message_out_by_index(self, message_index):
        messages = self.get_messages_out()

        if message_index > len(messages) - 1:
            raise Exception("Indice fora do range de mensagens enviadas")

        return Message(messages[message_index])



    def send_message(self):
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.element_to_be_clickable(self.send_btn_by)).click()

    def send_attachment(self, attachment):
        logger.info(f"Enviando anexo: {attachment.file_path}")
        # Clica no clips
        logger.info("Clicando no botão de anexo...")
        clip_element = self.wait.until(
            EC.element_to_be_clickable(self.attachment_btn_by)
        )
        clip_element.click()
        logger.info("Botão de anexo clicado.")

        # Localiza o Input de arquivos e envia os arquivos
        logger.info("Procurando o input de arquivo...")
        file_input_element = self.wait.until(
            EC.presence_of_element_located(self.file_input_by)
        )
        logger.info("Input de arquivo encontrado.")
        logger.info(f"Enviando o caminho do arquivo: {attachment.file_path}")
        file_input_element.send_keys(attachment.file_path)
        logger.info("Caminho do arquivo enviado.")

        # Clica no botão de envio
        logger.info("Procurando o botão de enviar anexo...")
        send_file_button = self.wait.until(
            EC.element_to_be_clickable(self.send_file_btn_by)
        )
        logger.info("Botão de enviar anexo encontrado.")
        send_file_button.click()
        logger.info("Botão de enviar anexo clicado.")
        time.sleep(1)

        last_message_index = len(self.get_messages_out()) - 1
        self.wait_upload_attachment(last_message_index, 30)

    def send_all_attachments(self, attachments):
        for attachment in attachments:
            try:
                time.sleep(1)
                self.send_attachment(attachment)

            except AttachmentTimeoutException as e:
                logger.error(
                    f"Timeout ao aguardar envio de anexo: {attachment.file_name}:\n\n {e}"
                )
                continue

            except Exception as e:
                logger.error(
                    f"Ocorreram problemas ao enviar o arquivo: {attachment.file_name}:\n\n {e}"
                )
                continue
