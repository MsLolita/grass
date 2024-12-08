import asyncio
import ctypes
import os
import random
import sys
import traceback
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog
from design import Ui_MainWindow
import aiohttp
from art import text2art
from imap_tools import MailboxLoginError
from termcolor import colored, cprint
from PySide6.QtCore import QThread, Signal, QUrl, Qt
from PySide6.QtGui import QDesktopServices, QPixmap

from better_proxy import Proxy
from core import Grass
from core.autoreger import AutoReger
from core.utils import logger, file_to_list
from core.utils.logger import logger, logging_setup
from core.utils.accounts_db import AccountsDB
from core.utils.exception import EmailApproveLinkNotFoundException, LoginException, RegistrationException
from core.utils.generate.person import Person

# Пути по умолчанию
DEFAULT_ACCOUNTS_FILE_PATH = 'data/accounts.txt'
DEFAULT_PROXIES_FILE_PATH = 'data/proxies.txt'
DEFAULT_WALLETS_FILE_PATH = 'data/wallets.txt'
DEFAULT_PROXY_DB_PATH = 'data/proxies_stats.db'

from data.config import (
    ACCOUNTS_FILE_PATH, PROXIES_FILE_PATH, REGISTER_ACCOUNT_ONLY, THREADS,
    REGISTER_DELAY, CLAIM_REWARDS_ONLY, APPROVE_EMAIL, APPROVE_WALLET_ON_EMAIL,
    MINING_MODE, CONNECT_WALLET, WALLETS_FILE_PATH, SEND_WALLET_APPROVE_LINK_TO_EMAIL,
    SINGLE_IMAP_ACCOUNT, SEMI_AUTOMATIC_APPROVE_LINK, PROXY_DB_PATH, MIN_PROXY_SCORE,
    EMAIL_FOLDER, IMAP_DOMAIN, STOP_ACCOUNTS_WHEN_SITE_IS_DOWN, CHECK_POINTS,
    TWO_CAPTCHA_API_KEY, ANTICAPTCHA_API_KEY, CAPMONSTER_API_KEY,
    CAPSOLVER_API_KEY, CAPTCHAAI_API_KEY, USE_PROXY_FOR_IMAP, SHOW_LOGS_RARELY, REF_CODE
)

def bot_info(name: str = ""):
    cprint(text2art(name), 'green')
    if sys.platform == 'win32':
        ctypes.windll.kernel32.SetConsoleTitleW(f"{name}")
    print(
        f"{colored('EnJoYeR <crypto/> moves:', color='light_yellow')} "
        f"{colored('https://t.me/+tdC-PXRzhnczNDli', color='light_green')}"
    )

async def worker_task(_id, account: str, proxy: str = None, wallet: str = None, db: AccountsDB = None):
    consumables = account.split(":")[:3]
    imap_pass = None

    if SINGLE_IMAP_ACCOUNT:
        consumables.append(SINGLE_IMAP_ACCOUNT.split(":")[1])

    if len(consumables) == 1:
        email = consumables[0]
        password = Person().random_string(8)
    elif len(consumables) == 2:
        email, password = consumables
    else:
        email, password, imap_pass = consumables

    grass = None

    try:
        grass = Grass(_id, email, password, proxy, db)

        if MINING_MODE:
            await asyncio.sleep(random.uniform(1, 2) * _id)
            logger.info(f"Starting №{_id} | {email} | {password} | {proxy}")
        else:
            await asyncio.sleep(random.uniform(*REGISTER_DELAY))
            logger.info(f"Starting №{_id} | {email} | {password} | {proxy}")

        if REGISTER_ACCOUNT_ONLY:
            await grass.create_account()
        elif APPROVE_EMAIL or CONNECT_WALLET or SEND_WALLET_APPROVE_LINK_TO_EMAIL or APPROVE_WALLET_ON_EMAIL:
            await grass.enter_account()
            user_info = await grass.retrieve_user()

            if APPROVE_EMAIL:
                if user_info['result']['data'].get("isVerified"):
                    logger.info(f"{grass.id} | {grass.email} email already verified!")
                else:
                    if SEMI_AUTOMATIC_APPROVE_LINK:
                        imap_pass = "placeholder"
                    elif imap_pass is None:
                        raise TypeError("IMAP password is not provided")
                    await grass.confirm_email(imap_pass)
            if CONNECT_WALLET:
                if user_info['result']['data'].get("walletAddress"):
                    logger.info(f"{grass.id} | {grass.email} wallet already linked!")
                else:
                    await grass.link_wallet(wallet)

            if user_info['result']['data'].get("isWalletAddressVerified"):
                logger.info(f"{grass.id} | {grass.email} wallet already verified!")
            else:
                if SEND_WALLET_APPROVE_LINK_TO_EMAIL:
                    await grass.send_approve_link(endpoint="sendWalletAddressEmailVerification")
                if APPROVE_WALLET_ON_EMAIL:
                    if SEMI_AUTOMATIC_APPROVE_LINK:
                        imap_pass = "placeholder"
                    elif imap_pass is None:
                        raise TypeError("IMAP password is not provided")
                    await grass.confirm_wallet_by_email(imap_pass)
        elif CLAIM_REWARDS_ONLY:
            await grass.claim_rewards()
        else:
            await grass.start()

        return True
    except (LoginException, RegistrationException) as e:
        error_msg = f"{_id} | {e}"
        logger.warning(error_msg)
        return False
    except MailboxLoginError as e:
        error_msg = f"{_id} | {e}"
        logger.error(error_msg)
        return False
    except EmailApproveLinkNotFoundException as e:
        logger.warning(e)
        return False
    except aiohttp.ClientError as e:
        error_msg = f"{_id} | Some connection error: {e}..."
        logger.warning(error_msg)
        return False
    except Exception as e:
        error_msg = f"{_id} | not handled exception | error: {e}\n{traceback.format_exc()}"
        logger.error(error_msg)
        return False
    finally:
        if grass:
            try:
                await grass.session.close()
            except Exception as e:
                logger.error(f"Error closing session: {e}")

