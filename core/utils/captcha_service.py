import asyncio
import captchatools
from data.config import settings


class CaptchaService:
    def __init__(self):
        self.SERVICE_API_MAP = {
            "2captcha": settings.TWO_CAPTCHA_API_KEY,
            "anticaptcha": settings.ANTICAPTCHA_API_KEY,
            "capmonster": settings.CAPMONSTER_API_KEY,
            "capsolver": settings.CAPSOLVER_API_KEY,
            "captchaai": settings.CAPTCHAAI_API_KEY,
        }

    def get_captcha_token(self):
        captcha_config = self.parse_captcha_type()
        solver = captchatools.new_harvester(**captcha_config, **settings.CAPTCHA_PARAMS)
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
