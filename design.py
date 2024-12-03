# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.8.0
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
    QSizePolicy, QStatusBar, QTabWidget, QTextBrowser,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1300, 700)
        MainWindow.setMinimumSize(QSize(1300, 700))
        MainWindow.setMaximumSize(QSize(1300, 700))
        MainWindow.setToolTipDuration(-1)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.textBrowser_Log = QTextBrowser(self.centralwidget)
        self.textBrowser_Log.setObjectName(u"textBrowser_Log")
        self.textBrowser_Log.setGeometry(QRect(20, 360, 1261, 311))
        self.lineEdit_CapthaAPI = QLineEdit(self.centralwidget)
        self.lineEdit_CapthaAPI.setObjectName(u"lineEdit_CapthaAPI")
        self.lineEdit_CapthaAPI.setGeometry(QRect(190, 13, 191, 25))
        font = QFont()
        font.setPointSize(10)
        font.setBold(True)
        self.lineEdit_CapthaAPI.setFont(font)
        self.label_Captcha = QLabel(self.centralwidget)
        self.label_Captcha.setObjectName(u"label_Captcha")
        self.label_Captcha.setGeometry(QRect(11, 13, 53, 17))
        self.label_Captcha.setFont(font)
        self.comboBox_CaptchaService = QComboBox(self.centralwidget)
        self.comboBox_CaptchaService.addItem("")
        self.comboBox_CaptchaService.addItem("")
        self.comboBox_CaptchaService.addItem("")
        self.comboBox_CaptchaService.addItem("")
        self.comboBox_CaptchaService.addItem("")
        self.comboBox_CaptchaService.setObjectName(u"comboBox_CaptchaService")
        self.comboBox_CaptchaService.setGeometry(QRect(70, 13, 114, 24))
        self.pushButton_Registration = QPushButton(self.centralwidget)
        self.pushButton_Registration.setObjectName(u"pushButton_Registration")
        self.pushButton_Registration.setGeometry(QRect(160, 320, 121, 31))
        font1 = QFont()
        font1.setFamilies([u"Arial"])
        font1.setPointSize(13)
        font1.setBold(True)
        font1.setItalic(False)
        font1.setUnderline(False)
        self.pushButton_Registration.setFont(font1)
        self.groupBox_2 = QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setGeometry(QRect(930, 10, 271, 261))
        self.gridLayout = QGridLayout(self.groupBox_2)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_8 = QLabel(self.groupBox_2)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setFont(font)

        self.gridLayout.addWidget(self.label_8, 4, 0, 1, 1)

        self.pushButton_ProxyFile = QPushButton(self.groupBox_2)
        self.pushButton_ProxyFile.setObjectName(u"pushButton_ProxyFile")
        font2 = QFont()
        font2.setFamilies([u"Arial"])
        font2.setBold(True)
        font2.setItalic(False)
        font2.setUnderline(False)
        self.pushButton_ProxyFile.setFont(font2)
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

        self.pushButton_AccountsFile = QPushButton(self.groupBox_2)
        self.pushButton_AccountsFile.setObjectName(u"pushButton_AccountsFile")
        font3 = QFont()
        font3.setFamilies([u"Arial"])
        font3.setBold(True)
        font3.setItalic(False)
        font3.setUnderline(False)
        font3.setKerning(False)
        self.pushButton_AccountsFile.setFont(font3)
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

        self.label_6 = QLabel(self.groupBox_2)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setFont(font)

        self.gridLayout.addWidget(self.label_6, 2, 0, 1, 1)

        self.pushButton_WalletsFile = QPushButton(self.groupBox_2)
        self.pushButton_WalletsFile.setObjectName(u"pushButton_WalletsFile")
        self.pushButton_WalletsFile.setFont(font2)
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

        self.label_7 = QLabel(self.groupBox_2)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setFont(font)

        self.gridLayout.addWidget(self.label_7, 3, 0, 1, 1)

        self.label_AccountFile = QLabel(self.groupBox_2)
        self.label_AccountFile.setObjectName(u"label_AccountFile")
        self.label_AccountFile.setFont(font)

        self.gridLayout.addWidget(self.label_AccountFile, 1, 0, 1, 1)

        self.pushButton_ProxyDB = QPushButton(self.groupBox_2)
        self.pushButton_ProxyDB.setObjectName(u"pushButton_ProxyDB")
        self.pushButton_ProxyDB.setFont(font2)
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

        self.pushButton_Default = QPushButton(self.groupBox_2)
        self.pushButton_Default.setObjectName(u"pushButton_Default")

        self.gridLayout.addWidget(self.pushButton_Default, 0, 0, 1, 1)

        self.pushButton_StartFarming = QPushButton(self.centralwidget)
        self.pushButton_StartFarming.setObjectName(u"pushButton_StartFarming")
        self.pushButton_StartFarming.setGeometry(QRect(20, 320, 131, 31))
        self.pushButton_StartFarming.setFont(font1)
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setGeometry(QRect(630, 10, 271, 261))
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
        self.scrollAreaWidgetContents_2.setGeometry(QRect(0, 0, 249, 213))
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
        font4 = QFont()
        font4.setBold(False)
        self.checkBox_TimeOutFarm.setFont(font4)
        self.checkBox_CheckPoints = QCheckBox(self.tab_3)
        self.checkBox_CheckPoints.setObjectName(u"checkBox_CheckPoints")
        self.checkBox_CheckPoints.setGeometry(QRect(20, 40, 101, 22))
        self.checkBox_CheckPoints.setFont(font4)
        self.checkBox_RarelyShowLogs = QCheckBox(self.tab_3)
        self.checkBox_RarelyShowLogs.setObjectName(u"checkBox_RarelyShowLogs")
        self.checkBox_RarelyShowLogs.setGeometry(QRect(20, 60, 121, 22))
        self.checkBox_RarelyShowLogs.setFont(font4)
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
        self.label_MinProxiScore = QLabel(self.centralwidget)
        self.label_MinProxiScore.setObjectName(u"label_MinProxiScore")
        self.label_MinProxiScore.setGeometry(QRect(16, 79, 104, 17))
        self.label_MinProxiScore.setFont(font)
        self.lineEdit_MinProxyScore = QLineEdit(self.centralwidget)
        self.lineEdit_MinProxyScore.setObjectName(u"lineEdit_MinProxyScore")
        self.lineEdit_MinProxyScore.setGeometry(QRect(126, 79, 108, 24))
        self.label_EmailFolder = QLabel(self.centralwidget)
        self.label_EmailFolder.setObjectName(u"label_EmailFolder")
        self.label_EmailFolder.setGeometry(QRect(16, 109, 82, 17))
        self.label_EmailFolder.setFont(font)
        self.label_ImapDomain = QLabel(self.centralwidget)
        self.label_ImapDomain.setObjectName(u"label_ImapDomain")
        self.label_ImapDomain.setGeometry(QRect(16, 139, 88, 17))
        self.label_ImapDomain.setFont(font)
        self.lineEdit_EmailFolder = QLineEdit(self.centralwidget)
        self.lineEdit_EmailFolder.setObjectName(u"lineEdit_EmailFolder")
        self.lineEdit_EmailFolder.setGeometry(QRect(126, 109, 108, 24))
        self.lineEdit_ImapDomain = QLineEdit(self.centralwidget)
        self.lineEdit_ImapDomain.setObjectName(u"lineEdit_ImapDomain")
        self.lineEdit_ImapDomain.setGeometry(QRect(126, 139, 108, 24))
        self.lineEdit_Threads = QLineEdit(self.centralwidget)
        self.lineEdit_Threads.setObjectName(u"lineEdit_Threads")
        self.lineEdit_Threads.setGeometry(QRect(70, 44, 41, 24))
        self.lineEdit_Threads.setStyleSheet(u"QLineEdit {\n"
"    border-radius: 10px;       /* \u0417\u0430\u043a\u0440\u0443\u0433\u043b\u0435\u043d\u043d\u044b\u0435 \u0443\u0433\u043b\u044b */\n"
"    background-color: #cca2ff;  /* \u0426\u0432\u0435\u0442 \u0444\u043e\u043d\u0430 */\n"
"    color: black;              /* \u0426\u0432\u0435\u0442 \u0442\u0435\u043a\u0441\u0442\u0430 */\n"
"}")
        self.label_Threads = QLabel(self.centralwidget)
        self.label_Threads.setObjectName(u"label_Threads")
        self.label_Threads.setGeometry(QRect(11, 44, 53, 17))
        self.label_Threads.setFont(font)
        self.pushButton_Save = QPushButton(self.centralwidget)
        self.pushButton_Save.setObjectName(u"pushButton_Save")
        self.pushButton_Save.setGeometry(QRect(1210, 30, 80, 24))
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(16, 169, 93, 17))
        self.label.setFont(font)
        self.lineEdit_Min = QLineEdit(self.centralwidget)
        self.lineEdit_Min.setObjectName(u"lineEdit_Min")
        self.lineEdit_Min.setGeometry(QRect(127, 170, 50, 25))
        self.lineEdit_Min.setMinimumSize(QSize(50, 25))
        self.lineEdit_Max = QLineEdit(self.centralwidget)
        self.lineEdit_Max.setObjectName(u"lineEdit_Max")
        self.lineEdit_Max.setGeometry(QRect(183, 170, 50, 25))
        self.lineEdit_Max.setMinimumSize(QSize(50, 25))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1300, 21))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
