from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from subprocess import CREATE_NO_WINDOW
from config.globals import get_app_dir
from exceptions import DriverInitException
import os


def start_webdriver(visible: bool = False):
    headless = False if visible else True

    driver_path = install_webdriver()

    if not driver_path.endswith(".exe"):
        driver_path = os.path.dirname(driver_path) + r"\chromedriver.exe"

    chrome_service = ChromeService(executable_path=driver_path)
    chrome_service.creationflags = CREATE_NO_WINDOW

    try:
        driver = webdriver.Chrome(
            service=chrome_service,
            options=get_chrome_options(headless),
        )
        driver.set_page_load_timeout(20)
        # 👇 Remove a flag "webdriver" do navegador
        driver.execute_script(
            "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
        )
    except Exception as e:
        raise DriverInitException(str(e))

    driver.maximize_window()

    return driver


def get_chrome_options(headless: bool):
    options = Options()

    user_data_dir = os.path.join(get_app_dir(), "user_data")

    options.headless = headless
    options.unhandled_prompt_behavior = "accept"

    if headless:
        # Se estiver em segundo plano, escondo a janela pois a nova
        # versão do chrome está exibindo uma janela em branco.
        options.add_argument("--window-position=-2400,-2400")

    # ✅ Evitar detecção por automação:
    options.add_argument(rf"--user-data-dir={user_data_dir}")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"
    )

    # ✅ Outras opções úteis:
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-extensions")

    if not headless:
        options.add_argument("--start-maximized")
        options.add_argument("--window-size=1920,1080")

    options.add_argument("--disable-gpu")
    options.add_argument("--log-level=3")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")

    return options


def install_webdriver():
    try:
        driver_path = ChromeDriverManager().install()
    except:
        # Se não conseguir instalar o chromeDriver correspondente ao chrome
        # instala uma versão fallback.
        print("Efetuando download do chrome driver 109.0.5414.74")
        driver_path = ChromeDriverManager(driver_version="109.0.5414.74").install()

    return driver_path
