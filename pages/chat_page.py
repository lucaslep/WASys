from selenium.webdriver.support.ui import WebDriverWait
import selenium.webdriver.support.expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
import urllib
from pages import BasePage
from utils import log_and_print


class ChatPage(BasePage):
    def __init__(self, driver, number: str, message: str):
        super().__init__(driver)

        text = urllib.parse.quote(f"{message}")
        whatsapp_url = f"https://web.whatsapp.com/send?phone={number}&text={text}"
        self.driver.get(whatsapp_url)
        self.wait_whatsapp_page_load(15)

    invalid_number_by = (
        By.XPATH,
        '//*[@id="app"]/div/span[2]/div/span/div/div/div/div/div/div[1]',
    )

    send_btn_by = (
        By.XPATH,
        '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[2]/button',
    )

    send_file_btn_by = (
        By.XPATH,
        '//*[@id="app"]/div/div[2]/div[2]/div[2]/span/div/span/div/div/div[2]/div/div[2]/div[2]/div/div',
    )

    def wait_whatsapp_page_load(self, timeout):
        wait = WebDriverWait(self.driver, timeout)
        wait.until(EC.visibility_of_element_located((By.ID, "side")))

    def is_number_valid(self):
        try:
            element = self.driver.find_element(*self.invalid_number_by)
            if element.text == "O número de telefone compartilhado por url é inválido.":
                return False
            else:
                return True

        except NoSuchElementException:
            return True

    def send_message(self):
        wait = WebDriverWait(self.driver, 50)
        wait.until(EC.element_to_be_clickable(self.send_btn_by)).click()

    def send_attachments(self, attachments):
        for attachment in attachments:
            try:
                time.sleep(1)
                # Clica no clips
                clip_element = self.wait.until(
                    EC.element_to_be_clickable(
                        (
                            By.XPATH,
                            '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[1]/div/div',
                        )
                    )
                )
                clip_element.click()

                # Localiza o Input de arquivos e envia os arquivos
                file_input_element = self.wait.until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, "input[type='file']")
                    )
                )
                file_input_element.send_keys(attachment.file_path)

                # Clica no botão de envio
                send_file_button = self.wait.until(
                    EC.element_to_be_clickable(self.send_file_btn_by)
                )
                send_file_button.click()
            except Exception as e:
                log_and_print(
                    f"Ocorreram problemas ao enviar o arquivo: {attachment.file_name}:\n\n {e}"
                )
                continue
