from loguru import logger
import asyncio

from commands import set_default_commands
from loader import dp, bot

import adapters.FSMs.Reservation as Reservation
import adapters.handlers.handlers as handlers
import adapters.handlers.callbacks as callbacks

from aiogram import Dispatcher, types
from aiogram.filters import Command


async def startup(dp: Dispatcher) -> None:
    """initialization"""
    

async def shutdown(dp: Dispatcher) -> None:
    logger.info("bot finished")


async def main():
    logger.add(
            "../logs/debug.log",
            level="DEBUG",
            format="{time} | {level} | {module}:{function}:{line} | {message}",
            rotation="30 KB",
            compression="zip",
        )
    await set_default_commands(bot)
    await bot.delete_webhook(drop_pending_updates=True)
    dp.include_router(Reservation.router)
    dp.include_router(handlers.router)
    dp.include_router(callbacks.router)

    logger.info("bot started")
    await dp.start_polling(bot)
    logger.info("bot finished")


if __name__ == "__main__":
    asyncio.run(main())
    
