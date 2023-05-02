from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage

import asyncio
import uvloop  # running only linux

from config import config


asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

storage = MemoryStorage()
bot = Bot(token=config.bot_token.get_secret_value(), parse_mode=types.ParseMode.MARKDOWN_V2)
loop = asyncio.get_event_loop()
dp = Dispatcher(bot, loop=loop, storage=storage)
