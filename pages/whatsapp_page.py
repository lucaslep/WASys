from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from pages import BasePage
from utils import (
    update_whatsapp_waiting_qrcode,
    Helpers,
)
import time
import logging

logger = logging.getLogger("main")


class WhatsappPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)

        if "web.whatsapp.com" not in self.driver.current_url:
            self.driver.get("https://web.whatsapp.com/")
            time.sleep(20)

    def login(self):
        for _ in range(3):
            if self.is_logged():
                logger.info("WhatsApp já estava logado ou terminou de carregar.")
                return
            time.sleep(5)

        logger.info(
            "WhatsApp não logado, iniciando rotina de Login ..."
        )

        update_whatsapp_waiting_qrcode("S")

        qr_printed = False

        while True:

            # Já logado completamente
            if self.is_logged():
                break

            try:

                qrcode = self.get_qrcode()

                if qrcode and not qr_printed:

                    Helpers.clear_terminal()

                    logger.info(
                        "Aguardando captura do QRCode para login ..."
                    )

                    qrcode.print_ascii()
                    print("\n") 
                    logger.info( "Após a leitura do QRCode, aguarde! " "O WhatsApp Web estará sendo carregado..." )

                    qr_printed = True

            except Exception:
                logger.info("QRCode lido com sucesso. " "Finalizando autenticação...")
                break

            time.sleep(1)

        # Espera sidebar carregar
        WebDriverWait(self.driver, 60).until(
            lambda d: d.find_elements(By.ID, "side")
        )

        logger.info("Login realizado com sucesso!")

        update_whatsapp_waiting_qrcode("N")

    def is_logged(self):

        try:

            # Sidebar principal carregada
            if self.driver.find_elements(By.ID, "side"):
                return True

            # Campo de busca carregado
            if self.driver.find_elements(
                By.CSS_SELECTOR,
                "div[contenteditable='true']"
            ):
                return True

            # Conversas renderizadas
            if self.driver.find_elements(
                By.CSS_SELECTOR,
                "[data-testid='chat-list']"
            ):
                return True

            return False

        except:
            return False


    def get_qrcode(self):

        try:

            WebDriverWait(self.driver, 60).until(
                self.__qrcode_loaded
            )

            # Busca qualquer elemento que tenha data-ref
            qrcode_elements = self.driver.find_elements(
                By.CSS_SELECTOR,
                "[data-ref]"
            )

            for element in qrcode_elements:

                qr_string = element.get_attribute("data-ref")

                if qr_string:
                    return Helpers.gen_qrcode_from_string(
                        qr_string
                    )

            raise Exception(
                "QR Code encontrado mas data-ref vazio."
            )

        except TimeoutException:
            raise TimeoutException(
                "Timeout ao aguardar QRCode."
            )

    def __qrcode_loaded(self, driver):

        try:

            elements = driver.find_elements(
                By.CSS_SELECTOR,
                "[data-ref]"
            )

            for element in elements:

                qr_string = element.get_attribute(
                    "data-ref"
                )

                if qr_string:
                    return True

            return False

        except:
            return False