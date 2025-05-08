from selenium.webdriver.support.ui import WebDriverWait
import selenium.webdriver.support.expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time, urllib, logging
from pages import BasePage
from components import Message
from exceptions import AttachmentTimeoutException, InvalidNumberException

logger = logging.getLogger("main")


class ChatPage(BasePage):
    def __init__(self, driver, number: str, message: str):
        super().__init__(driver)

        text = urllib.parse.quote(f"{message}")
        whatsapp_url = f"https://web.whatsapp.com/send?phone={number}&text={text}"
        self.driver.get(whatsapp_url)

        self.wait_load()

    invalid_number_by = (
        By.XPATH,
        f"//*[text()='O número de telefone compartilhado por url é inválido.']",
    )

    send_btn_by = (
        By.XPATH,
        # '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[2]/button',
        '//*[@id="main"]/footer/div[1]/div/span/div/div[2]/div/div[4]/button/span',
    )

    send_file_btn_by = (
        By.CSS_SELECTOR,
        '[aria-label="Enviar"]',
        # '//*[@id="app"]/div/div[2]/div[2]/div[2]/span/div/div/div/div[2]/div/div[2]/div[2]',
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

            if not self.is_number_valid():
                raise InvalidNumberException("Número de telefone inválido")

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

    def is_number_valid(self):
        try:
            element = self.driver.find_element(*self.invalid_number_by)
            # if element.text == "O número de telefone compartilhado por url é inválido.":
            if element:
                return False
            else:
                return True

        except NoSuchElementException:
            return True

    def send_message(self):
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.element_to_be_clickable(self.send_btn_by)).click()

    def send_attachment(self, attachment):
        # Clica no clips
        clip_element = self.wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    '//*[@id="main"]/footer/div[1]/div/span/div/div[1]/div/button/span',
                )
            )
        )
        clip_element.click()

        # Localiza o Input de arquivos e envia os arquivos
        file_input_element = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file']"))
        )
        file_input_element.send_keys(attachment.file_path)

        # Clica no botão de envio
        send_file_button = self.wait.until(
            EC.element_to_be_clickable(self.send_file_btn_by)
        )
        send_file_button.click()
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
