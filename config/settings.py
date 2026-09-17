import os
import sys
from utils.ini_file import IniFile
from config.globals import get_app_dir
from utils.helpers import Helpers

class Settings:
    _instance = None
    _loaded = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Settings, cls).__new__(cls)
        return cls._instance

    def __getattribute__(self, name):
        # Evita recursão infinita ao acessar atributos internos
        if name in ["_instance", "_loaded", "_load_settings", "__dict__"]:
            return super().__getattribute__(name)
            
        if not self._loaded:
            self._load_settings()
        return super().__getattribute__(name)

    def _load_settings(self):
        app_dir = get_app_dir()
        
        # Fallback se get_app_dir ainda não foi definido (circular dependency)
        if app_dir is None:
            if getattr(sys, 'frozen', False):
                app_dir = os.path.dirname(sys.executable)
            else:
                app_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
        
        # IntelectualSys.ini
        sys_ini_path = os.path.join(app_dir, "IntelectualSys.ini")
        if not os.path.exists(sys_ini_path):
            # Tenta no diretório atual como último recurso
            sys_ini_path = "IntelectualSys.ini"

        try:
            sys_ini = IniFile(sys_ini_path)
            self.db_path = Helpers.decrypt(sys_ini.get_value("DBCnxSystem"))
            self.browser_visible = str(sys_ini.get_value("WASYS_NAVEGADOR_VISIVEL")).strip().upper() == "TRUE"
            
            try:
                self.send_delay = int(sys_ini.get_value("WASYS_INTERVALO_ENVIO") or 5)
            except ValueError:
                self.send_delay = 5
        except Exception:
            # Fallbacks se o arquivo não existir ou falhar
            self.db_path = ""
            self.browser_visible = False
            self.send_delay = 5

        # config.ini for selectors
        config_ini_path = os.path.join(app_dir, "config.ini")
        if os.path.exists(config_ini_path):
            config_ini = IniFile(config_ini_path)
            self.selector_send_btn = config_ini.get_value("ENVIA_MENSAGEM")
        else:
            self.selector_send_btn = '//span[@data-icon="send"]'
            
        self._loaded = True

settings = Settings()
