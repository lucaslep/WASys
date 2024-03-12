from selenium.webdriver.support.ui import WebDriverWait
import selenium.webdriver.support.expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from pages import BasePage
from utils import (
    update_whatsapp_waiting_qrcode,
    log_and_print,
    start_webdriver,
    update_whatsapp_waiting_qrcode,
    Helpers,
)
import time, sys


class WhatsappPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        if not "web.whatsapp.com" in self.driver.current_url:
            self.driver.get("https://web.whatsapp.com/")

    qrcode_by = (By.XPATH, '//*[@id="app"]/div/div[2]/div[3]/div[1]/div/div/div[2]/div')

    def login(self):
        log_and_print("WhatsApp não logado, iniciando rotina de Login ... ")
        update_whatsapp_waiting_qrcode("S")

        while not self.is_logged():
            qrcode = self.get_qrcode()
            Helpers.clear_terminal()
            log_and_print("Aguardando captura do QRCode para login ...")
            qrcode.print_ascii()
            time.sleep(30)

        update_whatsapp_waiting_qrcode("N")

    def is_logged(self):
        reference_located = False
        while not reference_located:
            # Se encontrar esse elemento significa que o whatsapp está logado
            chat_page_element = self.driver.find_elements(By.ID, "side")
            if chat_page_element:
                reference_located = True
                return True

            # Se encontrar esse elemento significa que está na tela de login
            login_page_element = self.driver.find_elements(
                By.CSS_SELECTOR, "div.landing-main"
            )
            if login_page_element:
                reference_located = True
                return False

            time.sleep(1)

    def get_qrcode(self):
        try:
            WebDriverWait(self.driver, 15).until(self.__qrcode_loaded)
        except TimeoutException as e:
            raise TimeoutException("Timeout ao aguardar carregamento do QRCode")

        qrcode_element = self.driver.find_element(
            *self.qrcode_by,
        )
        if qrcode_element:
            qr_string = qrcode_element.get_attribute("data-ref")
            return Helpers.gen_qrcode_from_string(qr_string)

    def __qrcode_loaded(self, driver):
        try:
            qrcode = driver.find_element(*self.qrcode_by)
            return qrcode.get_attribute("data-ref") is not None
        except:
            return False
