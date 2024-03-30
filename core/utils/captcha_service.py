import asyncio
import captchatools
from data.config import (
    TWO_CAPTCHA_API_KEY,
    ANTICAPTCHA_API_KEY,
    CAPMONSTER_API_KEY,
    CAPSOLVER_API_KEY,
    CAPTCHAAI_API_KEY,
    CAPTCHA_PARAMS
)


class CaptchaService:
    def __init__(self):
        self.SERVICE_API_MAP = {
            "2captcha": TWO_CAPTCHA_API_KEY,
            "anticaptcha": ANTICAPTCHA_API_KEY,
            "capmonster": CAPMONSTER_API_KEY,
            "capsolver": CAPSOLVER_API_KEY,
            "captchaai": CAPTCHAAI_API_KEY,
        }

    def get_captcha_token(self):
        captcha_config = self.parse_captcha_type()
        solver = captchatools.new_harvester(**captcha_config, **CAPTCHA_PARAMS)
        return solver.get_token()

    def parse_captcha_type(self, exit_on_fail: bool = True):
        for service, api_key in self.SERVICE_API_MAP.items():
            if api_key:
                return {"solving_site": service, "api_key": api_key}
        if exit_on_fail:
            exit("No valid captcha solving service API key found")
        # raise ValueError("No valid captcha solving service API key found")

    async def get_captcha_token_async(self):
        return await asyncio.to_thread(self.get_captcha_token)
