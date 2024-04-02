import asyncio
import random

from core.utils import logger
from core.utils.exception import FailureLimitReachedException


def raise_error(error_type: Exception):
    raise error_type


class FailureCounter:
    def __init__(self):
        self.fail_count = 0

    def fail_increment(self, step: float = 1):
        self.fail_count += step

    def check_limit_reached(self, limit: int):
        return self.fail_count >= limit

    def fail_reset(self):
        self.fail_count = 0

    async def failure_handler(self, step: float = 1, limit: int = 5, is_raise: bool = True, msg: str = "",
                              sleep_time: int = 0):
        if self.check_limit_reached(limit):
            self.fail_reset()
            if is_raise:
                raise_error(FailureLimitReachedException(self.fail_count))
            else:
                await self.reset_with_delay(msg, sleep_time)
        else:
            self.fail_increment(step)

    async def reset_with_delay(self, msg: str, sleep_time: int = 0):
        self.fail_reset()
        logger.info(msg)
        await asyncio.sleep(sleep_time)
