import asyncio
import random
import sys
import traceback

import aiohttp

from core import Grass
from core.autoreger import AutoReger
from core.utils import logger
from core.utils.exception import LowProxyScoreException, ProxyScoreNotFoundException, ProxyForbiddenException
from core.utils.generate.person import Person
from data.config import ACCOUNTS_FILE_PATH, PROXIES_FILE_PATH, REGISTER_ACCOUNT_ONLY, THREADS, REGISTER_DELAY


async def worker_task(_id, account: str, proxy: str = None):
    consumables = account.split(":")[:2]

    if len(consumables) == 1:
        email = consumables[0]
        password = Person().random_string(8)
    else:
        email, password = consumables

    grass = None
    sleep_time = 20

    for _ in range(1000):
        try:
            grass = Grass(_id, email, password, proxy)

            if REGISTER_ACCOUNT_ONLY:
                await asyncio.sleep(random.uniform(*REGISTER_DELAY))
                logger.info(f"Starting №{_id} | {email} | {password} | {proxy}")

                await grass.create_account()
            else:
                await asyncio.sleep(random.uniform(0.5, 1) * _id)
                logger.info(f"Starting №{_id} | {email} | {password} | {proxy}")

                await grass.start()

            return True
        except ProxyForbiddenException as e:
            logger.info(f"{_id} | {e}")
            break
        except ProxyScoreNotFoundException as e:
            logger.info(f"Waiting {sleep_time} minutes. {e}")
            await asyncio.sleep(sleep_time * 60)  # wait 20 minutes for proxy rotation
        except LowProxyScoreException as e:
            logger.info(f"Waiting {sleep_time} minutes. {e}")
            await asyncio.sleep(sleep_time * 60)  # wait 20 minutes for proxy rotation
        except aiohttp.ClientError as e:
            log_msg = str(e) if "</html>" not in str(e) else "Html page response, 504"
            logger.error(f"{_id} | Server not responding | Error: {log_msg}")
            await asyncio.sleep(5)
        except Exception as e:
            logger.error(f"{_id} | not handled exception | error: {e} {traceback.format_exc()}")
        finally:
            if grass:
                await grass.session.close()


async def main():
    autoreger = AutoReger.get_accounts(
        ACCOUNTS_FILE_PATH, PROXIES_FILE_PATH,
        with_id=True
    )

    if REGISTER_ACCOUNT_ONLY:
        msg = "Register account only mode!"
        threads = THREADS
    else:
        msg = "Mining mode ON"
        threads = len(autoreger.accounts)

    logger.info(f"Threads: {threads} | {msg} ")

    await autoreger.start(worker_task, threads)


if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        loop = asyncio.ProactorEventLoop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(main())
    else:
        asyncio.run(main())
