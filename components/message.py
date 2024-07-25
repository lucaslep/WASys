from components import BaseComponent
from selenium.webdriver.common.by import By
from enum import Enum


class MessageStatus(Enum):
    READ = "Lida"
    DELIVERED = "Entregue"


class Message(BaseComponent):
    def __init__(self, root):
        super().__init__(root)

    status_by = (By.CSS_SELECTOR, "div.x1pn4fmt > span")

    def is_sent(self):
        status = self.get_status()
        return (
            status == MessageStatus.READ.value
            or status == MessageStatus.DELIVERED.value
        )

    def get_status(self):
        status_element = self.root.find_element(*self.status_by)
        return status_element.get_attribute("ariaLabel").strip()
