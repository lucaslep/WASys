from components import BaseComponent
from selenium.webdriver.common.by import By
from enum import Enum
import os
from utils.ini_file import IniFile
from config.globals import get_app_dir


class MessageStatus(Enum):
    READ = "Lida"
    DELIVERED = "Entregue"


class Message(BaseComponent):
    def __init__(self, root):
        super().__init__(root)
        config_path = os.path.join(get_app_dir(), 'config.ini')
        self.ini_config = IniFile(config_path)
        self.status_by = (
            By.CSS_SELECTOR,
            self.ini_config.get_value("MESSAGE_STATUS_CSS"),
        )

    def is_sent(self):
        try:
            status = self.get_status()
            return (
                status == MessageStatus.READ.value
                or status == MessageStatus.DELIVERED.value
            )
        except:
            # Se não encontrar o status, assume que não foi enviado ainda
            return False

    def get_status(self):
        status_element = self.root.find_element(*self.status_by)
        return status_element.get_attribute("ariaLabel").strip()
