from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from subprocess import CREATE_NO_WINDOW
from utils.fileUtils import getCurrentPath, getCurrentDisk
from utils.sysUtils import logAndPrint
from config import globals
import os
import logging


def startWebDriver(visible):
    headless = False if visible else True

    driver = webdriver.Chrome(
        service=getWebManagerService(),
        options=getWebDriverOptions(headless),
    )
    driver.maximize_window()

    return driver


def getWebDriverOptions(headless):
    options = Options()

    userDataDir = r"" + getCurrentDisk() + r"Google\Chrome\User Data\Default"

    options.headless = headless
    options.add_argument(r"--user-data-dir=" + userDataDir)
    options.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"
    )
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-extensions")
    #  options.add_argument("--no-sandbox")
    #  options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--start-maximized")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-application-chache=0")
    #  options.add_argument("--headless")
    options.add_argument("--log-level=3")
    #  options.add_experimental_option("excludeSwitches", ["enable-logging"])
    #  options.add_argument("--disable-logging")

    return options


def getWebManagerService():
    chromeService = ChromeService(ChromeDriverManager().install())
    chromeService.creationflags = CREATE_NO_WINDOW

    return chromeService
