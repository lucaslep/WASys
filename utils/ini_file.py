import os
import config.globals as globals


class IniFile:
    def __init__(self, ini_path):
        if not os.path.isfile(rf"{ini_path}"):
            raise FileNotFoundError(f"O arquivo ini: {ini_path} não foi encontrado!")

        self.read_ini_file(ini_path)

    def read_ini_file(self, ini_path):
        with open(ini_path, "r", encoding="UTF-8") as ini:
            self.lines = clear_text_lines(ini.readlines())

    def get_value(self, value_name):
        value = ""

        for line in self.lines:
            if value_name in line:
                start_pos = line.find("=") + 1
                value = line[start_pos : len(line)]

                return value


def clear_text_lines(lines):
    return [line.rstrip() for line in lines]
