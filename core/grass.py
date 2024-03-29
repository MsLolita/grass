import asyncio
import uuid

import aiohttp
from fake_useragent import UserAgent
from tenacity import stop_after_attempt, retry, retry_if_not_exception_type, wait_random, retry_if_exception_type

from data.config import MIN_PROXY_SCORE
from .grass_sdk.extension import GrassWs
from .grass_sdk.website import GrassRest
from .utils import logger
from .utils.exception import WebsocketClosedException, LowProxyScoreException, ProxyScoreNotFoundException, \
    ProxyForbiddenException
from better_proxy import Proxy


class Grass(GrassWs, GrassRest):
    def __init__(self, _id: int, email: str, password: str, proxy: str = None):
        self.proxy = Proxy.from_str(proxy).as_url if proxy else None
        super(GrassWs, self).__init__(email=email, password=password, user_agent=UserAgent().random, proxy=self.proxy)
        self.proxy_score = None
        self.id = _id

        self.session = aiohttp.ClientSession(trust_env=True, connector=aiohttp.TCPConnector(ssl=False))

    async def start(self):
        # logger.info(f"{self.id} | {self.email} | Starting...")

        user_id = await self.enter_account()
        browser_id = str(uuid.uuid3(uuid.NAMESPACE_DNS, self.proxy or ""))

        await self.run(browser_id, user_id)

    async def run(self, browser_id: str, user_id: str):
        while True:
            try:
                await self.connection_handler()
                await self.auth_to_extension(browser_id, user_id)

                if self.proxy_score is None:
                    await asyncio.sleep(1)

                    await self.handle_proxy_score(MIN_PROXY_SCORE)

                while True:
                    await self.send_ping()
                    await self.send_pong()

                    logger.info(f"{self.id} | Mined grass.")
                    # await self.handle_proxy_score(browser_id, 50)
                    await asyncio.sleep(19.9)
                    # await self.handle_proxy_score(browser_id, 50)
            except WebsocketClosedException as e:
                logger.info(f"Websocket closed: {e}. Retrying...")
            except ConnectionResetError as e:
                logger.info(f"Connection reset: {e}. Retrying...")
            await asyncio.sleep(1)

    @retry(stop=stop_after_attempt(30),
           retry=(retry_if_exception_type(ConnectionError) | retry_if_not_exception_type(ProxyForbiddenException)),
           wait=wait_random(0.5, 1),
           reraise=True)
    async def connection_handler(self):
        logger.info(f"{self.id} | Connecting...")
        await self.connect()
        logger.info(f"{self.id} | Connected")

    @retry(stop=stop_after_attempt(20),
           retry=retry_if_not_exception_type(LowProxyScoreException),
           before_sleep=lambda retry_state, **kwargs: logger.info(f"{retry_state.outcome.exception()}"),
           wait=wait_random(5, 7),
           reraise=True)
    async def handle_proxy_score(self, min_score: int):
        if (proxy_score := await self.get_proxy_score_by_device_id()) is None:
            raise ProxyScoreNotFoundException(f"{self.id} | Proxy score not found for {self.proxy}. Retrying...")
        elif proxy_score >= min_score:
            self.proxy_score = proxy_score
            logger.success(f"{self.id} | Proxy score: {self.proxy_score}")
            return True
        else:
            raise LowProxyScoreException(f"{self.id} | Too low proxy score: {proxy_score} for {self.proxy}. Exit...")
