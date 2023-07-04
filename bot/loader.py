from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.strategy import FSMStrategy

import asyncio
import uvloop

from config import config


asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

storage = MemoryStorage()
bot = Bot(token=config.BOT_TOKEN.get_secret_value(), parse_mode="HTML")
loop = asyncio.get_event_loop()
dp = Dispatcher(loop=loop, storage=storage,  fsm_strategy=FSMStrategy.USER_IN_CHAT)
