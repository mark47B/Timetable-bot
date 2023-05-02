from loguru import logger

from toolz import pipe

import bot.handlers as handlers
import bot.adapters.handlers.callbacks as callbacks
from commands import set_default_commands
from loader import dp, bot


from aiogram import executor, Dispatcher, types


async def startup(dp: Dispatcher) -> None:
    """initialization"""
    await set_default_commands(dp)
    logger.info("bot started")


async def shutdown(dp: Dispatcher) -> None:
    logger.info("bot finished")

if __name__ == '__main__':
    logger.add(
        "../logs/debug.log",
        level="DEBUG",
        format="{time} | {level} | {module}:{function}:{line} | {message}",
        rotation="30 KB",
        compression="zip",
    )
    pipe(
        callbacks,
        handlers,
        executor.start_polling(dp, skip_updates=True, on_startup=startup, on_shutdown=shutdown)
    )
