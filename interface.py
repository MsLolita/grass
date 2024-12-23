import os
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog
from PySide6.QtGui import QDesktopServices, QPixmap
from design import Ui_MainWindow
from core.utils.logger import logging_setup, logger
import importlib
import asyncio
import json
from data.config import (
    ACCOUNTS_FILE_PATH, PROXIES_FILE_PATH, REGISTER_ACCOUNT_ONLY, THREADS,
    REGISTER_DELAY, CLAIM_REWARDS_ONLY, APPROVE_EMAIL, APPROVE_WALLET_ON_EMAIL,
    MINING_MODE, CONNECT_WALLET, WALLETS_FILE_PATH, SEND_WALLET_APPROVE_LINK_TO_EMAIL,
    SINGLE_IMAP_ACCOUNT, SEMI_AUTOMATIC_APPROVE_LINK, PROXY_DB_PATH, MIN_PROXY_SCORE,
    EMAIL_FOLDER, IMAP_DOMAIN, STOP_ACCOUNTS_WHEN_SITE_IS_DOWN, CHECK_POINTS,
    TWO_CAPTCHA_API_KEY, ANTICAPTCHA_API_KEY, CAPMONSTER_API_KEY,
    CAPSOLVER_API_KEY, CAPTCHAAI_API_KEY, USE_PROXY_FOR_IMAP, SHOW_LOGS_RARELY, REF_CODE,
    NODE_TYPE
)
from PySide6.QtCore import QThread, Signal, QUrl
from main import main

# Пути по умолчанию
DEFAULT_ACCOUNTS_FILE_PATH = 'data/accounts.txt'
DEFAULT_PROXIES_FILE_PATH = 'data/proxies.txt'
DEFAULT_WALLETS_FILE_PATH = 'data/wallets.txt'
DEFAULT_PROXY_DB_PATH = 'data/proxies_stats.db'



class AsyncWorker(QThread):
    finished = Signal()
    error = Signal(str)
    stopped = Signal()


    def __init__(self, parent=None):
        super().__init__(parent)
        self.is_running = False
        self.loop = None
        
    def stop(self):
        """Безопасная остановка воркера"""
        self.is_running = False
        if self.loop and self.loop.is_running():
            try:
                # Отменяем все задачи в текущем loop
                for task in asyncio.all_tasks(self.loop):
                    task.cancel()
                self.stopped.emit()
            except Exception as e:
                logger.error(f"Ошибка при остановке: {e}")
                self.terminate()  # Принудительная остановка в случае ошибки
        
    def run(self):
        try:
            self.is_running = True
            
            if sys.platform == 'win32':
                asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.loop)
            
            try:
                self.loop.run_until_complete(main())
                if self.is_running:
                    self.finished.emit()
            except asyncio.CancelledError:
                logger.info("Процесс был остановлен пользователем")
                self.stopped.emit()
            except Exception as e:
                if self.is_running:
                    self.error.emit(str(e))
                    logger.error(f"Ошибка: {e}")
            finally:
                try:
                    if self.loop and self.loop.is_running():
                        self.loop.stop()
                    if self.loop:
                        self.loop.close()
                except:
                    pass
                self.loop = None
        finally:
            self.is_running = False


def update_global_config():
    """Обновляет глобальные переменные из файла конфига"""
    try:
        # Принудительно перечитываем файл конфига
        with open('data/config.py', 'r', encoding='utf-8') as file:
            config_content = file.read()

        # Создаем новое пространство имен для выполнения конфига
        config_globals = {}
        exec(config_content, config_globals)

        # Обновляем глобальные переменные в текущем моуле
        for key, value in config_globals.items():
            if not key.startswith('__'):
                globals()[key] = value

        # Обновляем локальные значения API ключей если они существуют
        if hasattr(globals().get('MainApp', None), 'local_captcha_keys'):
            for service, param_name in globals()['MainApp'].captcha_services.items():
                globals()['MainApp'].local_captcha_keys[service] = config_globals.get(param_name, "")

        return config_globals.get('MINING_MODE', False), config_globals.get('REGISTER_ACCOUNT_ONLY', False)

    except Exception as e:
        logger.error(f"Error updating global config: {e}")
        return False, False


