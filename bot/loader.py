from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.strategy import FSMStrategy
from redis.asyncio.client import Redis

import asyncio
import uvloop

from config import config


asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

storage = MemoryStorage()
# storage = RedisStorage(redis=Redis(host=config.REDIS_HOSTS, port=config.REDIS_PORT, db=0))

bot = Bot(token=config.BOT_TOKEN.get_secret_value(), parse_mode="HTML")
loop = asyncio.get_event_loop()
dp = Dispatcher(loop=loop,
                storage=storage,
                fsm_strategy=FSMStrategy.USER_IN_CHAT)

# db = Database(
#     name=config.PG_NAME,
#     user=config.PG_USER,
#     password=config.PG_PASSWORD,
#     host=config.PG_HOST,
#     port=config.PG_PORT,
#     loop=loop,
# )