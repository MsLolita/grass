import sys
import re
from datetime import date
from loguru import logger
from PySide6.QtWidgets import QTextEdit
from PySide6.QtGui import QColor


class QTextEditHandler:
    def __init__(self, text_edit: QTextEdit):
        self.text_edit = text_edit

    def write(self, message: str):
        clean_message = clean_brackets(message)
        self.append_colored_message(clean_message)
        scrollbar = self.text_edit.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def append_colored_message(self, message: str):
        # Определяем цвета в зависимости от уровня логирования
        if "ERROR" in message:
            colors = {
                "time": QColor("#00FF00"),  # зеленый
                "level": QColor("#FF0000"),  # красный
                "message": QColor("#FF0000")  # красный
            }
        elif "WARNING" in message:
            colors = {
                "time": QColor("#27e868"),  # зеленый
                "level": QColor("#FFD700"),  # желтый
                "message": QColor("#FFD700")  # желтый
            }
        elif "INFO" in message:
            colors = {
                "time": QColor("#27e868"),  # зеленый
                "level": QColor("#32c2c2"),  # синий
                "message": QColor("#FFFFFF")  # белый
            }
        else:
            colors = {
                "time": QColor("#27e868"),  # зеленый
                "level": QColor("#d137d4"),  # синий
                "message": QColor("#eb811e")  # белый
            }

        # Разделяем сообщение на части
        parts = message.split(" ", 2)
        if len(parts) >= 3:
            time_part, level_part, message_part = parts

            # Добавляем время
            self.text_edit.setTextColor(colors["time"])
            self.text_edit.insertPlainText(time_part + " ")

            # Добавляем уровень
            self.text_edit.setTextColor(colors["level"])
            self.text_edit.insertPlainText(level_part + " ")

            # Добавляем сообщение
            self.text_edit.setTextColor(colors["message"])
            self.text_edit.insertPlainText(message_part + "\n")


def logging_setup(gui_mode=False, text_edit=None):
    format_info = "<green>{time:HH:mm:ss.SS}</green> <blue>{level}</blue> <level>{message}</level>"
    format_error = "<green>{time:HH:mm:ss.SS}</green> <blue>{level}</blue> | " \
                   "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | <level>{message}</level>"
    file_path = r"logs/"

    logger.remove()  # Удаляем все предыдущие обработчики

    if gui_mode and text_edit is not None:
        # В GUI режиме добавляем только один обработчик для QTextEdit
        handler = QTextEditHandler(text_edit)
        logger.add(handler, format=format_info, level="INFO")
    else:
        # В консольном режиме добавляем обработчики для файла и stdout
        logger.add(file_path + f"out_{date.today().strftime('%m-%d')}.log", colorize=True,
                   format=format_info)
        logger.add(sys.stdout, colorize=True, format=format_info, level="INFO")


def clean_brackets(raw_str):
    clean_text = re.sub(brackets_regex, '', raw_str)
    return clean_text


brackets_regex = re.compile(r'<.*?>')

# Пример использования (предполагается, что `text_edit` — это ваш экземпляр QTextEdit):
# logging_setup(gui_mode=True, text_edit=text_edit)