async def main():
    accounts = file_to_list(ACCOUNTS_FILE_PATH)
    if not accounts:
        logger.warning("No accounts found!")
        return

    proxies = [Proxy.from_str(proxy).as_url for proxy in file_to_list(PROXIES_FILE_PATH)]

    if os.path.exists(PROXY_DB_PATH):
        os.remove(PROXY_DB_PATH)

    db = AccountsDB(PROXY_DB_PATH)
    await db.connect()

    for i, account in enumerate(accounts):
        account = account.split(":")[0]
        proxy = proxies[i] if len(proxies) > i else None

        if await db.proxies_exist(proxy) or not proxy:
            continue

        await db.add_account(account, proxy)

    await db.delete_all_from_extra_proxies()
    await db.push_extra_proxies(proxies[len(accounts):])

    autoreger = AutoReger.get_accounts(
        (ACCOUNTS_FILE_PATH, PROXIES_FILE_PATH, WALLETS_FILE_PATH),
        with_id=True,
        static_extra=(db,)
    )

    threads = THREADS if not MINING_MODE else len(autoreger.accounts)

    mode_msg = {
        REGISTER_ACCOUNT_ONLY: "__REGISTER__ MODE",
        APPROVE_EMAIL or CONNECT_WALLET or SEND_WALLET_APPROVE_LINK_TO_EMAIL or APPROVE_WALLET_ON_EMAIL: "__APPROVE__ MODE",
        CLAIM_REWARDS_ONLY: "__CLAIM__ MODE"
    }.get(True, "__MINING__ MODE")

    logger.info(mode_msg)

    await autoreger.start(worker_task, threads)
    await db.close_connection()

