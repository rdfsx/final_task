import logging
import os

from app.config import Config


def clear_directories():
    for file in os.listdir(Config.DOWNLOADS_PATH):
        if file != 'README.md':
            os.remove(os.path.join(Config.DOWNLOADS_PATH, file))
    logging.info("Directories was cleaned.")