#mining_mode, register_only = update_global_config()
class GrassInterface(QMainWindow):
    def __init__(self):
        super(GrassInterface, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # Инициализация логгера
        logging_setup(gui_mode=True, text_edit=self.ui.textEdit_Log)
        mining_mode, register_only = update_global_config()

        # Добавим обработку ошибок при загрузке изображения
        try:
            # Установка иконки окна
            self.setWindowTitle("Grass")
            window_icon = QPixmap("core/static/ico.png")
            if not window_icon.isNull():
                self.setWindowIcon(window_icon)
            else:
                logger.error("Failed to load window icon: icon is null")
        
            # Загрузка основного изображения
            pixmap = QPixmap("core/static/image.png")
            if not pixmap.isNull():
                self.ui.label_13.setPixmap(pixmap)
                self.ui.label_13.setFixedSize(pixmap.size())
                self.ui.label_13.setScaledContents(False)
            else:
                logger.error("Failed to load image: image is null")
        except Exception as e:
            logger.error(f"Error loading images: {e}")
        
        # Словарь для хранения API ключей
        self.local_captcha_keys = {
            "TWO_CAPTCHA": TWO_CAPTCHA_API_KEY,
            "ANTICAPTCHA": ANTICAPTCHA_API_KEY,
            "CAPMONSTER": CAPMONSTER_API_KEY,
            "CAPSOLVER": CAPSOLVER_API_KEY,
            "CAPTCHAAI": CAPTCHAAI_API_KEY
        }
        
        # Связь значений ComboBox с параметрами конфига
        self.captcha_services = {
            "TWO_CAPTCHA": "TWO_CAPTCHA_API_KEY",
            "ANTICAPTCHA": "ANTICAPTCHA_API_KEY",
            "CAPMONSTER": "CAPMONSTER_API_KEY",
            "CAPSOLVER": "CAPSOLVER_API_KEY",
            "CAPTCHAAI": "CAPTCHAAI_API_KEY"
        }
        
        # Сохраняем начальные значения параметров
        self.initial_params = {
            'THREADS': THREADS,
            'MIN_PROXY_SCORE': MIN_PROXY_SCORE,
            'EMAIL_FOLDER': EMAIL_FOLDER,
            'IMAP_DOMAIN': IMAP_DOMAIN,
            'REGISTER_DELAY': REGISTER_DELAY,
            'APPROVE_EMAIL': APPROVE_EMAIL,
            'CONNECT_WALLET': CONNECT_WALLET,
            'SEND_WALLET_APPROVE_LINK_TO_EMAIL': SEND_WALLET_APPROVE_LINK_TO_EMAIL,
            'APPROVE_WALLET_ON_EMAIL': APPROVE_WALLET_ON_EMAIL,
            'SEMI_AUTOMATIC_APPROVE_LINK': SEMI_AUTOMATIC_APPROVE_LINK,
            'SINGLE_IMAP_ACCOUNT': SINGLE_IMAP_ACCOUNT,
            'USE_PROXY_FOR_IMAP': USE_PROXY_FOR_IMAP,
            'STOP_ACCOUNTS_WHEN_SITE_IS_DOWN': STOP_ACCOUNTS_WHEN_SITE_IS_DOWN,
            'CHECK_POINTS': CHECK_POINTS,
            'SHOW_LOGS_RARELY': SHOW_LOGS_RARELY,
            'CLAIM_REWARDS_ONLY': CLAIM_REWARDS_ONLY,
            'REF_CODE': REF_CODE,
            'NODE_TYPE': NODE_TYPE,
        }
        
        # Инициализация полей
        self.ui.lineEdit_Threads.setText(str(THREADS))
        self.ui.lineEdit_MinProxyScore.setText(str(MIN_PROXY_SCORE))
        self.ui.lineEdit_EmailFolder.setText(EMAIL_FOLDER)
        self.ui.lineEdit_ImapDomain.setText(IMAP_DOMAIN)
        self.ui.lineEdit_REFCODE.setText(REF_CODE)
        self.ui.lineEdit_Min.setText(str(REGISTER_DELAY[0]))
        self.ui.lineEdit_Max.setText(str(REGISTER_DELAY[1]))

        # Конвертируем булевы значения из config в Python-формат
        '''Tab1'''
        self.ui.checkBox_ApproveEmail.setChecked(self.convert_to_bool(APPROVE_EMAIL))
        self.ui.checkBox_ConnectWallet.setChecked(self.convert_to_bool(CONNECT_WALLET))
        self.ui.checkBox_SendWallerApproveForEmail.setChecked(self.convert_to_bool(SEND_WALLET_APPROVE_LINK_TO_EMAIL))
        self.ui.checkBox_ApproveWalletOnEmail.setChecked(self.convert_to_bool(APPROVE_WALLET_ON_EMAIL))
        self.ui.checkBox_SemiAutoApproveLink.setChecked(self.convert_to_bool(SEMI_AUTOMATIC_APPROVE_LINK))
        self.ui.checkBox_SingleMapAccount.setChecked(self.convert_to_bool(SINGLE_IMAP_ACCOUNT))
        self.ui.checkBox_UseProxyForImap.setChecked(self.convert_to_bool(USE_PROXY_FOR_IMAP))
        '''Tab2'''
        self.ui.checkBox_TimeOutFarm.setChecked(self.convert_to_bool(STOP_ACCOUNTS_WHEN_SITE_IS_DOWN))
        self.ui.checkBox_CheckPoints.setChecked(self.convert_to_bool(CHECK_POINTS))
        self.ui.checkBox_RarelyShowLogs.setChecked(self.convert_to_bool(SHOW_LOGS_RARELY))
        '''Tab3'''
        self.ui.checkBox_ClaimRewardOnly.setChecked(self.convert_to_bool(CLAIM_REWARDS_ONLY))

        # Очистка comboBox и добавление начений
        self.ui.comboBox_CaptchaService.clear()
        self.ui.comboBox_CaptchaService.addItems(self.captcha_services.keys())

        # Установка текущего значения lineEdit_CapthaAPI
        self.update_lineedit_with_local_values()

        # Подключение событий
        self.ui.pushButton_Save.clicked.connect(self.save_changes)
        self.ui.comboBox_CaptchaService.currentTextChanged.connect(self.update_lineedit_with_local_values)
        self.ui.lineEdit_CapthaAPI.textChanged.connect(self.update_local_value)

        # Привязка кнопок к функции изменения путей
        self.ui.pushButton_AccountsFile.clicked.connect(
            lambda: self.update_file_path("ACCOUNTS_FILE_PATH", self.ui.pushButton_AccountsFile)
        )
        self.ui.pushButton_ProxyFile.clicked.connect(
            lambda: self.update_file_path("PROXIES_FILE_PATH", self.ui.pushButton_ProxyFile)
        )
        self.ui.pushButton_WalletsFile.clicked.connect(
            lambda: self.update_file_path("WALLETS_FILE_PATH", self.ui.pushButton_WalletsFile)
        )
        self.ui.pushButton_ProxyDB.clicked.connect(
            lambda: self.update_file_path("PROXY_DB_PATH", self.ui.pushButton_ProxyDB)
        )

        # Привязка кнопки Default
        self.ui.pushButton_Default.clicked.connect(self.reset_to_default)

        # Привязка изменений REGISTER_DELAY
        self.ui.lineEdit_Min.textChanged.connect(self.update_register_delay)
        self.ui.lineEdit_Max.textChanged.connect(self.update_register_delay)

        # Подключение основных кнопок
        self.ui.pushButton_StartFarming.clicked.connect(self.start_farming)
        self.ui.pushButton_Registration.clicked.connect(self.start_registration)

        # Подключение информационных кнопок
        self.ui.pushButton_Instructions.clicked.connect(self.open_instructions)
        self.ui.pushButton_more.clicked.connect(self.open_telegram)
        self.ui.pushButton_Web3.clicked.connect(self.open_web3)

        # Подключаем обработчик изменения NODE_TYPE
        self.ui.comboBox_NODE_TYPE.currentTextChanged.connect(self.update_node_type)
        
        # Устанавливаем текущее значение NODE_TYPE
        self.set_initial_node_type()

        self.worker = None
        self.is_farming = False


    def update_file_path(self, param_name, button):
        file_path, _ = QFileDialog.getOpenFileName(self, "Choose a file", "", "All Files (*)")
        if file_path:
            self.update_config_param(param_name, file_path)
            button.setText(f"Updated: {file_path.split('/')[-1]}")
            logger.info(f"{param_name} updated to {file_path}.")

    def update_config_param(self, param_name, value):
        try:
            with open('data/config.py', 'r', encoding='utf-8') as file:
                lines = file.readlines()

            with open('data/config.py', 'w', encoding='utf-8') as file:
                for line in lines:
                    if line.startswith(param_name):
                        if isinstance(value, str):
                            file.write(f"{param_name} = '{value}'\n")
                        elif isinstance(value, bool):
                            file.write(f"{param_name} = {str(value)}\n")
                        elif isinstance(value, tuple):
                            file.write(f"{param_name} = {value}\n")
                        else:
                            file.write(f"{param_name} = {value}\n")
                    else:
                        file.write(line)
            logger.info(f"Parameter {param_name} changed to {value}.")
        except Exception as e:
            logger.error(f"Error updating parameter {param_name}: {e}")

    def save_changes(self):
        try:
            params_to_save = {
                'THREADS': int(self.ui.lineEdit_Threads.text()),
                'MIN_PROXY_SCORE': int(self.ui.lineEdit_MinProxyScore.text()),
                'EMAIL_FOLDER': self.ui.lineEdit_EmailFolder.text(),
                'IMAP_DOMAIN': self.ui.lineEdit_ImapDomain.text(),
                'REF_CODE': self.ui.lineEdit_REFCODE.text(),
                'REGISTER_DELAY': (
                    int(self.ui.lineEdit_Min.text()),
                    int(self.ui.lineEdit_Max.text())
                ),
                'APPROVE_EMAIL': self.ui.checkBox_ApproveEmail.isChecked(),
                'CONNECT_WALLET': self.ui.checkBox_ConnectWallet.isChecked(),
                'SEND_WALLET_APPROVE_LINK_TO_EMAIL': self.ui.checkBox_SendWallerApproveForEmail.isChecked(),
                'APPROVE_WALLET_ON_EMAIL': self.ui.checkBox_ApproveWalletOnEmail.isChecked(),
                'SINGLE_IMAP_ACCOUNT': self.ui.checkBox_SingleMapAccount.isChecked(),
                'USE_PROXY_FOR_IMAP': self.ui.checkBox_UseProxyForImap.isChecked(),
                'STOP_ACCOUNTS_WHEN_SITE_IS_DOWN': self.ui.checkBox_TimeOutFarm.isChecked(),
                'CHECK_POINTS': self.ui.checkBox_CheckPoints.isChecked(),
                'SHOW_LOGS_RARELY': self.ui.checkBox_RarelyShowLogs.isChecked(),
                'CLAIM_REWARDS_ONLY': self.ui.checkBox_ClaimRewardOnly.isChecked(),
            }

            # Сохраняем основные параметры
            for param_name, new_value in params_to_save.items():
                old_value = self.initial_params.get(param_name)
                if old_value != new_value:
                    self.update_config_param(param_name, new_value)
                    logger.info(f"{param_name} updated from {old_value} to {new_value}.")
                    self.initial_params[param_name] = new_value

            # Сохраняем API ключи капчи
            for service, param_name in self.captcha_services.items():
                api_key_value = self.local_captcha_keys[service]
                old_value = globals().get(param_name)
                if old_value != api_key_value:
                    self.update_config_param(param_name, api_key_value)
                    # Обновляем глобальную переменную сразу после сохранения
                    globals()[param_name] = api_key_value
                    logger.info(f"API-key for {service} updated to {api_key_value}.")

            # Принудительно перезагружаем все модули, которые могут использовать конфиг
            modules_to_reload = [
                'data.config',
                'core.grass',
                'core.autoreger',
                'core.utils.captcha_service'
            ]

            for module_name in modules_to_reload:
                try:
                    module = sys.modules.get(module_name)
                    if module:
                        importlib.reload(module)
                except Exception as e:
                    logger.error(f"Error reloading module {module_name}: {e}")

            # Обновляем глобальные переменные
            update_global_config()

            # Очищаем кэш импортов для модулей
            importlib.invalidate_caches()

            logger.info("All parameters saved and modules reloaded.")

        except Exception as e:
            logger.error(f"Error saving parameters: {e}")

    def log(self, message):
        logger.info(message)

    def start_farming(self):
        try:
            if self.is_farming:
                # Останавливаем процесс
                if self.worker:
                    logger.info("Остановка фарминга...")
                    self.worker.stop()
                    self.ui.pushButton_StartFarming.setEnabled(False)
                return

            # Проверяем и очищаем старый воркер если он есть
            if self.worker:
                self.worker.quit()
                self.worker.wait()
                self.worker = None

            # Запускаем процесс
            self.save_changes()
            logger.info("Запуск фарминга...")

            self.worker = AsyncWorker(self)
            self.worker.finished.connect(self.on_worker_finished)
            self.worker.error.connect(self.on_worker_error)
            self.worker.stopped.connect(self.on_worker_stopped)
            self.worker.start()

            self.ui.pushButton_StartFarming.setText("Stop Farming")
            self.is_farming = True

        except Exception as e:
            logger.error(f"Ошибка при запуске фарминга: {e}")
            self.ui.pushButton_StartFarming.setText("Start Farming")
            self.is_farming = False

    def start_registration(self):
        self.save_changes()
        logger.info("Запуск регистрации...")
        # Здесь добавить логику запуска регистрации

    def show_instructions(self):
        logger.info("Открытие инструкций...")
        # Добавить логику показа инструкций

    def show_more_info(self):
        logger.info("Открытие дополнительной информации...")
        # Добавить логику показа дополнительной информации

    def show_web3_info(self):
        logger.info("Открытие информации о Web3...")
        # Добавить логику показа информации о Web3

    def convert_to_bool(self, value):
        if isinstance(value, str):
            return value.lower() == "true"
        return bool(value)

    def on_worker_finished(self):
        logger.info("Операция успешно завершена")
        self.ui.pushButton_StartFarming.setText("Start Farming")
        self.is_farming = False

    def on_worker_error(self, error_msg):
        logger.error(f"Ошибка при выполнении: {error_msg}")
        self.ui.pushButton_StartFarming.setText("Start Farming")
        self.is_farming = False

    def on_worker_stopped(self):
        """Обработчи�� успешной остановки воркера"""
        logger.info("Фарминг успешно остановлен")
        self.ui.pushButton_StartFarming.setText("Start Farming")
        self.ui.pushButton_StartFarming.setEnabled(True)
        self.is_farming = False
        if self.worker:
            self.worker.quit()
            self.worker.wait()
            self.worker = None  # Очищаем ссылку на старый воркер

    def update_lineedit_with_local_values(self):
        current_service = self.ui.comboBox_CaptchaService.currentText()
        if current_service in self.local_captcha_keys:
            self.ui.lineEdit_CapthaAPI.setText(self.local_captcha_keys[current_service])

    def update_local_value(self):
        current_service = self.ui.comboBox_CaptchaService.currentText()
        if current_service in self.local_captcha_keys:
            self.local_captcha_keys[current_service] = self.ui.lineEdit_CapthaAPI.text()

    def reset_to_default(self):
        default_paths = {
            "ACCOUNTS_FILE_PATH": DEFAULT_ACCOUNTS_FILE_PATH,
            "PROXIES_FILE_PATH": DEFAULT_PROXIES_FILE_PATH,
            "WALLETS_FILE_PATH": DEFAULT_WALLETS_FILE_PATH,
            "PROXY_DB_PATH": DEFAULT_PROXY_DB_PATH,
        }

        for param_name, default_path in default_paths.items():
            self.update_config_param(param_name, default_path)
            self.initial_params[param_name] = default_path
            logger.info(f"{param_name} updated to {default_path}.")

        self.ui.pushButton_AccountsFile.setText(f"{DEFAULT_ACCOUNTS_FILE_PATH.split('/')[-1]}")
        self.ui.pushButton_ProxyFile.setText(f"{DEFAULT_PROXIES_FILE_PATH.split('/')[-1]}")
        self.ui.pushButton_WalletsFile.setText(f"{DEFAULT_WALLETS_FILE_PATH.split('/')[-1]}")
        self.ui.pushButton_ProxyDB.setText(f"{DEFAULT_PROXY_DB_PATH.split('/')[-1]}")

    def update_register_delay(self):
        """Обновляет значения REGISTER_DELAY при изменении полей Min и Max"""
        try:
            min_delay = float(self.ui.lineEdit_Min.text())
            max_delay = float(self.ui.lineEdit_Max.text())
            if min_delay >= 0 and max_delay > min_delay:
                global REGISTER_DELAY
                REGISTER_DELAY = (min_delay, max_delay)
                logger.info(f"REGISTER_DELAY обновлен: {REGISTER_DELAY}")
            else:
                logger.error("Некорректные значения задержки. Max должен быть больше Min, и Min должен быть >= 0")
        except ValueError:
            logger.error("Ошибка: введите корректные чиловые значения для задержки")

    def open_instructions(self):
        """Открывает инструкции в браузере"""
        QDesktopServices.openUrl(QUrl("https://teletype.in/@c6zr7/grass_for_EnJoYeR"))
        logger.info("Opening instructions page...")

    def open_telegram(self):
        """Открывает Telegram канал"""
        QDesktopServices.openUrl(QUrl("https://t.me/web3_enjoyer_club"))
        logger.info("Opening Telegram channel...")

    def open_web3(self):
        """Открывает Web3 продукты"""
        QDesktopServices.openUrl(QUrl("https://gemups.com/"))
        logger.info("Opening Web3 products page...")

    def set_initial_node_type(self):
        """Устанавливает начальное значение comboBox в соответствии с конфигом"""
        node_type_map = {
            "1x": "1x",
            "1.25x": "1_25x",
            "2x": "2x"
        }
        
        # Получаем текущее значение из конфига и находим соответствующий индекс
        current_value = NODE_TYPE.replace(".", "_") if NODE_TYPE else "1x"
        index = self.ui.comboBox_NODE_TYPE.findText(current_value)
        if index >= 0:
            self.ui.comboBox_NODE_TYPE.setCurrentIndex(index)

    def update_node_type(self):
        """Обновляет NODE_TYPE при изменении значения в comboBox"""
        node_type_map = {
            "1x": "1x",
            "1_25x": "1.25x",
            "2x": "2x"
        }
        
        selected_value = self.ui.comboBox_NODE_TYPE.currentText()
        new_value = node_type_map.get(selected_value, "1x")
        
        try:
            self.update_config_param('NODE_TYPE', new_value)
            self.initial_params['NODE_TYPE'] = new_value
            logger.info(f"NODE_TYPE updated to {new_value}")
        except Exception as e:
            logger.error(f"Error updating NODE_TYPE: {e}")

def start_ui():
    app = QApplication(sys.argv)
    window = GrassInterface()
    window.show()
    sys.exit(app.exec())
