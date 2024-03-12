import datetime
import locale
import sys


def log(message):
    locale.setlocale(locale.LC_TIME, "")
    timestamp = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    log_message = f"{timestamp}: {message}\n"

    with open("log.txt", "a") as log_file:
        log_file.write(log_message)


def log_and_print(message):
    log(message)
    print(message)


def exit_with_log(message):
    log(message)
    sys.exit(message)
