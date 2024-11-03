THREADS = 5  # for register account / claim rewards mode / approve email mode
MIN_PROXY_SCORE = 0  # for mining mode

#########################################
APPROVE_EMAIL = False  # approve email (NEEDED IMAP AND ACCESS TO EMAIL)
CONNECT_WALLET = False  # connect wallet (put private keys in wallets.txt)
SEND_WALLET_APPROVE_LINK_TO_EMAIL = False  # send approve link to email
APPROVE_WALLET_ON_EMAIL = False  # get approve link from email (NEEDED IMAP AND ACCESS TO EMAIL)
SEMI_AUTOMATIC_APPROVE_LINK = False # if True - allow to manual paste approve link from email to cli
# If you have possibility to forward all approve mails to single IMAP address:
SINGLE_IMAP_ACCOUNT = False # usage "name@domain.com:password"

# skip for auto chosen
EMAIL_FOLDER = ""  # folder where mails comes
IMAP_DOMAIN = ""  # not always works

#########################################

CLAIM_REWARDS_ONLY = False  # claim tiers rewards only (https://app.getgrass.io/dashboard/referral-program)

STOP_ACCOUNTS_WHEN_SITE_IS_DOWN = False  # stop account for 20 minutes, to reduce proxy traffic usage
CHECK_POINTS = False  # show point for each account every nearly 10 minutes
SHOW_LOGS_RARELY = False  # not always show info about actions to decrease pc influence

# Mining mode
MINING_MODE = True  # False - not mine grass, True - mine grass | Remove all True on approve \ register section

# REGISTER PARAMETERS ONLY
REGISTER_ACCOUNT_ONLY = False
REGISTER_DELAY = (3, 7)

TWO_CAPTCHA_API_KEY = "c4bf076d2f0dcaff5acf65efb8e5a0b6"
ANTICAPTCHA_API_KEY = "de7aa4cd826e382ef84e4dc648f957d0"
CAPMONSTER_API_KEY = ""
CAPSOLVER_API_KEY = ""
CAPTCHAAI_API_KEY = ""

# Captcha params, left empty
CAPTCHA_PARAMS = {
    "captcha_type": "v2",
    "invisible_captcha": False,
    "sitekey": "6LeeT-0pAAAAAFJ5JnCpNcbYCBcAerNHlkK4nm6y",
    "captcha_url": "https://app.getgrass.io/register"
}

########################################

ACCOUNTS_FILE_PATH = "data/accounts.txt"
PROXIES_FILE_PATH = "data/proxies.txt"
WALLETS_FILE_PATH = "data/wallets.txt"