class FarmingThread(QThread):
    error = Signal(str)
    finished = Signal()
    account_error = Signal(str)

    def __init__(self):
        super().__init__()
        self.loop = None
        self.should_stop = False
        self.db = None
        self._cleanup_db()

    def _cleanup_db(self):
        """Принудительно очищает соединения с БД"""
        try:
            import sqlite3
            # Закрываем все существующие соединения
            try:
                conn = sqlite3.connect(PROXY_DB_PATH)
                conn.close()
            except:
                pass

            # Пытаемся удалить файл БД
            if os.path.exists(PROXY_DB_PATH):
                try:
                    # На Windows иногда нужно несколько попыток
                    for _ in range(3):
                        try:
                            os.remove(PROXY_DB_PATH)
                            # logger.info("База данных успешно очищена")
                            break
                        except PermissionError:
                            import time
                            time.sleep(0.5)
                except:
                    pass
                    # logger.warning("Не удалось очистить базу данных")

        except Exception as e:
            logger.error(f"Error cleaning up database: {e}")

    async def run_main(self):
        """Запускает main() с проверкой флага остановки"""
        try:
            # Update config first to catch any config errors early
            mining_mode, register_only = update_global_config()
            
            self._cleanup_db()
            self.db = AccountsDB(PROXY_DB_PATH)
            await self.db.connect()

            accounts = file_to_list(ACCOUNTS_FILE_PATH)
            if not accounts:
                error_msg = "No accounts found!"
                logger.warning(error_msg)
                self.error.emit(error_msg)
                return

            proxies = [Proxy.from_str(proxy).as_url for proxy in file_to_list(PROXIES_FILE_PATH)]

            for i, account in enumerate(accounts):
                if self.should_stop:
                    break
                account = account.split(":")[0]
                proxy = proxies[i] if len(proxies) > i else None

                if await self.db.proxies_exist(proxy) or not proxy:
                    continue

                await self.db.add_account(account, proxy)

            if not self.should_stop:
                await self.db.delete_all_from_extra_proxies()
                await self.db.push_extra_proxies(proxies[len(accounts):])

                autoreger = AutoReger.get_accounts(
                    (ACCOUNTS_FILE_PATH, PROXIES_FILE_PATH, WALLETS_FILE_PATH),
                    with_id=True,
                    static_extra=(self.db,)
                )

                if not autoreger:
                    error_msg = "Failed to initialize AutoReger"
                    logger.error(error_msg)
                    self.error.emit(error_msg)
                    return

                threads = THREADS if not MINING_MODE else len(autoreger.accounts)
                mode_msg = {
                    REGISTER_ACCOUNT_ONLY: "__REGISTER__ MODE",
                    APPROVE_EMAIL or CONNECT_WALLET or SEND_WALLET_APPROVE_LINK_TO_EMAIL or APPROVE_WALLET_ON_EMAIL: "__APPROVE__ MODE",
                    CLAIM_REWARDS_ONLY: "__CLAIM__ MODE"
                }.get(True, "__MINING__ MODE")

                logger.info(mode_msg)
                
                # Check captcha API key before starting if in register mode
                if REGISTER_ACCOUNT_ONLY:
                    captcha_key = None
                    for key_name in [TWO_CAPTCHA_API_KEY, ANTICAPTCHA_API_KEY, CAPMONSTER_API_KEY, CAPSOLVER_API_KEY, CAPTCHAAI_API_KEY]:
                        if key_name:
                            captcha_key = key_name
                            break
                    
                    if not captcha_key:
                        error_msg = "No valid captcha solving service API key found"
                        logger.error(error_msg)
                        self.error.emit(error_msg)
                        return

                try:
                    await autoreger.start(worker_task, threads)
                except Exception as e:
                    error_msg = f"Error in autoreger: {str(e)}\n{traceback.format_exc()}"
                    logger.error(error_msg)
                    self.error.emit(error_msg)
                    # Continue execution despite errors

        except Exception as e:
            error_msg = f"Critical error: {str(e)}\n{traceback.format_exc()}"
            logger.error(error_msg)
            self.error.emit(error_msg)
        finally:
            if self.db:
                try:
                    await self.db.close_connection()
                except Exception as e:
                    logger.error(f"Error closing DB connection: {e}")

    def run(self):
        """Запускает асинхронный код в отдельном потоке"""
        try:
            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.loop)
            
            try:
                self.loop.run_until_complete(self.run_main())
            except Exception as e:
                error_msg = f"Error in main loop: {str(e)}"
                logger.error(error_msg)
                self.error.emit(error_msg)
                # Don't re-raise, let the UI continue
        except Exception as e:
            error_msg = f"Thread error: {str(e)}\n{traceback.format_exc()}"
            logger.error(error_msg)
            self.error.emit(error_msg)
        finally:
            if self.loop:
                try:
                    self.loop.close()
                except:
                    pass
            self.finished.emit()

    def stop(self):
        """Корректно останавливает выполнение асинхронных задач"""
        self.should_stop = True
        
        if self.loop and self.loop.is_running():
            for task in asyncio.all_tasks(self.loop):
                task.cancel()
            
            self.loop.call_soon_threadsafe(self.loop.stop)
        
        # Ждем завершения потока максимум 2 секунды
        self.wait(2000)

def update_global_config():
    """Обновляет глобальные переменные из файла конфига"""
    with open('data/config.py', 'r', encoding='utf-8') as file:
        config_content = file.read()
        exec(config_content, globals())
        
    # Обновляем локальные значения API ключей
    if hasattr(globals()['MainApp'], 'local_captcha_keys'):
        for service, param_name in globals()['MainApp'].captcha_services.items():
            globals()['MainApp'].local_captcha_keys[service] = globals().get(param_name, "")
            
    return globals()['MINING_MODE'], globals()['REGISTER_ACCOUNT_ONLY']

