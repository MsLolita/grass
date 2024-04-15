from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_ignore_empty=True)
    MIN_PROXY_SCORE: int = 50
    CLAIM_REWARDS_ONLY: bool = False
    REGISTER_ACCOUNT_ONLY: bool = False
    REGISTER_DELAY_MIN: int = 3
    REGISTER_DELAY_MAX: int = 5
    THREADS: int = 2
    CHECK_POINTS: bool = True
    STOP_ACCOUNTS_WHEN_SITE_IS_DOWN: bool = True
    SHOW_LOGS_RARELY: bool = False
    ACCOUNTS_FILE_PATH: str = "data/accounts.txt"
    PROXIES_FILE_PATH: str = "data/proxies.txt"
    REF_CODE: str = "fUzBa0jy7s9Eawx" # %)
    TWO_CAPTCHA_API_KEY: str = ""
    ANTICAPTCHA_API_KEY: str = ""
    CAPMONSTER_API_KEY: str = ""
    CAPSOLVER_API_KEY: str = ""
    CAPTCHAAI_API_KEY: str = ""
    CAPTCHA_PARAMS: str = ""


settings = Settings()
