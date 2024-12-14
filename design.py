# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.8.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QFrame,
    QGridLayout, QGroupBox, QLabel, QLineEdit,
    QMainWindow, QMenuBar, QPushButton, QScrollArea,
    QSizePolicy, QStatusBar, QTabWidget, QTextEdit,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(865, 540)
        MainWindow.setToolTipDuration(-1)
        
        # Устанавливаем иконку окна
        icon = QIcon("core/static/ico.png")
        MainWindow.setWindowIcon(icon)
        
        # Устанавливаем заголовок окна
        MainWindow.setWindowTitle("Grass")
        
        # Устанавливаем фиксированную темную тему
        dark_palette = QPalette()
        dark_palette.setColor(QPalette.Window, QColor(18, 18, 18))
        dark_palette.setColor(QPalette.WindowText, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.Base, QColor(27, 27, 27))
        dark_palette.setColor(QPalette.AlternateBase, QColor(35, 35, 35))
        dark_palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.ToolTipText, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.Text, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.Button, QColor(27, 27, 27))
        dark_palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
        dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))
        
        # Применяем палитру
        MainWindow.setPalette(dark_palette)
        
        # Устанавливаем стиль для всего приложения
        MainWindow.setStyleSheet("""
            QMainWindow {
                background-color: #121212;
            }
            QWidget {
                color: #ffffff;
                background-color: #121212;
            }
            QFrame {
                background-color: #1b1b1b;
                border-radius: 10px;
            }
            QPushButton {
                background-color: #3e2d9f;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #4e3dbf;
            }
            QPushButton:pressed {
                background-color: #2e1d7f;
            }
            QLineEdit {
                background-color: #424242;
                border: none;
                border-radius: 5px;
                padding: 5px;
                color: white;
            }
            QTextEdit {
                background-color: #424242;
                border: none;
                border-radius: 5px;
                padding: 5px;
                color: white;
            }
            QComboBox {
                background-color: #303030;
                border: none;
                border-radius: 5px;
                padding: 5px;
                color: white;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: none;
            }
            QTabWidget::pane {
                border: none;
                background-color: #2d2d2d;
            }
            QTabBar::tab {
                background-color: #2d2d2d;
                color: white;
                padding: 8px 20px;
                border: none;
            }
            QTabBar::tab:selected {
                background-color: #3e2d9f;
            }
            QCheckBox {
                color: white;
            }
            /* Стили для чекбоксов внутри tabWidget */
            QTabWidget QCheckBox::indicator {
                width: 13px;
                height: 13px;
                background-color: transparent;
            }
            QTabWidget QCheckBox::indicator:unchecked {
                background-color: transparent;
                border: 1px solid #ffffff;
            }
            QTabWidget QCheckBox::indicator:checked {
                background-color: transparent;
                border: 1px solid #ffffff;
                image: url(core/static/ico.png);
            }
            /* Стили для остальных чекбоксов */
            QCheckBox::indicator {
                width: 15px;
                height: 15px;
            }
            QCheckBox::indicator:unchecked {
                background-color: #424242;
                border: 2px solid #666666;
                border-radius: 3px;
            }
            QCheckBox::indicator:checked {
                background-color: #3e2d9f;
                border: 2px solid #3e2d9f;
                border-radius: 3px;
            }
        """)

        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_5 = QGridLayout(self.centralwidget)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.label_13 = QLabel(self.centralwidget)
        self.label_13.setObjectName(u"label_13")

        self.gridLayout_5.addWidget(self.label_13, 0, 0, 1, 1)

        self.pushButton_Instructions = QPushButton(self.centralwidget)
        self.pushButton_Instructions.setObjectName(u"pushButton_Instructions")
        font = QFont()
        font.setPointSize(10)
        font.setBold(True)
        self.pushButton_Instructions.setFont(font)
        self.pushButton_Instructions.setStyleSheet(u"background-color: #3e2d9f;")

        self.gridLayout_5.addWidget(self.pushButton_Instructions, 0, 1, 1, 1)

        self.pushButton_more = QPushButton(self.centralwidget)
        self.pushButton_more.setObjectName(u"pushButton_more")
        self.pushButton_more.setFont(font)
        self.pushButton_more.setStyleSheet(u"background-color: #3e2d9f;")

        self.gridLayout_5.addWidget(self.pushButton_more, 0, 2, 1, 1)

        self.pushButton_Web3 = QPushButton(self.centralwidget)
        self.pushButton_Web3.setObjectName(u"pushButton_Web3")
        self.pushButton_Web3.setFont(font)
        self.pushButton_Web3.setStyleSheet(u"background-color: #3e2d9f;")

        self.gridLayout_5.addWidget(self.pushButton_Web3, 0, 3, 1, 1)

        self.frame = QFrame(self.centralwidget)
        self.frame.setObjectName(u"frame")
        self.frame.setStyleSheet(u"background-color: #1b1b1b ;  /* \u0426\u0432\u0435\u0442 \u0444\u043e\u043d\u0430 */\n"
"border-radius: 10px;       /* \u0417\u0430\u043a\u0440\u0443\u0433\u043b\u0435\u043d\u043d\u044b\u0435 \u0443\u0433\u043b\u044b */")
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_4 = QGridLayout(self.frame)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.lineEdit_CapthaAPI = QLineEdit(self.frame)
        self.lineEdit_CapthaAPI.setObjectName(u"lineEdit_CapthaAPI")
        self.lineEdit_CapthaAPI.setFont(font)
        self.lineEdit_CapthaAPI.setStyleSheet(u"border-radius: 5px;       /* \u0417\u0430\u043a\u0440\u0443\u0433\u043b\u0435\u043d\u043d\u044b\u0435 \u0443\u0433\u043b\u044b */\n"
"background-color: #424242;")

        self.gridLayout_3.addWidget(self.lineEdit_CapthaAPI, 0, 4, 1, 2)

        self.lineEdit_Max = QLineEdit(self.frame)
        self.lineEdit_Max.setObjectName(u"lineEdit_Max")
        self.lineEdit_Max.setMinimumSize(QSize(50, 25))
        self.lineEdit_Max.setStyleSheet(u"border-radius: 5px;       /* \u0417\u0430\u043a\u0440\u0443\u0433\u043b\u0435\u043d\u043d\u044b\u0435 \u0443\u0433\u043b\u044b */\n"
"background-color: #424242 ;")

        self.gridLayout_3.addWidget(self.lineEdit_Max, 5, 5, 1, 1)

        self.lineEdit_REFCODE = QLineEdit(self.frame)
        self.lineEdit_REFCODE.setObjectName(u"lineEdit_REFCODE")
        self.lineEdit_REFCODE.setMinimumSize(QSize(50, 25))
        self.lineEdit_REFCODE.setStyleSheet(u"border-radius: 5px;       /* \u0417\u0430\u043a\u0440\u0443\u0433\u043b\u0435\u043d\u043d\u044b\u0435 \u0443\u0433\u043b\u044b */\n"
"background-color: #424242 ;")

        self.gridLayout_3.addWidget(self.lineEdit_REFCODE, 6, 2, 1, 2)

        self.label_Threads = QLabel(self.frame)
        self.label_Threads.setObjectName(u"label_Threads")
        self.label_Threads.setFont(font)

        self.gridLayout_3.addWidget(self.label_Threads, 1, 0, 1, 1)

        self.comboBox_CaptchaService = QComboBox(self.frame)
        self.comboBox_CaptchaService.addItem("")
        self.comboBox_CaptchaService.addItem("")
        self.comboBox_CaptchaService.addItem("")
        self.comboBox_CaptchaService.addItem("")
        self.comboBox_CaptchaService.addItem("")
        self.comboBox_CaptchaService.setObjectName(u"comboBox_CaptchaService")
        font1 = QFont()
        font1.setBold(False)
        font1.setHintingPreference(QFont.PreferDefaultHinting)
        self.comboBox_CaptchaService.setFont(font1)
        self.comboBox_CaptchaService.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.comboBox_CaptchaService.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.comboBox_CaptchaService.setAutoFillBackground(False)
        self.comboBox_CaptchaService.setStyleSheet(u"background-color: #303030 ;\n"
"border-radius: 0px; /* \u0417\u0430\u043a\u0440\u0443\u0433\u043b\u0435\u043d\u043d\u044b\u0435 \u0443\u0433\u043b\u044b */")

        self.gridLayout_3.addWidget(self.comboBox_CaptchaService, 0, 1, 1, 3)

        self.lineEdit_Threads = QLineEdit(self.frame)
        self.lineEdit_Threads.setObjectName(u"lineEdit_Threads")
        self.lineEdit_Threads.setStyleSheet(u"QLineEdit {\n"
"    border-radius: 5px;       /* \u0417\u0430\u043a\u0440\u0443\u0433\u043b\u0435\u043d\u043d\u044b\u0435 \u0443\u0433\u043b\u044b */\n"
"    color: White;              /* \u0426\u0432\u0435\u0442 \u0442\u0435\u043a\u0441\u0442\u0430 */\n"
"	background-color: #424242 ;\n"
"}")

        self.gridLayout_3.addWidget(self.lineEdit_Threads, 1, 1, 1, 3)

        self.label_ImapDomain = QLabel(self.frame)
        self.label_ImapDomain.setObjectName(u"label_ImapDomain")
        self.label_ImapDomain.setFont(font)

        self.gridLayout_3.addWidget(self.label_ImapDomain, 4, 0, 1, 2)

        self.lineEdit_EmailFolder = QLineEdit(self.frame)
        self.lineEdit_EmailFolder.setObjectName(u"lineEdit_EmailFolder")
        self.lineEdit_EmailFolder.setStyleSheet(u"border-radius: 5px;       /* \u0417\u0430\u043a\u0440\u0443\u0433\u043b\u0435\u043d\u043d\u044b\u0435 \u0443\u0433\u043b\u044b */\n"
"background-color: #424242 ;")

        self.gridLayout_3.addWidget(self.lineEdit_EmailFolder, 3, 2, 1, 1)

        self.label_EmailFolder = QLabel(self.frame)
        self.label_EmailFolder.setObjectName(u"label_EmailFolder")
        self.label_EmailFolder.setFont(font)

        self.gridLayout_3.addWidget(self.label_EmailFolder, 3, 0, 1, 2)

        self.label = QLabel(self.frame)
        self.label.setObjectName(u"label")
        self.label.setFont(font)

        self.gridLayout_3.addWidget(self.label, 5, 0, 1, 2)

        self.label_Captcha = QLabel(self.frame)
        self.label_Captcha.setObjectName(u"label_Captcha")
        self.label_Captcha.setFont(font)

        self.gridLayout_3.addWidget(self.label_Captcha, 0, 0, 1, 1)

        self.label_3 = QLabel(self.frame)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setFont(font)

        self.gridLayout_3.addWidget(self.label_3, 6, 0, 1, 2)

        self.label_MinProxiScore = QLabel(self.frame)
        self.label_MinProxiScore.setObjectName(u"label_MinProxiScore")
        self.label_MinProxiScore.setFont(font)

        self.gridLayout_3.addWidget(self.label_MinProxiScore, 2, 0, 1, 2)

        self.lineEdit_MinProxyScore = QLineEdit(self.frame)
        self.lineEdit_MinProxyScore.setObjectName(u"lineEdit_MinProxyScore")
        self.lineEdit_MinProxyScore.setStyleSheet(u"border-radius: 5px;       /* \u0417\u0430\u043a\u0440\u0443\u0433\u043b\u0435\u043d\u043d\u044b\u0435 \u0443\u0433\u043b\u044b */\n"
"background-color: #424242 ;")

        self.gridLayout_3.addWidget(self.lineEdit_MinProxyScore, 2, 2, 1, 1)

        self.lineEdit_ImapDomain = QLineEdit(self.frame)
        self.lineEdit_ImapDomain.setObjectName(u"lineEdit_ImapDomain")
        self.lineEdit_ImapDomain.setStyleSheet(u"border-radius: 5px;       /* \u0417\u0430\u043a\u0440\u0443\u0433\u043b\u0435\u043d\u043d\u044b\u0435 \u0443\u0433\u043b\u044b */\n"
"background-color: #424242 ;")

        self.gridLayout_3.addWidget(self.lineEdit_ImapDomain, 4, 2, 1, 1)

        self.lineEdit_Min = QLineEdit(self.frame)
        self.lineEdit_Min.setObjectName(u"lineEdit_Min")
        self.lineEdit_Min.setMinimumSize(QSize(50, 25))
        self.lineEdit_Min.setStyleSheet(u"border-radius: 5px;       /* \u0417\u0430\u043a\u0440\u0443\u0433\u043b\u0435\u043d\u043d\u044b\u0435 \u0443\u0433\u043b\u044b */\n"
"background-color: #424242 ;")

        self.gridLayout_3.addWidget(self.lineEdit_Min, 5, 2, 1, 1)

        self.label_2 = QLabel(self.frame)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setFont(font)

        self.gridLayout_3.addWidget(self.label_2, 5, 3, 1, 1)


        self.gridLayout_4.addLayout(self.gridLayout_3, 0, 0, 1, 2)

        self.tabWidget = QTabWidget(self.frame)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setStyleSheet(u"background-color: #2d2d2d;")
        self.tabWidget.setTabPosition(QTabWidget.TabPosition.North)
        self.tabWidget.setTabShape(QTabWidget.TabShape.Rounded)
        self.tabWidget.setUsesScrollButtons(True)
        self.tabWidget.setDocumentMode(False)
        self.tabWidget.setTabsClosable(False)
        self.tabWidget.setMovable(True)
        self.tabWidget.setTabBarAutoHide(False)
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.tab.setEnabled(True)
        self.verticalLayout_2 = QVBoxLayout(self.tab)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.scrollArea = QScrollArea(self.tab)
        self.scrollArea.setObjectName(u"scrollArea")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(sizePolicy)
        self.scrollArea.setFrameShape(QFrame.Shape.NoFrame)
        self.scrollArea.setFrameShadow(QFrame.Shadow.Sunken)
        self.scrollArea.setLineWidth(1)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.scrollAreaWidgetContents_2 = QWidget()
        self.scrollAreaWidgetContents_2.setObjectName(u"scrollAreaWidgetContents_2")
        self.scrollAreaWidgetContents_2.setGeometry(QRect(0, 0, 280, 173))
        self.verticalLayout = QVBoxLayout(self.scrollAreaWidgetContents_2)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.checkBox_ApproveEmail = QCheckBox(self.scrollAreaWidgetContents_2)
        self.checkBox_ApproveEmail.setObjectName(u"checkBox_ApproveEmail")
        self.checkBox_ApproveEmail.setFocusPolicy(Qt.FocusPolicy.WheelFocus)
        self.checkBox_ApproveEmail.setContextMenuPolicy(Qt.ContextMenuPolicy.DefaultContextMenu)
        self.checkBox_ApproveEmail.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.checkBox_ApproveEmail.setAutoFillBackground(False)

        self.verticalLayout.addWidget(self.checkBox_ApproveEmail)

        self.checkBox_ConnectWallet = QCheckBox(self.scrollAreaWidgetContents_2)
        self.checkBox_ConnectWallet.setObjectName(u"checkBox_ConnectWallet")
        self.checkBox_ConnectWallet.setFocusPolicy(Qt.FocusPolicy.WheelFocus)
        self.checkBox_ConnectWallet.setContextMenuPolicy(Qt.ContextMenuPolicy.DefaultContextMenu)
        self.checkBox_ConnectWallet.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.checkBox_ConnectWallet.setAutoFillBackground(False)

        self.verticalLayout.addWidget(self.checkBox_ConnectWallet)

        self.checkBox_SendWallerApproveForEmail = QCheckBox(self.scrollAreaWidgetContents_2)
        self.checkBox_SendWallerApproveForEmail.setObjectName(u"checkBox_SendWallerApproveForEmail")
        self.checkBox_SendWallerApproveForEmail.setFocusPolicy(Qt.FocusPolicy.WheelFocus)
        self.checkBox_SendWallerApproveForEmail.setContextMenuPolicy(Qt.ContextMenuPolicy.DefaultContextMenu)
        self.checkBox_SendWallerApproveForEmail.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.checkBox_SendWallerApproveForEmail.setAutoFillBackground(False)

        self.verticalLayout.addWidget(self.checkBox_SendWallerApproveForEmail)

        self.checkBox_ApproveWalletOnEmail = QCheckBox(self.scrollAreaWidgetContents_2)
        self.checkBox_ApproveWalletOnEmail.setObjectName(u"checkBox_ApproveWalletOnEmail")
        self.checkBox_ApproveWalletOnEmail.setFocusPolicy(Qt.FocusPolicy.WheelFocus)
        self.checkBox_ApproveWalletOnEmail.setContextMenuPolicy(Qt.ContextMenuPolicy.DefaultContextMenu)
        self.checkBox_ApproveWalletOnEmail.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.checkBox_ApproveWalletOnEmail.setAutoFillBackground(False)

        self.verticalLayout.addWidget(self.checkBox_ApproveWalletOnEmail)

        self.checkBox_SemiAutoApproveLink = QCheckBox(self.scrollAreaWidgetContents_2)
        self.checkBox_SemiAutoApproveLink.setObjectName(u"checkBox_SemiAutoApproveLink")
        self.checkBox_SemiAutoApproveLink.setFocusPolicy(Qt.FocusPolicy.WheelFocus)
        self.checkBox_SemiAutoApproveLink.setContextMenuPolicy(Qt.ContextMenuPolicy.DefaultContextMenu)
        self.checkBox_SemiAutoApproveLink.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.checkBox_SemiAutoApproveLink.setAutoFillBackground(False)

        self.verticalLayout.addWidget(self.checkBox_SemiAutoApproveLink)

        self.checkBox_SingleMapAccount = QCheckBox(self.scrollAreaWidgetContents_2)
        self.checkBox_SingleMapAccount.setObjectName(u"checkBox_SingleMapAccount")
        self.checkBox_SingleMapAccount.setFocusPolicy(Qt.FocusPolicy.WheelFocus)
        self.checkBox_SingleMapAccount.setContextMenuPolicy(Qt.ContextMenuPolicy.DefaultContextMenu)
        self.checkBox_SingleMapAccount.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.checkBox_SingleMapAccount.setAutoFillBackground(False)

        self.verticalLayout.addWidget(self.checkBox_SingleMapAccount)

        self.checkBox_UseProxyForImap = QCheckBox(self.scrollAreaWidgetContents_2)
        self.checkBox_UseProxyForImap.setObjectName(u"checkBox_UseProxyForImap")
        self.checkBox_UseProxyForImap.setFocusPolicy(Qt.FocusPolicy.WheelFocus)
        self.checkBox_UseProxyForImap.setContextMenuPolicy(Qt.ContextMenuPolicy.DefaultContextMenu)
        self.checkBox_UseProxyForImap.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.checkBox_UseProxyForImap.setAutoFillBackground(False)

        self.verticalLayout.addWidget(self.checkBox_UseProxyForImap)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents_2)

        self.verticalLayout_2.addWidget(self.scrollArea)

        self.tabWidget.addTab(self.tab, "")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.checkBox_TimeOutFarm = QCheckBox(self.tab_3)
        self.checkBox_TimeOutFarm.setObjectName(u"checkBox_TimeOutFarm")
        self.checkBox_TimeOutFarm.setGeometry(QRect(20, 20, 111, 22))
        font2 = QFont()
        font2.setBold(False)
        self.checkBox_TimeOutFarm.setFont(font2)
        self.checkBox_CheckPoints = QCheckBox(self.tab_3)
        self.checkBox_CheckPoints.setObjectName(u"checkBox_CheckPoints")
        self.checkBox_CheckPoints.setGeometry(QRect(20, 40, 101, 22))
        self.checkBox_CheckPoints.setFont(font2)
        self.checkBox_RarelyShowLogs = QCheckBox(self.tab_3)
        self.checkBox_RarelyShowLogs.setObjectName(u"checkBox_RarelyShowLogs")
        self.checkBox_RarelyShowLogs.setGeometry(QRect(20, 60, 121, 22))
        self.checkBox_RarelyShowLogs.setFont(font2)
        self.tabWidget.addTab(self.tab_3, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.checkBox_ClaimRewardOnly = QCheckBox(self.tab_2)
        self.checkBox_ClaimRewardOnly.setObjectName(u"checkBox_ClaimRewardOnly")
        self.checkBox_ClaimRewardOnly.setGeometry(QRect(10, 20, 161, 21))
        self.checkBox_ClaimRewardOnly.setFocusPolicy(Qt.FocusPolicy.WheelFocus)
        self.checkBox_ClaimRewardOnly.setContextMenuPolicy(Qt.ContextMenuPolicy.DefaultContextMenu)
        self.checkBox_ClaimRewardOnly.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.checkBox_ClaimRewardOnly.setAutoFillBackground(False)
        self.tabWidget.addTab(self.tab_2, "")

        self.gridLayout_4.addWidget(self.tabWidget, 0, 2, 1, 1)

        self.groupBox_2 = QGroupBox(self.frame)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setStyleSheet(u"background-color: #2d2d2d;\n"
"border-radius: 5px;       /* \u0417\u0430\u043a\u0440\u0443\u0433\u043b\u0435\u043d\u043d\u044b\u0435 \u0443\u0433\u043b\u044b */")
        self.gridLayout = QGridLayout(self.groupBox_2)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_AccountFile = QLabel(self.groupBox_2)
        self.label_AccountFile.setObjectName(u"label_AccountFile")
        self.label_AccountFile.setFont(font)

        self.gridLayout.addWidget(self.label_AccountFile, 1, 0, 1, 1)

        self.pushButton_WalletsFile = QPushButton(self.groupBox_2)
        self.pushButton_WalletsFile.setObjectName(u"pushButton_WalletsFile")
        font3 = QFont()
        font3.setFamilies([u"Arial"])
        font3.setBold(True)
        font3.setItalic(False)
        font3.setUnderline(False)
        font3.setKerning(False)
        self.pushButton_WalletsFile.setFont(font3)
        self.pushButton_WalletsFile.setStyleSheet(u"QPushButton {\n"
"    background-color: #3498db;  /* \u0426\u0432\u0435\u0442 \u0444\u043e\u043d\u0430 */\n"
"    color: black;              /* \u0426\u0432\u0435\u0442 \u0442\u0435\u043a\u0441\u0442\u0430 */\n"
"    border-radius: 10px;       /* \u0417\u0430\u043a\u0440\u0443\u0433\u043b\u0435\u043d\u043d\u044b\u0435 \u0443\u0433\u043b\u044b */\n"
"    border: 2px solid #2980b9; /* \u0413\u0440\u0430\u043d\u0438\u0446\u0430 \u043a\u043d\u043e\u043f\u043a\u0438 */\n"
"    font-size: 14px;           /* \u0420\u0430\u0437\u043c\u0435\u0440 \u0442\u0435\u043a\u0441\u0442\u0430 */\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #2980b9; /* \u0426\u0432\u0435\u0442 \u0444\u043e\u043d\u0430 \u043f\u0440\u0438 \u043d\u0430\u0432\u0435\u0434\u0435\u043d\u0438\u0438 */\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #1abc9c; /* \u0426\u0432\u0435\u0442 \u0444\u043e\u043d\u0430 \u043f\u0440\u0438 \u043d\u0430\u0436\u0430\u0442\u0438\u0438 */\n"
"}\n"
"")

        self.gridLayout.addWidget(self.pushButton_WalletsFile, 3, 2, 1, 1)

        self.label_6 = QLabel(self.groupBox_2)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setFont(font)

        self.gridLayout.addWidget(self.label_6, 2, 0, 1, 1)

        self.pushButton_AccountsFile = QPushButton(self.groupBox_2)
        self.pushButton_AccountsFile.setObjectName(u"pushButton_AccountsFile")
        font4 = QFont()
        font4.setFamilies([u"Arial"])
        font4.setBold(True)
        font4.setItalic(False)
        font4.setUnderline(False)
        font4.setKerning(False)
        self.pushButton_AccountsFile.setFont(font4)
        self.pushButton_AccountsFile.setAutoFillBackground(False)
        self.pushButton_AccountsFile.setStyleSheet(u"QPushButton {\n"
"    background-color: #3498db;  /* \u0426\u0432\u0435\u0442 \u0444\u043e\u043d\u0430 */\n"
"    color: black;              /* \u0426\u0432\u0435\u0442 \u0442\u0435\u043a\u0441\u0442\u0430 */\n"
"    border-radius: 10px;       /* \u0417\u0430\u043a\u0440\u0443\u0433\u043b\u0435\u043d\u043d\u044b\u0435 \u0443\u0433\u043b\u044b */\n"
"    border: 2px solid #2980b9; /* \u0413\u0440\u0430\u043d\u0438\u0446\u0430 \u043a\u043d\u043e\u043f\u043a\u0438 */\n"
"    font-size: 14px;           /* \u0420\u0430\u0437\u043c\u0435\u0440 \u0442\u0435\u043a\u0441\u0442\u0430 */\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #2980b9; /* \u0426\u0432\u0435\u0442 \u0444\u043e\u043d\u0430 \u043f\u0440\u0438 \u043d\u0430\u0432\u0435\u0434\u0435\u043d\u0438\u0438 */\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #1abc9c; /* \u0426\u0432\u0435\u0442 \u0444\u043e\u043d\u0430 \u043f\u0440\u0438 \u043d\u0430\u0436\u0430\u0442\u0438\u0438 */\n"
"}\n"
"")

        self.gridLayout.addWidget(self.pushButton_AccountsFile, 1, 2, 1, 1)

        self.pushButton_ProxyFile = QPushButton(self.groupBox_2)
        self.pushButton_ProxyFile.setObjectName(u"pushButton_ProxyFile")
        self.pushButton_ProxyFile.setFont(font3)
        self.pushButton_ProxyFile.setStyleSheet(u"QPushButton {\n"
"    background-color: #3498db;  /* \u0426\u0432\u0435\u0442 \u0444\u043e\u043d\u0430 */\n"
"    color: black;              /* \u0426\u0432\u0435\u0442 \u0442\u0435\u043a\u0441\u0442\u0430 */\n"
"    border-radius: 10px;       /* \u0417\u0430\u043a\u0440\u0443\u0433\u043b\u0435\u043d\u043d\u044b\u0435 \u0443\u0433\u043b\u044b */\n"
"    border: 2px solid #2980b9; /* \u0413\u0440\u0430\u043d\u0438\u0446\u0430 \u043a\u043d\u043e\u043f\u043a\u0438 */\n"
"    font-size: 14px;           /* \u0420\u0430\u0437\u043c\u0435\u0440 \u0442\u0435\u043a\u0441\u0442\u0430 */\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #2980b9; /* \u0426\u0432\u0435\u0442 \u0444\u043e\u043d\u0430 \u043f\u0440\u0438 \u043d\u0430\u0432\u0435\u0434\u0435\u043d\u0438\u0438 */\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #1abc9c; /* \u0426\u0432\u0435\u0442 \u0444\u043e\u043d\u0430 \u043f\u0440\u0438 \u043d\u0430\u0436\u0430\u0442\u0438\u0438 */\n"
"}\n"
"")

        self.gridLayout.addWidget(self.pushButton_ProxyFile, 2, 2, 1, 1)

        self.label_7 = QLabel(self.groupBox_2)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setFont(font)

        self.gridLayout.addWidget(self.label_7, 3, 0, 1, 1)

        self.pushButton_Default = QPushButton(self.groupBox_2)
        self.pushButton_Default.setObjectName(u"pushButton_Default")
        self.pushButton_Default.setStyleSheet(u"QPushButton {\n"
"    background-color: #424242 ;\n"
"    border-radius: 5px; /* \u0417\u0430\u043a\u0440\u0443\u0433\u043b\u0435\u043d\u043d\u044b\u0435 \u0443\u0433\u043b\u044b */\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #595959; /* \u0426\u0432\u0435\u0442 \u0444\u043e\u043d\u0430 \u043f\u0440\u0438 \u043d\u0430\u0432\u0435\u0434\u0435\u043d\u0438\u0438 */\n"
"}")

        self.gridLayout.addWidget(self.pushButton_Default, 0, 0, 1, 1)

        self.pushButton_ProxyDB = QPushButton(self.groupBox_2)
        self.pushButton_ProxyDB.setObjectName(u"pushButton_ProxyDB")
        self.pushButton_ProxyDB.setFont(font3)
        self.pushButton_ProxyDB.setStyleSheet(u"QPushButton {\n"
"    background-color: #3498db;  /* \u0426\u0432\u0435\u0442 \u0444\u043e\u043d\u0430 */\n"
"    color: black;              /* \u0426\u0432\u0435\u0442 \u0442\u0435\u043a\u0441\u0442\u0430 */\n"
"    border-radius: 10px;       /* \u0417\u0430\u043a\u0440\u0443\u0433\u043b\u0435\u043d\u043d\u044b\u0435 \u0443\u0433\u043b\u044b */\n"
"    border: 2px solid #2980b9; /* \u0413\u0440\u0430\u043d\u0438\u0446\u0430 \u043a\u043d\u043e\u043f\u043a\u0438 */\n"
"    font-size: 14px;           /* \u0420\u0430\u0437\u043c\u0435\u0440 \u0442\u0435\u043a\u0441\u0442\u0430 */\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #2980b9; /* \u0426\u0432\u0435\u0442 \u0444\u043e\u043d\u0430 \u043f\u0440\u0438 \u043d\u0430\u0432\u0435\u0434\u0435\u043d\u0438\u0438 */\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #1abc9c; /* \u0426\u0432\u0435\u0442 \u0444\u043e\u043d\u0430 \u043f\u0440\u0438 \u043d\u0430\u0436\u0430\u0442\u0438\u0438 */\n"
"}\n"
"")

        self.gridLayout.addWidget(self.pushButton_ProxyDB, 4, 2, 1, 1)

        self.label_8 = QLabel(self.groupBox_2)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setFont(font)

        self.gridLayout.addWidget(self.label_8, 4, 0, 1, 1)


        self.gridLayout_4.addWidget(self.groupBox_2, 0, 3, 1, 1)

        self.pushButton_StartFarming = QPushButton(self.frame)
        self.pushButton_StartFarming.setObjectName(u"pushButton_StartFarming")
        font5 = QFont()
        font5.setFamilies([u"Arial"])
        font5.setPointSize(13)
        font5.setBold(True)
        font5.setItalic(False)
        font5.setUnderline(False)
        self.pushButton_StartFarming.setFont(font5)
        self.pushButton_StartFarming.setStyleSheet(u"QPushButton {\n"
"    background-color: #3b4fac;\n"
"    border-radius: 5px; /* \u0417\u0430\u043a\u0440\u0443\u0433\u043b\u0435\u043d\u043d\u044b\u0435 \u0443\u0433\u043b\u044b */\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #30418c; /* \u0426\u0432\u0435\u0442 \u0444\u043e\u043d\u0430 \u043f\u0440\u0438 \u043d\u0430\u0432\u0435\u0434\u0435\u043d\u0438\u0438 */\n"
"}")

        self.gridLayout_4.addWidget(self.pushButton_StartFarming, 1, 0, 1, 1)

        self.pushButton_Registration = QPushButton(self.frame)
        self.pushButton_Registration.setObjectName(u"pushButton_Registration")
        self.pushButton_Registration.setFont(font5)
        self.pushButton_Registration.setStyleSheet(u"QPushButton {\n"
"    background-color: #3b4fac;\n"
"    border-radius: 5px; /* \u0417\u0430\u043a\u0440\u0443\u0433\u043b\u0435\u043d\u043d\u044b\u0435 \u0443\u0433\u043b\u044b */\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #30418c; /* \u0426\u0432\u0435\u0442 \u0444\u043e\u043d\u0430 \u043f\u0440\u0438 \u043d\u0430\u0432\u0435\u0434\u0435\u043d\u0438\u0438 */\n"
"}")

        self.gridLayout_4.addWidget(self.pushButton_Registration, 1, 1, 1, 1)

        self.textEdit_Log = QTextEdit(self.frame)
        self.textEdit_Log.setObjectName(u"textEdit_Log")
        self.textEdit_Log.setStyleSheet(u"background-color: #424242 ;\n"
"border-radius: 5px;       /* \u0417\u0430\u043a\u0440\u0443\u0433\u043b\u0435\u043d\u043d\u044b\u0435 \u0443\u0433\u043b\u044b */")

        self.gridLayout_4.addWidget(self.textEdit_Log, 2, 0, 1, 5)

        self.pushButton_Save = QPushButton(self.frame)
        self.pushButton_Save.setObjectName(u"pushButton_Save")
        self.pushButton_Save.setStyleSheet(u"QPushButton {\n"
"    background-color: #424242 ;\n"
"    border-radius: 5px; /* \u0417\u0430\u043a\u0440\u0443\u0433\u043b\u0435\u043d\u043d\u044b\u0435 \u0443\u0433\u043b\u044b */\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #595959; /* \u0426\u0432\u0435\u0442 \u0444\u043e\u043d\u0430 \u043f\u0440\u0438 \u043d\u0430\u0432\u0435\u0434\u0435\u043d\u0438\u0438 */\n"
"}")

        self.gridLayout_4.addWidget(self.pushButton_Save, 1, 3, 1, 1)


        self.gridLayout_5.addWidget(self.frame, 1, 0, 1, 4)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 865, 21))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Grass", None))
