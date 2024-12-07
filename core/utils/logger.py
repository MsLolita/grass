import sys
import re
from datetime import date
from loguru import logger


class QTextEditHandler:
    def __init__(self, text_edit):
        self.text_edit = text_edit

    def write(self, message):
        clean_message = clean_brackets(message)
        self.text_edit.append(clean_message)
        scrollbar = self.text_edit.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())


def logging_setup(gui_mode=False, text_edit=None):
    format_info = "<green>{time:HH:mm:ss.SS}</green> <blue>{level}</blue> <level>{message}</level>"
    format_error = "<green>{time:HH:mm:ss.SS}</green> <blue>{level}</blue> | " \
                   "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | <level>{message}</level>"
    file_path = r"logs/"

    logger.remove()  # Удаляем все предыдущие обработчики
    # if sys.platform == "win32":

    if gui_mode and text_edit is not None:
        logger.add(file_path + f"out_{date.today().strftime('%m-%d')}.log", colorize=True,
                   format=format_info)

        handler = QTextEditHandler(text_edit)
        logger.add(handler, format=format_info, level="INFO")
    else:
        logger.add(file_path + f"out_{date.today().strftime('%m-%d')}.log", colorize=True,
                   format=format_info)

        logger.add(sys.stdout, colorize=True,
                   format=format_info, level="INFO")


def clean_brackets(raw_str):
    clean_text = re.sub(brackets_regex, '', raw_str)
    return clean_text


brackets_regex = re.compile(r'<.*?>')
logging_setup()
