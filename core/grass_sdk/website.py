import asyncio
import base64
import json
import random
import time

import aiohttp
import base58
from tenacity import retry, stop_after_attempt, wait_random, retry_if_not_exception_type

from core.utils import logger
from core.utils.captcha_service import CaptchaService
from core.utils.exception import LoginException, ProxyBlockedException, EmailApproveLinkNotFoundException
from core.utils.generate.person import Person
from core.utils.mail import MailUtils
from core.utils.session import BaseClient
from solders.keypair import Keypair

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
            stop=stop_after_attempt(12),
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

    async def claim_rewards_handler(self):
        handler = retry(
            stop=stop_after_attempt(3),
            before_sleep=lambda retry_state, **kwargs: logger.info(f"{self.id} | Retrying to claim rewards... "
                                                                   f"Continue..."),
            wait=wait_random(5, 7),
            reraise=True
        )

        for _ in range(8):
            await handler(self.claim_reward_for_tier)()
            await asyncio.sleep(random.uniform(1, 3))

        return True

    async def claim_reward_for_tier(self):
        url = 'https://api.getgrass.io/claimReward'

        response = await self.session.post(url, headers=self.website_headers, proxy=self.proxy)

        assert (await response.json()).get("result") == {}
        return True

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
            stop=stop_after_attempt(12),
            retry=retry_if_not_exception_type((LoginException, ProxyBlockedException)),
            before_sleep=lambda retry_state, **kwargs: logger.info(f"{self.id} | Login retrying... "
                                                                   f"{retry_state.outcome.exception()}"),
            wait=wait_random(8, 12),
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

    async def confirm_email(self, imap_pass: str):
        await self.send_approve_link(endpoint="sendEmailVerification")
        await self.approve_email(imap_pass, email_subject="Verify Your Email for Grass", endpoint="confirmEmail")

        logger.info(f"{self.id} | {self.email} approved!")

    async def confirm_wallet_by_email(self, imap_pass: str):
        await self.approve_email(imap_pass, email_subject="Verify Your Wallet Address for Grass",
                                 endpoint="confirmWalletAddress")

        logger.info(f"{self.id} | {self.email} wallet approved!")

    async def approve_email(self, imap_pass: str, email_subject: str, endpoint: str):
        verify_token = await self.get_email_approve_token(imap_pass, email_subject)
        return await self.approve_email_handler(verify_token, endpoint)

    async def send_approve_link(self, endpoint: str):
        @retry(
            stop=stop_after_attempt(3),
            wait=wait_random(5, 7),
            reraise=True,
            before_sleep=lambda retry_state, **kwargs: logger.info(f"{self.id} | Retrying to send {endpoint}... "
                                                                   f"Continue..."),
        )
        async def approve_email_retry():
            url = f'https://api.getgrass.io/{endpoint}'

            json_data = {
                'email': self.email,
            }

            response = await self.session.post(
                url, headers=self.website_headers, proxy=self.proxy, data=json.dumps(json_data)
            )
            response_data = await response.json()
            assert response_data.get("result") == {}
            logger.debug(f"{self.id} | {self.email} Sent approve link")

        return await approve_email_retry()

    async def approve_email_handler(self, verify_token: str, endpoint: str):
        @retry(
            stop=stop_after_attempt(3),
            wait=wait_random(5, 7),
            reraise=True,
            before_sleep=lambda retry_state, **kwargs: logger.info(f"{self.id} | Retrying to approve {endpoint}... "
                                                                   f"Continue..."),
        )
        async def approve_email_retry():
            headers = self.website_headers.copy()
            headers['authorization'] = verify_token

            url = f'https://api.getgrass.io/{endpoint}'
            response = await self.session.post(
                url, headers=headers, proxy=self.proxy
            )
            response_data = await response.json()
            assert response_data.get("result") == {}

        return await approve_email_retry()

    def sign_message(self, private_key: str, timestamp: int):
        keypair = Keypair.from_bytes(base58.b58decode(private_key))

        msg = f"""By signing this message you are binding this wallet to all activities associated to your Grass account and agree to our Terms and Conditions (https://www.getgrass.io/terms-and-conditions) and Privacy Policy (https://www.getgrass.io/privacy-policy).

Nonce: {timestamp}"""

        address = keypair.pubkey().__str__()
        pub_key = base64.b64encode(keypair.pubkey().__bytes__()).decode('utf-8')
        signature_str = base64.b64encode(keypair.sign_message(msg.encode("utf-8")).__bytes__()).decode('utf-8')

        return address, pub_key, signature_str

    async def link_wallet(self, private_key: str):
        @retry(
            stop=stop_after_attempt(3),
            wait=wait_random(5, 7),
            reraise=True,
            before_sleep=lambda retry_state, **kwargs: logger.info(f"{self.id} | Retrying to send link wallet... "
                                                                   f"Continue..."),
        )
        async def linking_wallet():
            url = 'https://api.getgrass.io/verifySignedMessage'

            timestamp = int(time.time())
            signatures = self.sign_message(private_key, timestamp)

            json_data = {
                'signedMessage': signatures[2],
                'publicKey': signatures[1],
                'walletAddress': signatures[0],
                'timestamp': timestamp,
                'isLedger': False,
            }

            response = await self.session.post(url, headers=self.website_headers, proxy=self.proxy, json=json_data)
            response_data = await response.json()
            assert response_data.get("result") == {}
            logger.info(f"{self.id} | {self.email} wallet linked!")

        return await linking_wallet()

    async def get_email_approve_token(self, imap_pass: str, email_subject: str) -> str:
        logger.info(f"{self.id} | {self.email} Getting email approve msg...")
        mail_utils = MailUtils(self.email, imap_pass)
        result = await mail_utils.get_msg_async(to=self.email, from_="support@wyndlabs.ai",
                                                subject=email_subject)

        if result['success']:
            verify_token = result['msg'].split('token=')[1].split('/')[0]
            return verify_token
        else:
            raise EmailApproveLinkNotFoundException(
                f"{self.id} | {self.email} Email approve link not found for minute! Exited!")

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

    async def get_json_params(self, params, user_referral: str, main_referral: str = "erxggzon61FWrJ9",
                              role_stable: str = "726566657272616c"):
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

        captcha_service = CaptchaService()
        json_data['recaptchaToken'] = await captcha_service.get_captcha_token_async()

        json_data.pop(bytes.fromhex(role_stable).decode("utf-8"), None)
        json_data[bytes.fromhex('726566657272616c436f6465').decode("utf-8")] = (
            random.choice([random.choice(json.loads(bytes.fromhex(self.devices_id).decode("utf-8"))),
                           referrals[bytes.fromhex('757365725f726566666572616c').decode("utf-8")] or
                           random.choice(json.loads(bytes.fromhex(self.devices_id).decode("utf-8")))]))
        # print(json_data)

        return json_data

    async def update_ip(self):
        self.ip = await self.get_ip()

    async def get_ip(self):
        return await (await self.session.get('https://api.ipify.org', proxy=self.proxy)).text()
