from os import getenv

MIN_PROXY_SCORE = int(getenv("MIN_PROXY_SCORE", 50))

CLAIM_REWARDS_ONLY = eval(getenv("CLAIM_REWARDS_ONLY", "False"))  # claim tiers rewards only (https://app.getgrass.io/dashboard/referral-program)

# REGISTER PARAMETRS ONLY
REGISTER_ACCOUNT_ONLY = eval(getenv("REGISTER_ACCOUNT_ONLY", "True")) 
REGISTER_DELAY = eval(getenv("REGISTER_DELAY", "(3, 7)")) 
THREADS = int(getenv("THREADS", 2))  # for register account / claim rewards mode only

CHECK_POINTS = eval(getenv("CHECK_POINTS", "True"))  # show point for each account every nearly 10 minutes

STOP_ACCOUNTS_WHEN_SITE_IS_DOWN = eval(getenv("STOP_ACCOUNTS_WHEN_SITE_IS_DOWN", "True")) # stop account for 20 minutes, to reduce proxy traffic usage

SHOW_LOGS_RARELY = eval(getenv("SHOW_LOGS_RARELY", "False"))

########################################

ACCOUNTS_FILE_PATH = "data/accounts.txt"
PROXIES_FILE_PATH = "data/proxies.txt"