class MainApp(QMainWindow):
    def __init__(self):
        super(MainApp, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # Добавим загрузку изображения после setupUi
        try:
            # Загружаем изображение
            pixmap = QPixmap("core/static/image.png")
            if not pixmap.isNull():
                # Устанавливаем изображение в label без масштабирования
                self.ui.label_13.setPixmap(pixmap)
                # Устанавливаем размер label по размеру картинки
                self.ui.label_13.setFixedSize(pixmap.size())
                # Отключаем масштабирование
                self.ui.label_13.setScaledContents(False)
            else:
                logger.error("Failed to load image: image is null")
        except Exception as e:
            logger.error(f"Error loading image: {e}")

        # Добавляем атрибуты для управления задачей
        self.farming_thread = None
        self.is_running = False

        # Настройка логирования для GUI
        logging_setup(gui_mode=True, text_edit=self.ui.textEdit_Log)

        # Устанавлваем первую вкладку активной
        self.ui.tabWidget.setCurrentIndex(0)

        # Связь значений ComboBox с параметрами конфига
        self.captcha_services = {
            "TWO_CAPTCHA": "TWO_CAPTCHA_API_KEY",
            "ANTICAPTCHA": "ANTICAPTCHA_API_KEY",
            "CAPMONSTER": "CAPMONSTER_API_KEY",
            "CAPSOLVER": "CAPSOLVER_API_KEY",
            "CAPTCHAAI": "CAPTCHAAI_API_KEY"
        }

        # Локальное хранилище значений API-ключей
        self.local_captcha_keys = {
            "TWO_CAPTCHA": globals().get("TWO_CAPTCHA_API_KEY", ""),
            "ANTICAPTCHA": globals().get("ANTICAPTCHA_API_KEY", ""),
            "CAPMONSTER": globals().get("CAPMONSTER_API_KEY", ""),
            "CAPSOLVER": globals().get("CAPSOLVER_API_KEY", ""),
            "CAPTCHAAI": globals().get("CAPTCHAAI_API_KEY", "")
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

        # Добавляем подключение кнопки StartFarming
        self.ui.pushButton_StartFarming.clicked.connect(self.toggle_farming)

        # Добавляем подключение кнопки Registration
        self.ui.pushButton_Registration.clicked.connect(self.start_registration)

        # Добавьте эти строки после других подключений кнопок
        self.ui.pushButton_Instructions.clicked.connect(self.open_instructions)
        self.ui.pushButton_more.clicked.connect(self.open_telegram)
        self.ui.pushButton_Web3.clicked.connect(self.open_web3)

        # Initialize thread
        self.farming_thread = None
        self.is_running = False

        # Setup logging for GUI
        logging_setup(gui_mode=True, text_edit=self.ui.textEdit_Log)
        
        # Connect error handlers
        self.setup_error_handlers()
        
        # Rest of initialization...

    def setup_error_handlers(self):
        """Setup error handlers for the UI"""
        if self.farming_thread:
            self.farming_thread.error.connect(self.on_error)
            self.farming_thread.finished.connect(self.on_finished)
            self.farming_thread.account_error.connect(self.on_account_error)

    def on_error(self, error_msg):
        """Handle errors in the UI"""
        logger.error(error_msg)
        # Make sure UI stays responsive
        self.stop_farming()
        # Show error in UI console
        self.ui.textEdit_Log.append(f"ERROR: {error_msg}")
        
    def on_account_error(self, error_msg):
        """Handle individual account errors"""
        logger.warning(error_msg)
        # Show in UI console but don't stop
        self.ui.textEdit_Log.append(f"Account Error: {error_msg}")

    def on_finished(self):
        """Handle thread completion"""
        logger.info("Process completed")
        self.stop_farming()
        self.ui.textEdit_Log.append("Process completed")

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

    def convert_to_bool(self, value):
        if isinstance(value, str):
            return value.lower() == "true"
        return bool(value)

    def update_lineedit_with_local_values(self):
        current_service = self.ui.comboBox_CaptchaService.currentText()
        if current_service in self.local_captcha_keys:
            self.ui.lineEdit_CapthaAPI.setText(self.local_captcha_keys[current_service])

    def update_local_value(self):
        current_service = self.ui.comboBox_CaptchaService.currentText()
        if current_service in self.local_captcha_keys:
            self.local_captcha_keys[current_service] = self.ui.lineEdit_CapthaAPI.text()

    def update_file_path(self, param_name, button):
        file_path, _ = QFileDialog.getOpenFileName(self, "Choose a file", "", "All Files (*)")
        if file_path:
            self.update_config_param(param_name, file_path)
            button.setText(f"Updated: {file_path.split('/')[-1]}")
            logger.info(f"{param_name} updated to {file_path}.")

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
        try:
            min_delay = int(self.ui.lineEdit_Min.text())
            max_delay = int(self.ui.lineEdit_Max.text())
            if min_delay >= 0 and max_delay > min_delay:
                self.update_config_param("REGISTER_DELAY", (min_delay, max_delay))
        except ValueError:
            logger.error("Invalid REGISTER_DELAY.")

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

            # Перезагружаем модуль конфига
            import data.config
            import importlib
            importlib.reload(data.config)
            
            # Обновляем глобальные переменные после сохранения
            update_global_config()
            
            # Обновляем локальные значения API ключей из обновленных глобальных переменных
            for service, param_name in self.captcha_services.items():
                self.local_captcha_keys[service] = globals().get(param_name, "")
                
            logger.info("All parameters saved.")
            
        except Exception as e:
            logger.error(f"Error saving parameters: {e}")

    def toggle_farming(self):
        """Переключает состояние фарминга между запуском и остановкой"""
        if not self.is_running:
            # Обновляем конфиг и проверяем режим
            mining_mode, register_only = update_global_config()
            if not mining_mode or register_only:
                self.update_config_param("MINING_MODE", True)
                self.update_config_param("REGISTER_ACCOUNT_ONLY", False)
                update_global_config()
            self.start_farming()
        else:
            self.stop_farming()

    def start_farming(self):
        """Запускает процесс фарминга"""
        try:
            self.is_running = True
            self.ui.pushButton_StartFarming.setText("Stop Farming")
            
            # Создаем и запускаем поток
            self.farming_thread = FarmingThread()
            self.farming_thread.error.connect(self.on_farming_error)
            self.farming_thread.finished.connect(self.on_farming_finished)
            self.farming_thread.start()
            
        except Exception as e:
            logger.error(f"Error starting mining: {e}")
            self.stop_farming()

    def stop_farming(self):
        """Останавливает процесс фарминга"""
        try:
            if not self.is_running:
                return
                
            self.is_running = False
            self.ui.pushButton_StartFarming.setText("Start Farming")
            
            if self.farming_thread:
                self.farming_thread.stop()
                self.farming_thread.wait()  # Ждем завершения потока
                self.farming_thread = None
                
            logger.info("Mining stopped")
            
        except Exception as e:
            logger.error(f"Error stopping mining: {e}")

    def on_farming_error(self, error_msg):
        """Обработчик ошибок фарминга"""
        logger.error(f"Error in mining: {error_msg}")
        self.stop_farming()

    def on_farming_finished(self):
        """Обработчик завершения фарминга"""
        logger.info("Mining finished")
        self.stop_farming()

    def closeEvent(self, event):
        """Обработчик закрытия окна"""
        try:
            if self.is_running:
                self.stop_farming()
            event.accept()
        except:
            event.accept()

    def start_registration(self):
        """Запускает процесс регистрации"""
        logger.info({CAPMONSTER_API_KEY})
        try:
            # Обновляем конфиг и проверяем режим
            mining_mode, register_only = update_global_config()
            if mining_mode or not register_only:
                self.update_config_param("MINING_MODE", False)
                self.update_config_param("REGISTER_ACCOUNT_ONLY", True)
                update_global_config()
            
            # Если уже запущен процесс - останавливаем его
            if self.is_running:
                self.stop_farming()
            
            # Запускаем процесс регистрации
            self.is_running = True
            self.ui.pushButton_Registration.setText("Stop register")
            self.ui.pushButton_StartFarming.setEnabled(False)
            
            self.farming_thread = FarmingThread()
            self.farming_thread.error.connect(self.on_registration_error)
            self.farming_thread.finished.connect(self.on_registration_finished)
            self.farming_thread.start()
            
        except Exception as e:
            logger.error(f"Error starting registration: {e}")
            self.stop_registration()

    def stop_registration(self):
        """Останавливает процесс регистрации"""
        try:
            if not self.is_running:
                return
                
            self.is_running = False
            self.ui.pushButton_Registration.setText("Start register")
            self.ui.pushButton_StartFarming.setEnabled(True)
            
            if self.farming_thread:
                self.farming_thread.stop()
                self.farming_thread.wait()
                self.farming_thread = None
                
            logger.info("Registration stopped")
            
        except Exception as e:
            logger.error(f"Error stopping registration: {e}")

    def on_registration_error(self, error_msg):
        """Обработчик ошибок регистации"""
        # logger.error(f"Error in registration: {error_msg}")
        self.stop_registration()

    def on_registration_finished(self):
        """Обработчик завершения регистрации"""
        # logger.info("Registration finished")
        self.stop_registration()

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

def start_ui():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec())

#if __name__ == "__main__":
#     start_ui()

