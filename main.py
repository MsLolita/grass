import asyncio
import ctypes
import random
import sys
import traceback

import aiohttp
from art import tprint
from better_proxy import Proxy

from core import Grass
from core.autoreger import AutoReger
from core.utils import logger, file_to_list
from core.utils.accounts_db import AccountsDB
from core.utils.exception import LowProxyScoreException, ProxyScoreNotFoundException, ProxyForbiddenException, \
    LoginException
from core.utils.generate.person import Person
from data.config import ACCOUNTS_FILE_PATH, PROXIES_FILE_PATH, REGISTER_ACCOUNT_ONLY, THREADS, REGISTER_DELAY


def bot_info(name: str = ""):
    tprint(name)

    if sys.platform == 'win32':
        ctypes.windll.kernel32.SetConsoleTitleW(f"{name}")
    print("EnJoYeR's <crypto/> moves: https://t.me/+tdC-PXRzhnczNDli\nDonate here: 0x000007c73a94f8582ef95396918dcd04f806cdd8")


async def worker_task(_id, account: str, proxy: str = None, db: AccountsDB = None):
    consumables = account.split(":")[:2]

    if len(consumables) == 1:
        email = consumables[0]
        password = Person().random_string(8)
    else:
        email, password = consumables

    grass = None

    for _ in range(3):
        try:
            grass = Grass(_id, email, password, proxy, db)

            if REGISTER_ACCOUNT_ONLY:
                await asyncio.sleep(random.uniform(*REGISTER_DELAY))
                logger.info(f"Starting №{_id} | {email} | {password} | {proxy}")

                await grass.create_account()
            else:
                await asyncio.sleep(random.uniform(0.5, 1) * _id)
                logger.info(f"Starting №{_id} | {email} | {password} | {proxy}")

                await grass.start()

            return True
        except LoginException as e:
            logger.warning(e)
            return True
        except Exception as e:
            logger.error(f"{_id} | not handled exception | error: {e} {traceback.format_exc()}")
        finally:
            if grass:
                await grass.session.close()


async def main():
    accounts = file_to_list(ACCOUNTS_FILE_PATH)
    proxies = [Proxy.from_str(proxy).as_url for proxy in file_to_list(PROXIES_FILE_PATH)]

    db = AccountsDB('data/proxies_stats.db')
    await db.connect()
    await db.delete_all_proxies()
    await db.push_proxies(proxies[len(accounts):])

    autoreger = AutoReger.get_accounts(
        (ACCOUNTS_FILE_PATH, PROXIES_FILE_PATH),
        with_id=True,
        static_extra=(db, )
    )

    if REGISTER_ACCOUNT_ONLY:
        msg = "__REGISTER__ MODE"
        threads = THREADS
    else:
        msg = "__MINING__ MODE"
        threads = len(autoreger.accounts)

    logger.info(msg)

    await autoreger.start(worker_task, threads)

    await db.close_connection()


if __name__ == "__main__":
    bot_info("GRASS_AUTO")

    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        loop = asyncio.ProactorEventLoop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(main())
    else:
        asyncio.run(main())
