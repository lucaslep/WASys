from selenium.webdriver.support.ui import WebDriverWait


class BaseComponent:
    def __init__(self, root):
        self.root = root
        self.wait = WebDriverWait(self.root, 10)
