from loader import dp, bot
from aiogram import types, Router

from ..buttons import get_timetable


from aiogram import types
from aiogram.filters import Command


router = Router()


@router.message(Command("start"))
async def process_start_command(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.answer("Привет!\nЭтот бот поможет тебе забронировать репетиционную комнату и узнать свободные слоты 😉", reply_markup=get_timetable())
