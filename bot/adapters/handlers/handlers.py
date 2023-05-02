from loader import dp, bot
from aiogram import types

import bot as tt

from buttons import inline_days, inline_timetable


from aiogram import types


@dp.message_handler(commands="start")
async def process_start_command(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply("Привет\\!\n Этот бот поможет тебе забронировать репетиционную комнату и узнать свободные слоты 😉", reply_markup=inline_timetable)

@dp.message_handler(commands="reserve")
async def process_start_command(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply("Привет\\!\n Этот бот поможет тебе забронировать репетиционную комнату и узнать свободные слоты 😉", reply_markup=inline_timetable)
