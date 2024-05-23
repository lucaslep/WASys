from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from subprocess import CREATE_NO_WINDOW
from utils import get_current_disk


def start_webdriver(visible: bool):
    headless = False if visible else True

    try:
        driver_path = ChromeDriverManager().install()
    except:
        # Se não conseguir instalar o chromeDriver correspondente ao chrome
        # instala uma versão fallback.
        driver_path = ChromeDriverManager(driver_version="109.0.5414.74").install()

    chrome_service = ChromeService(executable_path=driver_path)
    chrome_service.creationflags = CREATE_NO_WINDOW

    driver = webdriver.Chrome(
        service=chrome_service,
        options=get_chrome_options(headless),
    )
    driver.maximize_window()

    return driver


def get_chrome_options(headless):
    options = Options()

    user_data_dir = r"" + get_current_disk() + r"Google\Chrome\User Data\Default"

    options.headless = headless
    options.unhandled_prompt_behavior = "accept"
    options.add_argument(r"--user-data-dir=" + user_data_dir)
    options.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"
    )
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_argument("--start-maximized")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-application-chache=0")
    options.add_argument("--log-level=3")

    return options
