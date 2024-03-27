import logging


def setup_logger():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("main")

    file_handler = logging.FileHandler("logfile.log")
    file_handler.setLevel(logging.ERROR)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    log_formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s:\n%(message)s\n", datefmt="%d/%m/%Y %H:%M:%S"
    )
    file_handler.setFormatter(log_formatter)

    console_formatter = logging.Formatter(
        "%(levelname)s - %(asctime)s - %(message)s", datefmt="%H:%M:%S"
    )
    console_handler.setFormatter(console_formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    logger.propagate = False
