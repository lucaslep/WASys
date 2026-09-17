from selenium.webdriver.support.ui import WebDriverWait
import selenium.webdriver.support.expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time, urllib, logging, os
from pages import BasePage
from config.settings import settings
from exceptions.whatsapp_exceptions import MessageSendException

logger = logging.getLogger("main")

class ChatPage(BasePage):
    def __init__(self, driver, number: str, message: str):
        super().__init__(driver)
        self.number = number
        self.message = message
        self.send_btn_by = (By.XPATH, settings.selector_send_btn)

    def open_chat(self):
        text = urllib.parse.quote(f"{self.message}")
        whatsapp_url = f"https://web.whatsapp.com/send?phone={self.number}&text={text}"
        self.driver.get(whatsapp_url)
        self.wait_load_chat()

    def wait_load_chat(self):
        try:
            # Espera o painel lateral (indica que o WA carregou) e o botão de enviar
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.ID, "side"))
            )
            WebDriverWait(self.driver, 15).until(
                EC.element_to_be_clickable(self.send_btn_by)
            )
        except TimeoutException:
            logger.error(f"Timeout ao carregar chat para o número {self.number}")
            raise MessageSendException(f"Não foi possível carregar o chat para {self.number}")

    def send_message(self):
        try:
            btn = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self.send_btn_by)
            )
            btn.click()
            # Pequena espera para garantir que o clique foi processado
            time.sleep(1)
        except Exception as e:
            raise MessageSendException(f"Erro ao clicar no botão de enviar: {e}")
