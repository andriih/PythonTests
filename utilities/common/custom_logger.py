import inspect
import logging
import os

from datetime import datetime


class CustomLogger(logging.Filter):

    @staticmethod
    def log():
        logger_name = inspect.stack()[4].function
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.DEBUG)

        if not logger.handlers:
            console_handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(funcName)s - %(levelname)s: %(message)s',
                                          datefmt='%m/%d/%Y %I:%M:%S %p')
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)

            base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
            log_dir = os.path.join(base_dir, "logs")
            log_file_name = datetime.utcnow().strftime('%Y-%m-%d_%H-%M') + "-logs" + ".log"
            log_path = log_dir + "/" + log_file_name

            file_handler = logging.FileHandler(log_path)
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

        return logger
