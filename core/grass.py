import asyncio
import uuid
from typing import List, Optional

import aiohttp
from fake_useragent import UserAgent
from tenacity import stop_after_attempt, retry, retry_if_not_exception_type, wait_random, retry_if_exception_type

from data.config import MIN_PROXY_SCORE, CHECK_POINTS
from .grass_sdk.extension import GrassWs
from .grass_sdk.website import GrassRest
from .utils import logger
from .utils.accounts_db import AccountsDB
from .utils.exception import WebsocketClosedException, LowProxyScoreException, ProxyScoreNotFoundException, \
    ProxyForbiddenException, ProxyError
from better_proxy import Proxy


class Grass(GrassWs, GrassRest):
    def __init__(self, _id: int, email: str, password: str, proxy: str = None, db: AccountsDB = None):
        self.proxy = Proxy.from_str(proxy).as_url if proxy else None
        super(GrassWs, self).__init__(email=email, password=password, user_agent=UserAgent().random, proxy=self.proxy)
        self.proxy_score: Optional[int] = None
        self.id: int = _id

        self.db: AccountsDB = db

        self.session: aiohttp.ClientSession = aiohttp.ClientSession(trust_env=True,
                                                                    connector=aiohttp.TCPConnector(ssl=False))

        self.proxies: List[str] = [self.proxy]
        self.is_new_proxies_used: bool = False

    async def start(self):
        # logger.info(f"{self.id} | {self.email} | Starting...")
        while True:
            try:
                user_id = await self.enter_account()

                browser_id = str(uuid.uuid3(uuid.NAMESPACE_DNS, self.proxy or ""))

                await self.run(browser_id, user_id)
            except ProxyForbiddenException:
                self.proxies.remove(self.proxy)
                msg = "Proxy forbidden"
            except ProxyError:
                msg = "Low proxy score"
            except aiohttp.ClientError as e:
                msg = f"{str(e.args[0])[:20]}..." if "</html>" not in str(e) else "Html page response, 504"
            else:
                msg = ""

            await self.change_proxy()
            logger.info(f"{self.id} | Changed Proxy. {msg}. Retrying...")

    async def run(self, browser_id: str, user_id: str):
        while True:
            try:
                await self.connection_handler()
                await self.auth_to_extension(browser_id, user_id)

                if self.proxy_score is None:
                    await asyncio.sleep(1)

                    await self.handle_proxy_score(MIN_PROXY_SCORE)

                for i in range(999999):
                    await self.send_ping()
                    await self.send_pong()

                    logger.info(f"{self.id} | Mined grass.")

                    if CHECK_POINTS and not (i % 30):
                        points = await self.get_points()
                        logger.info(f"{self.id} | Total points: {points}")

                    await asyncio.sleep(19.9)
            except WebsocketClosedException as e:
                logger.info(f"{self.id} | Websocket closed: {e}. Reconnecting...")
            except ConnectionResetError as e:
                logger.info(f"{self.id} | Connection reset: {e}. Reconnecting...")
            except TypeError as e:
                logger.info(f"{self.id} | Type error: {e}. Reconnecting...")

            await asyncio.sleep(1)

    @retry(stop=stop_after_attempt(30),
           retry=(retry_if_exception_type(ConnectionError) | retry_if_not_exception_type(ProxyForbiddenException)),
           wait=wait_random(0.5, 1),
           reraise=True)
    async def connection_handler(self):
        logger.info(f"{self.id} | Connecting...")
        await self.connect()
        logger.info(f"{self.id} | Connected")

    @retry(stop=stop_after_attempt(10),
           retry=retry_if_not_exception_type(LowProxyScoreException),
           before_sleep=lambda retry_state, **kwargs: logger.info(f"{retry_state.outcome.exception()}"),
           wait=wait_random(5, 7),
           reraise=True)
    async def handle_proxy_score(self, min_score: int):
        if (proxy_score := await self.get_proxy_score_by_device_id_handler()) is None:
            # logger.info(f"{self.id} | Proxy score not found for {self.proxy}. Guess Bad proxies! Continue...")
            # return None
            raise ProxyScoreNotFoundException(f"{self.id} | Proxy score not found! Retrying...")
        elif proxy_score >= min_score:
            self.proxy_score = proxy_score
            logger.success(f"{self.id} | Proxy score: {self.proxy_score}")
            return True
        else:
            raise LowProxyScoreException(f"{self.id} | Too low proxy score: {proxy_score} for {self.proxy}. Exit...")

    async def change_proxy(self):
        self.proxy = await self.get_new_proxy()

    async def get_new_proxy(self):
        if self.is_new_proxies_used:
            pass
        elif (proxy := await self.db.get_new()) is not None:
            if proxy not in self.proxies:
                if email := await self.db.proxies_exist(proxy):
                    if self.email == email:
                        self.proxies.insert(0, proxy)
                else:
                    await self.db.add_proxy(self.email, proxy)
                    self.proxies.insert(0, proxy)
        else:
            self.is_new_proxies_used = True

        return self.next_proxy()

    def next_proxy(self):
        proxy = self.proxies.pop(0)
        self.proxies.append(proxy)

        return proxy
