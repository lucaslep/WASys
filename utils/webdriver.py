from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from subprocess import CREATE_NO_WINDOW
from config.globals import get_app_dir
from config.settings import settings
from exceptions import DriverInitException
from utils.helpers import Helpers
import os
import logging

logger = logging.getLogger("main")

def start_webdriver(visible: bool = None):
    if visible is None:
        visible = settings.browser_visible
    
    logger.info(f"Iniciando WebDriver (Configuração Visível: {visible})")

    # Tenta limpar processos antigos ANTES de começar para evitar conflitos de perfil
    Helpers.kill_process("chrome")
    
    # Limpa o arquivo de trava do perfil se existir
    user_data_dir = os.path.join(get_app_dir(), "user_data")
    lock_file = os.path.join(user_data_dir, "DevToolsActivePort")
    if os.path.exists(lock_file):
        try:
            os.remove(lock_file)
        except:
            pass

    try:
        driver_path = install_webdriver()

        if not driver_path.endswith(".exe"):
            driver_path = os.path.dirname(driver_path) + r"\chromedriver.exe"

        chrome_service = ChromeService(executable_path=driver_path)
        chrome_service.creationflags = CREATE_NO_WINDOW

        driver = webdriver.Chrome(
            service=chrome_service,
            options=get_chrome_options(visible),
        )

        driver.set_page_load_timeout(30)

        # Remove webdriver flag
        driver.execute_script(
            "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
        )

        return driver

    except Exception as e:
        logger.error(f"Erro ao inicializar o WebDriver: {e}")
        raise DriverInitException(str(e))

def get_chrome_options(visible: bool):
    options = Options()
    user_data_dir = os.path.join(get_app_dir(), "user_data")

    # Mantém sessão do WhatsApp
    options.add_argument(rf"--user-data-dir={user_data_dir}")
    options.unhandled_prompt_behavior = "accept"

    if visible:
        options.add_argument("--start-maximized")
    else:
        # Força o modo headless para garantir que não apareça
        options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1080")
        # Posição negativa como redundância
        options.add_argument("--window-position=-32000,-32000")

    # Anti-detecção
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument("--disable-blink-features=AutomationControlled")

    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"
    )

    # Performance e Estabilidade
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    options.add_argument("--log-level=3")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument("--remote-debugging-port=9222")

    return options

def install_webdriver():
    try:
        return ChromeDriverManager().install()
    except Exception as e:
        logger.warning(f"Falha ao instalar ChromeDriver padrão, tentando fallback: {e}")
        return ChromeDriverManager(driver_version="109.0.5414.74").install()
