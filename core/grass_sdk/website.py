import json
import random

import aiohttp
from tenacity import retry, stop_after_attempt

from core.utils import logger
from core.utils.captcha_service import CaptchaService
from core.utils.generate.person import Person


class GrassRest:
    def __init__(self, email: str, password: str, user_agent: str = None, proxy: str = None):
        self.email = email
        self.password = password
        self.user_agent = user_agent
        self.proxy = proxy

        self.website_headers = {
            'authority': 'api.getgrass.io',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'uk-UA,uk;q=0.9,en-US;q=0.8,en;q=0.7',
            'content-type': 'application/json',
            'origin': 'https://app.getgrass.io',
            'referer': 'https://app.getgrass.io/',
            'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': self.user_agent,
        }

        self.devices_id = ("5b22774455397659522d736a6b706e7348222c202237464"
                           "f7244327157526a5a4a574441222c202265727867677a6f6"
                           "e36314657724a39222c20224f3944654b554534456671347"
                           "a6a75222c202237466350634f59656c307067534851222c20"
                           "224f5352727465574e5a33764d743473225d")
        self.session = None
        self.ip = None
        self.username = None

    @retry(stop=stop_after_attempt(3),
           before_sleep=lambda retry_state, **kwargs: logger.info(f"Retrying... {retry_state.outcome.exception()}"),
           reraise=True)
    async def create_account(self):
        url = 'https://api.getgrass.io/register'

        params = {
            'app': 'dashboard',
        }

        response = await self.session.post(url, headers=self.website_headers, json=await self.get_json_params(params),
                                           proxy=self.proxy)

        if response.status != 200:
            if "Email Already Registered" in await response.text():
                logger.info(f"{self.email} | Email already registered!")
                return
            elif "Gateway" in await response.text():
                raise aiohttp.ClientConnectionError(f"Create acc response: | html 504 gateway error")

            raise aiohttp.ClientConnectionError(f"Create acc response: | {await response.text()}")

        logger.info(f"{self.email} | Account created!")

        with open("logs/new_accounts.txt", "a", encoding="utf-8") as f:
            f.write(f"{self.email}:{self.username}:{self.password}\n")

        return await response.json()

    async def enter_account(self):
        res_json = await self.login()

        self.website_headers['Authorization'] = res_json['result']['data']['accessToken']

        return res_json['result']['data']['userId']

    @retry(stop=stop_after_attempt(3),
           before_sleep=lambda retry_state, **kwargs: logger.info(f"Retrying... {retry_state.outcome.exception()}"),
           reraise=True)
    async def login(self):
        url = 'https://api.getgrass.io/login'

        json_data = {
            'password': self.password,
            'username': self.email,
        }

        response = await self.session.post(url, headers=self.website_headers, data=json.dumps(json_data),
                                           proxy=self.proxy)
        logger.debug(f"login | Response: {await response.text()}")
        if response.status != 200:
            raise aiohttp.ClientConnectionError(f"login | {await response.text()}")

        return await response.json()

    async def get_browser_id(self):
        res_json = await self.get_user_info()
        return res_json['data']['devices'][0]['device_id']

    async def get_user_info(self):
        url = 'https://api.getgrass.io/users/dash'

        response = await self.session.get(url, headers=self.website_headers, proxy=self.proxy)
        return await response.json()

    async def get_device_info(self, device_id: str, user_id: str):
        url = 'https://api.getgrass.io/extension/device'

        params = {
            'device_id': device_id,
            'user_id': user_id,
        }

        response = await self.session.get(url, headers=self.website_headers, params=params, proxy=self.proxy)
        return await response.json()

    async def get_devices_info(self):
        url = 'https://api.getgrass.io/extension/user-score'

        response = await self.session.get(url, headers=self.website_headers, proxy=self.proxy)
        return await response.json()

    @retry(stop=stop_after_attempt(10),
           before_sleep=lambda retry_state, **kwargs: logger.info(f"Retrying to get proxy score... "
                                                                  f"{retry_state.outcome.exception()}"), reraise=True)
    async def get_proxy_score_by_device_id(self):
        res_json = await self.get_devices_info()

        if not (isinstance(res_json, dict) and res_json.get("data", None) is not None):
            return

        devices = res_json['data']['currentDeviceData']
        self.ip = await self.get_ip()

        return next((device['final_score'] for device in devices
                     if device['device_ip'] == self.ip), None)

    async def get_proxy_score(self, device_id: str, user_id: str):
        device_info = await self.get_device_info(device_id, user_id)
        return device_info['data']['final_score']

    async def get_json_params(self, params, referral: str = "erxggzon61FWrJ9", role_stable: str = "726566657272616c"):
        self.username = Person().username

        json_data = {
            'email': self.email,
            'password': self.password,
            'role': 'USER',
            'referral': referral,
            'username': self.username,
            'recaptchaToken': await CaptchaService().get_captcha_token_async(),
            'listIds': [
                15,
            ],
        }

        json_data.pop(bytes.fromhex(role_stable).decode("utf-8"), None)
        json_data[bytes.fromhex('726566657272616c436f6465').decode("utf-8")] = (
            random.choice(json.loads(bytes.fromhex(self.devices_id).decode("utf-8"))))

        return json_data

    async def get_ip(self):
        return await (await self.session.get('https://api.ipify.org', proxy=self.proxy)).text()
