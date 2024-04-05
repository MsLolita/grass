import asyncio
import random
from typing import Optional

from core.utils import logger
from core.utils.exception import FailureLimitReachedException


def raise_error(error_type: Exception):
    raise error_type


class FailureCounter:
    global_fail_counter = {}

    def __init__(self):
        self.fail_count = 0

        self.id = None

        self.limit = 5

    def fail_increment(self, step: float = 1):
        self.fail_count += step

    def check_limit_reached(self, limit: int):
        return self.fail_count >= limit

    def fail_reset(self):
        self.fail_count = 0

    async def failure_handler(self, step: float = 1, limit: Optional[int] = None, is_raise: bool = True, msg: str = "",
                              sleep_time: int = 0):
        if limit is None:
            limit = self.limit

        if self.check_limit_reached(limit):
            self.log_global_count()
            self.fail_reset()
            if is_raise:
                raise_error(FailureLimitReachedException(self.fail_count))
            else:
                sleep_time = random.randint(2, 5) * 60
                msg = f"{self.id} | Sleeping for {int(sleep_time)} seconds... Too many errors. Retrying..."
                await self.reset_with_delay(msg, sleep_time)
        else:
            self.fail_increment(step)

    async def reset_with_delay(self, msg: str, sleep_time: int = 0):
        self.fail_reset()
        await self.delay_with_log(msg, sleep_time)

    def reach_fail_limit(self):
        self.fail_count = self.limit

    async def delay_with_log(self, msg: str, sleep_time: int = random.randint(5, 10) * 60):
        logger.info(msg)
        await asyncio.sleep(sleep_time)

    def log_global_count(self, is_work: bool = False):
        FailureCounter.global_fail_counter[self.id] = int(is_work)

    @staticmethod
    async def clear_global_counter():
        await asyncio.sleep(10 * 60)

        FailureCounter.global_fail_counter = {x: 1 for x in FailureCounter.global_fail_counter}

    @staticmethod
    def is_global_error(min_limit: int = 10):
        amount = len(FailureCounter.global_fail_counter)
        work_count = sum(FailureCounter.global_fail_counter.values())
        fail_count = amount - work_count

        limit_fail_amount = amount * 0.30

        if limit_fail_amount < min_limit:
            limit_fail_amount = min(amount, min_limit)

        if fail_count > limit_fail_amount:
            asyncio.create_task(FailureCounter.clear_global_counter())
            return True
