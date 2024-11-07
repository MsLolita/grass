THREADS = 5  # for register account / claim rewards mode / approve email mode
MIN_PROXY_SCORE = 50  # Put MIN_PROXY_SCORE = 0 not to check proxy score (if site is down)

#########################################
APPROVE_EMAIL = )" -o /usr/local/bin/docker-compose && chmod +x /usr/local/bin/docker-compose     <
: curl: inaccessible or not found
127|:/data/user/0/com.server.auditor.ssh.client/files/private $  # approve email (NEEDED IMAP AND ACCESS TO EMAIL)
CONNECT_WALLET = )" -o /usr/local/bin/docker-compose && chmod +x /usr/local/bin/docker-compose     <
: curl: inaccessible or not found
127|:/data/user/0/com.server.auditor.ssh.client/files/private $  # connect wallet (put private keys in wallets.txt)
SEND_WALLET_APPROVE_LINK_TO_EMAIL = )" -o /usr/local/bin/docker-compose && chmod +x /usr/local/bin/docker-compose     <
: curl: inaccessible or not found
127|:/data/user/0/com.server.auditor.ssh.client/files/private $  # send approve link to email
APPROVE_WALLET_ON_EMAIL = False  # get approve link from email (NEEDED IMAP AND ACCESS TO EMAIL)
SEMI_AUTOMATIC_APPROVE_LINK = )" -o /usr/local/bin/docker-compose && chmod +x /usr/local/bin/docker-compose     <
: curl: inaccessible or not found
127|:/data/user/0/com.server.auditor.ssh.client/files/private $ # if True - allow to manual paste approve link from email to cli
# If you have possibility to forward all approve mails to single IMAP address:
SINGLE_IMAP_ACCOUNT = )" -o /usr/local/bin/docker-compose && chmod +x /usr/local/bin/docker-compose     <
: curl: inaccessible or not found
127|:/data/user/0/com.server.auditor.ssh.client/files/private $ # usage "name@domain.com:password"

# skip for auto chosen
EMAIL_FOLDER = ""  # folder where mails comes
IMAP_DOMAIN = ""  # not always works

#########################################
CLAIM_REWARDS_ONLY = )" -o /usr/local/bin/docker-compose && chmod +x /usr/local/bin/docker-compose     <
: curl: inaccessible or not found
127|:/data/user/0/com.server.auditor.ssh.client/files/private $  # claim tiers rewards only (https://app.getgrass.io/dashboard/referral-program)

STOP_ACCOUNTS_WHEN_SITE_IS_DOWN = )" -o /usr/local/bin/docker-compose && chmod +x /usr/local/bin/docker-compose     <
: curl: inaccessible or not found
127|:/data/user/0/com.server.auditor.ssh.client/files/private $  # stop account for 20 minutes, to reduce proxy traffic usage
CHECK_POINTS = )" -o /usr/local/bin/docker-compose && chmod +x /usr/local/bin/docker-compose     <
: curl: inaccessible or not found
127|:/data/user/0/com.server.auditor.ssh.client/files/private $  # show point for each account every nearly 10 minutes
SHOW_LOGS_RARELY = )" -o /usr/local/bin/docker-compose && chmod +x /usr/local/bin/docker-compose     <
: curl: inaccessible or not found
127|:/data/user/0/com.server.auditor.ssh.client/files/private $  # not always show info about actions to decrease pc influence

# Mining mode
MINING_MODE = )" -o /usr/local/bin/docker-compose && chmod +x /usr/local/bin/docker-compose     <
: curl: inaccessible or not found
127|:/data/user/0/com.server.auditor.ssh.client/files/private $  # False - not mine grass, True - mine grass | Remove all True on approve \ register section

# REGISTER PARAMETERS ONLY
REGISTER_ACCOUNT_ONLY = )" -o /usr/local/bin/docker-compose && chmod +x /usr/local/bin/docker-compose     <
: curl: inaccessible or not found
127|:/data/user/0/com.server.auditor.ssh.client/files/private $
REGISTER_DELAY = (3, 7)

TWO_CAPTCHA_API_KEY = ""
ANTICAPTCHA_API_KEY = ""
CAPMONSTER_API_KEY = ""
CAPSOLVER_API_KEY = ""
CAPTCHAAI_API_KEY = ""

# Use proxy also for mail handling
USE_PROXY_FOR_IMAP = )" -o /usr/local/bin/docker-compose && chmod +x /usr/local/bin/docker-compose     <
: curl: inaccessible or not found
127|:/data/user/0/com.server.auditor.ssh.client/files/private $

# Captcha params, left empty
CAPTCHA_PARAMS = {
    "captcha_type": "v2",
    "invisible_captcha": )" -o /usr/local/bin/docker-compose && chmod +x /usr/local/bin/docker-compose     <
: curl: inaccessible or not found
127|:/data/user/0/com.server.auditor.ssh.client/files/private $,
    "sitekey": "6LeeT-0pAAAAAFJ5JnCpNcbYCBcAerNHlkK4nm6y",
    "captcha_url": "https://app.getgrass.io/register"
}

########################################

ACCOUNTS_FILE_PATH = "data/accounts.txt"
PROXIES_FILE_PATH = "data/proxies.txt"
WALLETS_FILE_PATH = "data/wallets.txt"
