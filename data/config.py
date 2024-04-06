MIN_PROXY_SCORE = 50

CLAIM_REWARDS_ONLY = False  # claim tiers rewards only (https://app.getgrass.io/dashboard/referral-program)

# REGISTER PARAMETRS ONLY
REGISTER_ACCOUNT_ONLY = True
REGISTER_DELAY = (1, 100)
THREADS = 1  # for register account / claim rewards mode only

CHECK_POINTS = True  # show point for each account every nearly 10 minutes

STOP_ACCOUNTS_WHEN_SITE_IS_DOWN = True  # stop account for 20 minutes, to reduce proxy traffic usage
########################################
# While this variable is bool(True) ref code will be retried from a data\ref_codes_any.txt,
#                             all string that follow this pattern r'[A-Za-z0-9_-]{15}' will be considered reff-codes.
# While this variable is string, it itself be considered as one-and-only reff-code (default as before)
USE_CUSTOM_REF_LINK_FILE = True
########################################

ACCOUNTS_FILE_PATH = "data/accounts.txt"
PROXIES_FILE_PATH = "data/proxies.txt"
