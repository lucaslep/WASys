from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import Chrome


class BasePage:
    def __init__(self, driver: Chrome):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)

    def wait_load(self):
        self.wait.until(
            lambda driver: driver.execute_script("return document.readyState")
            == "complete"
        )
