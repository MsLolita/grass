import asyncio
import captchatools
import importlib
import data.config


class CaptchaService:
    def __init__(self):
        pass

    def get_service_api_map(self):
        importlib.reload(data.config)
        
        return {
            "2captcha": data.config.TWO_CAPTCHA_API_KEY,
            "anticaptcha": data.config.ANTICAPTCHA_API_KEY,
            "capmonster": data.config.CAPMONSTER_API_KEY,
            "capsolver": data.config.CAPSOLVER_API_KEY,
            "captchaai": data.config.CAPTCHAAI_API_KEY,
        }

    def get_captcha_token(self):
        captcha_config = self.parse_captcha_type()
        if captcha_config:
            solver = captchatools.new_harvester(**captcha_config, **data.config.CAPTCHA_PARAMS)
            return solver.get_token()
        return None

    def parse_captcha_type(self, exit_on_fail: bool = True):
        service_api_map = self.get_service_api_map()
        for service, api_key in service_api_map.items():
            if api_key:
                return {"solving_site": service, "api_key": api_key}
        if exit_on_fail:
            exit("No valid captcha solving service API key found")
        # raise ValueError("No valid captcha solving service API key found")
        return None
        
    async def get_captcha_token_async(self):
        return await asyncio.to_thread(self.get_captcha_token)