#if QT_CONFIG(tooltip)
        MainWindow.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.label_13.setText("")
        self.pushButton_Instructions.setText(QCoreApplication.translate("MainWindow", u"Instructions", None))
        self.pushButton_more.setText(QCoreApplication.translate("MainWindow", u"Grass, Dawn, Gradient and more ...", None))
        self.pushButton_Web3.setText(QCoreApplication.translate("MainWindow", u"Web3 products", None))
        self.lineEdit_CapthaAPI.setPlaceholderText(QCoreApplication.translate("MainWindow", u"\u0412\u0432\u0435\u0434\u0438\u0442\u0435 API Key", None))
#if QT_CONFIG(tooltip)
        self.label_Threads.setToolTip(QCoreApplication.translate("MainWindow", u"for register account / claim rewards mode / approve email mode", None))
#endif // QT_CONFIG(tooltip)
        self.label_Threads.setText(QCoreApplication.translate("MainWindow", u"Threads:", None))
        self.comboBox_CaptchaService.setItemText(0, QCoreApplication.translate("MainWindow", u"TWO_CAPTCHA", None))
        self.comboBox_CaptchaService.setItemText(1, QCoreApplication.translate("MainWindow", u"ANTICAPTCHA", None))
        self.comboBox_CaptchaService.setItemText(2, QCoreApplication.translate("MainWindow", u"CAPMONSTER", None))
        self.comboBox_CaptchaService.setItemText(3, QCoreApplication.translate("MainWindow", u"CAPSOLVER", None))
        self.comboBox_CaptchaService.setItemText(4, QCoreApplication.translate("MainWindow", u"CAPTCHAAI", None))

        self.comboBox_CaptchaService.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Capthca service", None))
