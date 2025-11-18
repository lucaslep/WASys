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
            self.ini_config.get_value("ENVIA_MENSAGEM"),
        )
        self.attachment_btn_by = (
            By.XPATH,
            self.ini_config.get_value("SELECIONA_ANEXO"),
        )
        self.file_input_by = (
            By.XPATH,
            self.ini_config.get_value("CARREGA_ANEXO"),
        )
        self.send_file_btn_by = (
            By.XPATH,
            self.ini_config.get_value("ENVIA_ANEXO"),
        )

    def wait_load(self):
        wait = WebDriverWait(self.driver, 20)
        try:
            wait.until(EC.visibility_of_element_located((By.ID, "side")))
            wait.until(EC.element_to_be_clickable(self.send_btn_by))
        except Exception as e:
            logger.error(f"Erro ao aguardar a página de conversa carregar: {e}")
            # Adicione qualquer outra lógica de tratamento de erro que você queira aqui
            raise

    def send_message(self):
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.element_to_be_clickable(self.send_btn_by)).click()

    def send_attachment(self, attachment):

        # Clica no clips

        clip_element = self.wait.until(
            EC.element_to_be_clickable(self.attachment_btn_by)
        )
        clip_element.click()


        # Localiza o Input de arquivos e envia os arquivos

        file_input_element = self.wait.until(
            EC.presence_of_element_located(self.file_input_by)
        )

        file_input_element.send_keys(attachment.file_path)


        # Clica no botão de envio

        send_file_button = self.wait.until(
            EC.element_to_be_clickable(self.send_file_btn_by)
        )

        send_file_button.click()

        time.sleep(3)

    def send_all_attachments(self, attachments):
        success = True
        for attachment in attachments:
            try:
                self.send_attachment(attachment)

            except AttachmentTimeoutException as e:
                success = False
                continue

            except Exception as e:
                logger.error(
                    f"Ocorreram problemas ao enviar o arquivo: {attachment.file_name}:\n\n {e}"
                )
                success = False
                continue
        return success
