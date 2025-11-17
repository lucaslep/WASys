from utils.ini_file import IniFile

class SelectorsRepository:
    def __init__(self, config_path='config.ini'):
        self.ini = IniFile(config_path)

    def get_selector(self, selector_name):
        value = self.ini.get_value(selector_name)
        if not value:
            raise ValueError(f"Seletor '{selector_name}' não encontrado ou vazio no config.ini")
        return value

selectors_repository = SelectorsRepository()