#if QT_CONFIG(tooltip)
        self.label_ImapDomain.setToolTip(QCoreApplication.translate("MainWindow", u"imap server domain (example: imap.firstmail.ltd for firstmail)", None))
#endif // QT_CONFIG(tooltip)
        self.label_ImapDomain.setText(QCoreApplication.translate("MainWindow", u"Imap Domain:", None))
#if QT_CONFIG(tooltip)
        self.label_EmailFolder.setToolTip(QCoreApplication.translate("MainWindow", u"folder where mails comes (example: SPAM INBOX JUNK etc.)", None))
#endif // QT_CONFIG(tooltip)
        self.label_EmailFolder.setText(QCoreApplication.translate("MainWindow", u"Email Folder:", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Register Delay:", None))
        self.label_Captcha.setText(QCoreApplication.translate("MainWindow", u"Capthca:", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"REF_CODE:", None))
#if QT_CONFIG(tooltip)
        self.label_MinProxiScore.setToolTip(QCoreApplication.translate("MainWindow", u"Put MIN_PROXY_SCORE = 0 not to check proxy score (if site is down)", None))
#endif // QT_CONFIG(tooltip)
        self.label_MinProxiScore.setText(QCoreApplication.translate("MainWindow", u"Min Proxy Score:", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"to", None))
#if QT_CONFIG(tooltip)
        self.checkBox_ApproveEmail.setToolTip(QCoreApplication.translate("MainWindow", u"approve email (NEEDED IMAP AND ACCESS TO EMAIL)", None))
#endif // QT_CONFIG(tooltip)
        self.checkBox_ApproveEmail.setText(QCoreApplication.translate("MainWindow", u"Approve Email", None))
#if QT_CONFIG(tooltip)
        self.checkBox_ConnectWallet.setToolTip(QCoreApplication.translate("MainWindow", u"connect wallet (put private keys in wallets.txt)", None))
#endif // QT_CONFIG(tooltip)
        self.checkBox_ConnectWallet.setText(QCoreApplication.translate("MainWindow", u"Connect Wallet", None))
#if QT_CONFIG(tooltip)
        self.checkBox_SendWallerApproveForEmail.setToolTip(QCoreApplication.translate("MainWindow", u"send approve link to email", None))
#endif // QT_CONFIG(tooltip)
        self.checkBox_SendWallerApproveForEmail.setText(QCoreApplication.translate("MainWindow", u"Send Wallet Approve Link To Email", None))
#if QT_CONFIG(tooltip)
        self.checkBox_ApproveWalletOnEmail.setToolTip(QCoreApplication.translate("MainWindow", u"get approve link from email (NEEDED IMAP AND ACCESS TO EMAIL)", None))
#endif // QT_CONFIG(tooltip)
        self.checkBox_ApproveWalletOnEmail.setText(QCoreApplication.translate("MainWindow", u"Approve Wallet On Email", None))
#if QT_CONFIG(tooltip)
        self.checkBox_SemiAutoApproveLink.setToolTip(QCoreApplication.translate("MainWindow", u"if on - allow to manual paste approve link from email to cli", None))
#endif // QT_CONFIG(tooltip)
        self.checkBox_SemiAutoApproveLink.setText(QCoreApplication.translate("MainWindow", u"Semi Auto Approve Link", None))
#if QT_CONFIG(tooltip)
        self.checkBox_SingleMapAccount.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><pre style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; background-color:#1e1f22;\"><span style=\" font-family:'JetBrains Mono','monospace'; color:#eaf2ff;\">If you have possibility to forward all approve mails to single IMAP address:</span></pre><pre style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; background-color:#1e1f22;\"><span style=\" font-family:'JetBrains Mono','monospace'; color:#eaf2ff;\">usage &quot;name@domain.com:password&quot;</span></pre></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.checkBox_SingleMapAccount.setText(QCoreApplication.translate("MainWindow", u"Single Imap Account", None))
#if QT_CONFIG(tooltip)
        self.checkBox_UseProxyForImap.setToolTip(QCoreApplication.translate("MainWindow", u"Use proxy also for mail handling", None))
#endif // QT_CONFIG(tooltip)
        self.checkBox_UseProxyForImap.setText(QCoreApplication.translate("MainWindow", u"Use Proxy For Imap", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"Reg. Settings", None))
#if QT_CONFIG(tooltip)
        self.checkBox_TimeOutFarm.setToolTip(QCoreApplication.translate("MainWindow", u"stop account for 20 minutes, to reduce proxy traffic usage", None))
#endif // QT_CONFIG(tooltip)
        self.checkBox_TimeOutFarm.setText(QCoreApplication.translate("MainWindow", u"Time Out Farm", None))
#if QT_CONFIG(tooltip)
        self.checkBox_CheckPoints.setToolTip(QCoreApplication.translate("MainWindow", u"show point for each account every nearly 10 minutes", None))
#endif // QT_CONFIG(tooltip)
        self.checkBox_CheckPoints.setText(QCoreApplication.translate("MainWindow", u"Check Points", None))
#if QT_CONFIG(tooltip)
        self.checkBox_RarelyShowLogs.setToolTip(QCoreApplication.translate("MainWindow", u"not always show info about actions to decrease pc influence", None))
#endif // QT_CONFIG(tooltip)
        self.checkBox_RarelyShowLogs.setText(QCoreApplication.translate("MainWindow", u"Rarely Show Logs", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QCoreApplication.translate("MainWindow", u"Farm", None))
#if QT_CONFIG(tooltip)
        self.checkBox_ClaimRewardOnly.setToolTip(QCoreApplication.translate("MainWindow", u"claim tiers rewards only (https://app.getgrass.io/dashboard/referral-program)", None))
#endif // QT_CONFIG(tooltip)
        self.checkBox_ClaimRewardOnly.setText(QCoreApplication.translate("MainWindow", u"Claim Reward ONLY", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"Rewards", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"Files", None))
        self.label_AccountFile.setText(QCoreApplication.translate("MainWindow", u"Accounsts File", None))
        self.pushButton_WalletsFile.setText(QCoreApplication.translate("MainWindow", u"Click", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Proxies FIile", None))
        self.pushButton_AccountsFile.setText(QCoreApplication.translate("MainWindow", u"Click", None))
        self.pushButton_ProxyFile.setText(QCoreApplication.translate("MainWindow", u"Click", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"WALLETS_FILE", None))
        self.pushButton_Default.setText(QCoreApplication.translate("MainWindow", u"Default", None))
        self.pushButton_ProxyDB.setText(QCoreApplication.translate("MainWindow", u"Click", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"PROXY_DB", None))
        self.pushButton_StartFarming.setText(QCoreApplication.translate("MainWindow", u"Start Farming", None))
        self.pushButton_Registration.setText(QCoreApplication.translate("MainWindow", u"Reg", None))
        self.textEdit_Log.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Logs...", None))
        self.pushButton_Save.setText(QCoreApplication.translate("MainWindow", u"Save", None))
    # retranslateUi

