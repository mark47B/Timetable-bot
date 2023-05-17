from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

import asyncio
import uvloop

from config import config


asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

storage = MemoryStorage()
bot = Bot(token=config.BOT_TOKEN.get_secret_value(), parse_mode="markdownv2")
loop = asyncio.get_event_loop()
dp = Dispatcher(loop=loop, storage=storage)
