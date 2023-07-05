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
    await message.answer("Привет!\n"
                         "Этот бот поможет тебе забронировать репетиционную комнату и узнать свободные слоты 😉\n\n"
                         "Список команд:\n"
                         "       <i>Перезапуск:</i> /start \n"
                         "       <i>Зарезервировать слот:</i> /reserve \n"
                         "       <i>Освободить все свои слоты:</i> /free_my_slots \n"
                         "       <i>Отмена текущей операции:</i> /cancel \n\n",
                         reply_markup=get_timetable())
