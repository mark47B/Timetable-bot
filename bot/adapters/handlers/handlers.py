from aiogram import types, Router
from aiogram.filters import Command

from aiogram import F


from core.entities import GENERAL_FUNCTIONALITY
from view.timetable import get_timetable_pretty, get_pretty_free_slots
from view.buttons import make_inline_buttons_for_timetable, make_two_columns_keyboard


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
                         "       <i>Свободные слоты:</i> /check_free_slots \n"
                         "       <i>Зарезервировать слот:</i> /reserve \n"
                         "       <i>Освободить все свои слоты:</i> /free_my_slots \n"
                         "       <i>Отмена текущей операции:</i> /cancel \n\n",
                         reply_markup=make_two_columns_keyboard([command[0] for command in GENERAL_FUNCTIONALITY.values()]))


@router.message(Command("info"))
async def process_info_command(message: types.Message):
    """
    This handler will be called when user sends `/info`
    """
    await message.answer(
                         "<i>Репетиционная комната находится в здании ДКиН \"Шайба\", кабинет 207</i>\n\n"
                         "Как попасть на реп. точку:\n"
                         "1. <i>Посмотреть свободные слоты</i> /check_free_slots \n"
                         "2. <i>Забронировать репетиционную комнату</i> /reserve \n"
                         "3. <i>Получить ключ от репетиционной комнаты в кабинете ___</i>\n\n"
                         "Оборудование:\n"
                         "       <i>Барабанная установка</i> \n"
                         "       <i>Гитарный комбик x2 </i> \n"
                         "       <i>Басовый комбик x2 </i>\n"
                         "       <i>Электронные барабаны </i> \n"
                         "       <i>Микрофоны (нужно брать отдельно)</i> \n"
                         "       <i>Микшер (нужно брать отдельно)</i> \n\n"
                         "Перед уходом не забудь:\n"
                         "       <b>Отключить все сетевые фильтры</b> \n"
                         "       <b>Выключить свет</b> \n"
                         ,
                         reply_markup=make_two_columns_keyboard([command[0] for command in GENERAL_FUNCTIONALITY.values()]))
router.message.register(process_info_command, F.text.in_(GENERAL_FUNCTIONALITY['info']))


@router.message(F.text.in_(GENERAL_FUNCTIONALITY['timetable']))
async def get_full_timetable(message: types.Message):
    await message.answer(get_timetable_pretty(), reply_markup=make_inline_buttons_for_timetable(), disable_web_page_preview=True)


@router.message(Command("check_free_slots"))
async def check_free_slots(message: types.Message):
    await message.answer(get_pretty_free_slots(), reply_markup=make_inline_buttons_for_timetable())
router.message.register(check_free_slots, F.text.in_(GENERAL_FUNCTIONALITY['check_free_slots']))