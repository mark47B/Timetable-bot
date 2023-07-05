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
                         "       <i>Информация о реп. точке:</i> /info \n"
                         "       <i>Зарезервировать слот:</i> /reserve \n"
                         "       <i>Освободить все свои слоты:</i> /free_my_slots \n"
                         "       <i>Отмена текущей операции:</i> /cancel \n\n",
                         reply_markup=get_timetable())


@router.message(Command("info"))
async def process_start_command(message: types.Message):
    """
    This handler will be called when user sends `/info`
    """
    await message.answer(
                         "<i>Репетиционная комната находится в здании ДКиН \"Шайба\", кабинет 207</i>\n\n"
                         "Как попасть на реп. точку:\n"
                         "1. <i>Посмотреть свободные слоты</i> \free_slots \n"
                         "2. <i>Забронировать репетиционную комнату</i> \reserve \n"
                         "3. <i>Получить ключ от репетиционной комнаты в кабинете ___</i>\n\n"
                         "Оборудование:\n"
                         "       <i>Барабанная установка(убитый пластик и железо, которое видело распад императорской России</i> \n"
                         "       <i>Гитарный комбик Fender </i> \n"
                         "       <i>Гитарный комбик ___</i>\n"
                         "       <i>Микрофоны (нужно брать в кабинете ___)</i> \n\n"
                         "Перед уходом не забудь:\n"
                         "       <i>Отключить все сетевые фильтры</i> \n"
                         "       <i>Выключить свет</i> \n"
                         ,
                         reply_markup=get_timetable())
