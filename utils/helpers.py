import re, qrcode, os


class Helpers:
    @staticmethod
    def format_error_message(error_message, replacements):
        return re.sub(
            r"{\d+}",
            lambda match: (
                str(replacements[int(match.group(0)[1:-1])])
                if replacements[int(match.group(0)[1:-1])] is not None
                else match.group(0)
            ),
            error_message,
        )

    @staticmethod
    def decrypt(str):
        str_decrypted = ""

        for char in str:
            str_decrypted = str_decrypted + chr(
                23 ^ ord(bytearray(char, encoding="UTF-8"))
            )

        return str_decrypted

    @staticmethod
    def gen_qrcode_from_string(s: str) -> qrcode:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=5,
            border=4,
        )
        qr.add_data(s)
        qr.make()

        return qr

    @staticmethod
    def clear_terminal():
        if os.name == "nt":
            os.system("cls")
        elif os.name == "posix":
            os.system("clear")
