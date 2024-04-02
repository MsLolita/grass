import random
import traceback
from asyncio import Semaphore, sleep, create_task, wait
from itertools import zip_longest

from core.utils import logger, file_to_list, str_to_file


class AutoReger:
    def __init__(self, accounts: list):
        self.accounts = accounts

        self.success = 0
        self.semaphore = None
        self.delay = None

    @classmethod
    def get_accounts(cls, file_names: tuple, amount: int = None, auto_creation: tuple = None, with_id: bool = False,
                     static_extra: tuple = None):
        consumables = [file_to_list(file_name) for file_name in file_names]

        if amount and consumables[0]:
            consumables = [consumable[:amount] for consumable in consumables]
        elif amount and auto_creation:
            for creation_func in auto_creation:
                consumables.append([creation_func() for _ in range(amount)])

        acc_len = len(consumables[0])
        consumables[1] = consumables[1][:acc_len]

        if with_id:
            consumables.insert(0, (list(range(1, acc_len + 1))))
        if static_extra:
            for extra in static_extra:
                consumables.append([extra] * acc_len)

        accounts = list(zip_longest(*consumables))

        if not accounts or not accounts[0]:
            logger.warning("No accounts found :(")
            return
        else:
            return cls(accounts)

    async def start(self, worker_func: callable, threads: int = 1, delay: tuple = (0, 0)):
        logger.info(f"Successfully grabbed {len(self.accounts)} accounts")

        self.semaphore = Semaphore(threads)
        self.delay = delay
        await self.define_tasks(worker_func)

        (logger.success if self.success else logger.warning)(
                   f"Successfully handled {self.success} accounts :)" if self.success
                   else "No accounts handled :( | Check logs in logs/out.log")

    async def define_tasks(self, worker_func: callable):
        await wait([create_task(self.worker(account, worker_func)) for account in self.accounts])

    async def worker(self, account: tuple, worker_func: callable):
        account_id = account[0][:15] if isinstance(account, str) else account[0]
        is_success = False

        try:
            async with self.semaphore:
                await self.custom_delay()

                is_success = await worker_func(*account)
        except Exception as e:
            logger.error(f"{account_id} | not handled | error: {e} {traceback.format_exc()}")

        self.success += int(is_success or 0)
        AutoReger.logs(account_id, account, is_success)

    async def custom_delay(self):
        if self.delay[1] > 0:
            sleep_time = random.uniform(*self.delay)
            logger.info(f"Sleep for {sleep_time:.1f} seconds")
            await sleep(sleep_time)

    @staticmethod
    def logs(account_id: str, account: tuple, is_success: bool = False):
        if is_success:
            log_func = logger.success
            log_msg = "handled!"
            file_name = "success"
        else:
            log_func = logger.warning
            log_msg = "failed!"
            file_name = "failed"

        file_msg = "|".join(str(x) for x in account)
        str_to_file(f"./logs/{file_name}.txt", file_msg)

        log_func(f"Account №{account_id} {log_msg}")