#if QT_CONFIG(tooltip)
        MainWindow.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.textBrowser_Log.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Log...", None))
        self.lineEdit_CapthaAPI.setPlaceholderText(QCoreApplication.translate("MainWindow", u"\u0412\u0432\u0435\u0434\u0438\u0442\u0435 API Key", None))
        self.label_Captcha.setText(QCoreApplication.translate("MainWindow", u"Capthca:", None))
        self.comboBox_CaptchaService.setItemText(0, QCoreApplication.translate("MainWindow", u"TWO_CAPTCHA", None))
        self.comboBox_CaptchaService.setItemText(1, QCoreApplication.translate("MainWindow", u"ANTICAPTCHA", None))
        self.comboBox_CaptchaService.setItemText(2, QCoreApplication.translate("MainWindow", u"CAPMONSTER", None))
        self.comboBox_CaptchaService.setItemText(3, QCoreApplication.translate("MainWindow", u"CAPSOLVER", None))
        self.comboBox_CaptchaService.setItemText(4, QCoreApplication.translate("MainWindow", u"CAPTCHAAI", None))

        self.comboBox_CaptchaService.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Capthca service", None))
        self.pushButton_Registration.setText(QCoreApplication.translate("MainWindow", u"Reg", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"Files", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"PROXY_DB", None))
        self.pushButton_ProxyFile.setText(QCoreApplication.translate("MainWindow", u"Click", None))
        self.pushButton_AccountsFile.setText(QCoreApplication.translate("MainWindow", u"Click", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Proxies FIile", None))
        self.pushButton_WalletsFile.setText(QCoreApplication.translate("MainWindow", u"Click", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"WALLETS_FILE", None))
        self.label_AccountFile.setText(QCoreApplication.translate("MainWindow", u"Accounsts File", None))
        self.pushButton_ProxyDB.setText(QCoreApplication.translate("MainWindow", u"Click", None))
        self.pushButton_Default.setText(QCoreApplication.translate("MainWindow", u"Default", None))
        self.pushButton_StartFarming.setText(QCoreApplication.translate("MainWindow", u"Start Farming", None))
        self.checkBox_ApproveEmail.setText(QCoreApplication.translate("MainWindow", u"Approve Email", None))
        self.checkBox_ConnectWallet.setText(QCoreApplication.translate("MainWindow", u"Connect Wallet", None))
        self.checkBox_SendWallerApproveForEmail.setText(QCoreApplication.translate("MainWindow", u"Send Wallet Approve Link To Email", None))
        self.checkBox_ApproveWalletOnEmail.setText(QCoreApplication.translate("MainWindow", u"Approve Wallet On Email", None))
        self.checkBox_SemiAutoApproveLink.setText(QCoreApplication.translate("MainWindow", u"Semi Auto Approve Link", None))
#if QT_CONFIG(tooltip)
        self.checkBox_SingleMapAccount.setToolTip(QCoreApplication.translate("MainWindow", u"name@domain.com:password", None))
#endif // QT_CONFIG(tooltip)
        self.checkBox_SingleMapAccount.setText(QCoreApplication.translate("MainWindow", u"Single Imap Account", None))
        self.checkBox_UseProxyForImap.setText(QCoreApplication.translate("MainWindow", u"Use Proxy For Imap", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"Reg. Settings", None))
        self.checkBox_TimeOutFarm.setText(QCoreApplication.translate("MainWindow", u"Time Out Farm", None))
        self.checkBox_CheckPoints.setText(QCoreApplication.translate("MainWindow", u"Check Points", None))
        self.checkBox_RarelyShowLogs.setText(QCoreApplication.translate("MainWindow", u"Rarely Show Logs", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QCoreApplication.translate("MainWindow", u"Farm", None))
        self.checkBox_ClaimRewardOnly.setText(QCoreApplication.translate("MainWindow", u"Claim Reward ONLY", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"Rewards", None))
#if QT_CONFIG(tooltip)
        self.label_MinProxiScore.setToolTip(QCoreApplication.translate("MainWindow", u"\u0423\u0441\u0442\u0430\u043d\u043e\u0432\u0438\u0442\u0435 MIN_PROXY_SCORE = 0, \u0447\u0442\u043e\u0431\u044b \u043d\u0435 \u043f\u0440\u043e\u0432\u0435\u0440\u044f\u0442\u044c \u0440\u0435\u0439\u0442\u0438\u043d\u0433 \u043f\u0440\u043e\u043a\u0441\u0438 (\u0435\u0441\u043b\u0438 \u0441\u0430\u0439\u0442 \u043d\u0435 \u0440\u0430\u0431\u043e\u0442\u0430\u0435\u0442)", None))
#endif // QT_CONFIG(tooltip)
        self.label_MinProxiScore.setText(QCoreApplication.translate("MainWindow", u"Min Proxy Score:", None))
#if QT_CONFIG(tooltip)
        self.label_EmailFolder.setToolTip(QCoreApplication.translate("MainWindow", u"\u0423\u0441\u0442\u0430\u043d\u043e\u0432\u0438\u0442\u0435 MIN_PROXY_SCORE = 0, \u0447\u0442\u043e\u0431\u044b \u043d\u0435 \u043f\u0440\u043e\u0432\u0435\u0440\u044f\u0442\u044c \u0440\u0435\u0439\u0442\u0438\u043d\u0433 \u043f\u0440\u043e\u043a\u0441\u0438 (\u0435\u0441\u043b\u0438 \u0441\u0430\u0439\u0442 \u043d\u0435 \u0440\u0430\u0431\u043e\u0442\u0430\u0435\u0442)", None))
#endif // QT_CONFIG(tooltip)
        self.label_EmailFolder.setText(QCoreApplication.translate("MainWindow", u"Email Folder:", None))
#if QT_CONFIG(tooltip)
        self.label_ImapDomain.setToolTip(QCoreApplication.translate("MainWindow", u"\u0423\u0441\u0442\u0430\u043d\u043e\u0432\u0438\u0442\u0435 MIN_PROXY_SCORE = 0, \u0447\u0442\u043e\u0431\u044b \u043d\u0435 \u043f\u0440\u043e\u0432\u0435\u0440\u044f\u0442\u044c \u0440\u0435\u0439\u0442\u0438\u043d\u0433 \u043f\u0440\u043e\u043a\u0441\u0438 (\u0435\u0441\u043b\u0438 \u0441\u0430\u0439\u0442 \u043d\u0435 \u0440\u0430\u0431\u043e\u0442\u0430\u0435\u0442)", None))
#endif // QT_CONFIG(tooltip)
        self.label_ImapDomain.setText(QCoreApplication.translate("MainWindow", u"Imap Domain:", None))
#if QT_CONFIG(tooltip)
        self.label_Threads.setToolTip(QCoreApplication.translate("MainWindow", u"\u0434\u043b\u044f \u0440\u0435\u0436\u0438\u043c\u0430 \u0440\u0435\u0433\u0438\u0441\u0442\u0440\u0430\u0446\u0438\u0438 \u0430\u043a\u043a\u0430\u0443\u043d\u0442\u043e\u0432 / \u043f\u043e\u043b\u0443\u0447\u0435\u043d\u0438\u044f \u043d\u0430\u0433\u0440\u0430\u0434 / \u043f\u043e\u0434\u0442\u0432\u0435\u0440\u0436\u0434\u0435\u043d\u0438\u044f email", None))
#endif // QT_CONFIG(tooltip)
        self.label_Threads.setText(QCoreApplication.translate("MainWindow", u"Threads:", None))
        self.pushButton_Save.setText(QCoreApplication.translate("MainWindow", u"Save", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Register Delay:", None))
    # retranslateUi

