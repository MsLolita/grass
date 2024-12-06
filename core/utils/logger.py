import sys
import re
from datetime import date
from loguru import logger


class QTextBrowserHandler:
    """
    Логер для вывода сообщений в QTextBrowser.
    """

    def __init__(self, text_browser):
        self.text_browser = text_browser

    def write(self, message):
        clean_message = clean_brackets(message)
        self.text_browser.append(clean_message)
        # Автоматическая прокрутка после добавления сообщения
        scrollbar = self.text_browser.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def flush(self):
        pass  # Метод flush не требуется


def logging_setup(gui_mode=False, text_browser=None):
    """
    Настройка логирования с учётом GUI.
    :param gui_mode: Если True, логи выводятся в textBrowser_Log.
    :param text_browser: Экземпляр QTextBrowser для GUI.
    """
    format_info = "<green>{time:HH:mm:ss.SS}</green> <blue>{level}</blue> <level>{message}</level>"
    format_error = "<green>{time:HH:mm:ss.SS}</green> <blue>{level}</blue> | " \
                   "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | <level>{message}</level>"
    file_path = r"logs/"

    logger.remove()  # Удаляем все предыдущие обработчики
    # if sys.platform == "win32":

    if gui_mode and text_browser is not None:
        # Логирование в файл
        logger.add(file_path + f"out_{date.today().strftime('%m-%d')}.log", colorize=True,
                   format=format_info)

        # Логирование в QTextBrowser
        handler = QTextBrowserHandler(text_browser)
        logger.add(handler, format=format_info, level="INFO")
    else:
        # Логирование в консоль
        logger.add(file_path + f"out_{date.today().strftime('%m-%d')}.log", colorize=True,
                   format=format_info)

        logger.add(sys.stdout, colorize=True,
                   format=format_info, level="INFO")


def clean_brackets(raw_str):
    """
    Убирает HTML-теги из строки.
    """
    clean_text = re.sub(brackets_regex, '', raw_str)
    return clean_text


brackets_regex = re.compile(r'<.*?>')
logging_setup()
