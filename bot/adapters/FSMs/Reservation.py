from aiogram import Router, F
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters.command import Command
from aiogram.types import Message
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import KeyboardButton

from core.entities import AVAILABLE_DAYS, AVAILABLE_TIME, ProfileLink, GENERAL_FUNCTIONALITY, convert_day_to_column_letter, convert_time_to_row_number
from view.timetable import get_pretty_free_slots, get_timetable_pretty
from view.buttons import make_row_keyboard, make_two_columns_keyboard, make_capital_first, make_inline_buttons_for_timetable
from service.store import Excel_interactions, GoogleSheet_interactions

from config import config

router = Router()


class Reservation_fsm(StatesGroup):
    day_selection = State()
    time_selection = State()
    acceptance = State()
    contact_sharing = State()
    tg_sharing = State()
    vk_sharing = State()

    async def clear(self) -> None:
        await self.set_state(state=None)
        await self.set_data({})


# Entrypoint handler for 'reserve'
@router.message(Command("reserve"))
async def entrypoint(message: Message, state: FSMContext):
    await message.answer(
        text="Выберите день ",
        reply_markup=make_row_keyboard(AVAILABLE_DAYS)
    )
    await state.set_state(Reservation_fsm.day_selection)
# Additional options for calling 'Reservation'
router.message.register(entrypoint, F.text.in_(GENERAL_FUNCTIONALITY['reserve']))


# Handler for day selection
@router.message(
    Reservation_fsm.day_selection,
    F.text.in_(AVAILABLE_DAYS)
)
async def select_day(message: Message, state: FSMContext):
    await state.update_data(day=message.text.lower())
    user_data = await state.get_data()
    await message.answer(
        text=f"Вы выбрали '{user_data['day']}'. Спасибо.\n<b>Сейчас, пожалуйста, выберите время</b>",
        reply_markup=make_row_keyboard(AVAILABLE_TIME)
    )
    await state.set_state(Reservation_fsm.time_selection)


@router.message(Reservation_fsm.day_selection)
async def incorrect_day(message: Message):
    await message.answer(
        text="<b>Некорректный формат дня недели!</b> \n\n"
             "Пожалуйста, выберите день из списка ниже:",
        reply_markup=make_row_keyboard(AVAILABLE_DAYS)
    )


@router.message(
    Reservation_fsm.time_selection,
    F.text.in_(AVAILABLE_TIME)
)
async def select_time(message: Message, state: FSMContext):
    await state.update_data(time=message.text.lower())
    user_data = await state.get_data()

    # Decline reservation for reserved slot
    INTERACT_WITH_DB = GoogleSheet_interactions(CREDENTIALS_FILE=config.SERVICE_ACCOUNT_CREDENTIALS_PATH, spreadsheetId=config.SPREADSHEET_ID)
    dict_with_free_slots = INTERACT_WITH_DB.get_free_slots()
    if make_capital_first(user_data['day']) in dict_with_free_slots.keys() and user_data['time'] in dict_with_free_slots[make_capital_first(user_data['day'])] :
        builder = ReplyKeyboardBuilder()
        builder.row(KeyboardButton(text="Отправить Telegram профиль", request_contact=True))
        await message.answer(
            text=f"Вы выбрали день '{user_data['day']}' и время '{user_data['time']}'.\n"
                 "<b>Сейчас поделитесь Вашим контактом в Telegram</b>",
                 reply_markup=builder.as_markup(resize_keyboard=True)
        )
        await state.set_state(Reservation_fsm.contact_sharing)
    else:
        await message.answer(
            text=f"Вы выбрали занятый слот: '{user_data['day']}' и время '{user_data['time']}'.\n"
                 "<b>Пожалуйста, выберите другой слот</b>",
                 reply_markup=make_row_keyboard(AVAILABLE_DAYS)
        )
        await state.clear()
        await state.set_state(Reservation_fsm.day_selection)



@router.message(Reservation_fsm.time_selection)
async def incorrect_time(message: Message):
    await message.answer(
        text="Неправильный формат времени! \n\n"
             "<b>Выберите один из слотов из списка ниже<b>",
        reply_markup=make_row_keyboard(AVAILABLE_TIME)
    )


# Handler for contact sharing
@router.message(
    Reservation_fsm.contact_sharing,
    F.contact,
    F.contact.user_id == F.from_user.id
)
async def select_contact(message: Message, state: FSMContext):
    await state.update_data(username=message.from_user.username)
    user_data = await state.get_data()
    await message.answer(
        text=f"<b>Вы выбрали день:</b> {user_data['day']}\n"
                f"<b>Время:</b> {user_data['time']} \n"
                f"<b>Telegram profile:</b> <a href=\"https://t.me/{message.from_user.username}\">@{message.from_user.username}</a>.\n\n"
                "<b>Бронируем?</b>",
        reply_markup=make_row_keyboard(['Да', 'Нет']),
        disable_web_page_preview=True
    )
    await state.set_state(Reservation_fsm.acceptance)


@router.message(Reservation_fsm.contact_sharing)
async def incorrect_contact(message: Message):
    builder = ReplyKeyboardBuilder()
    builder.row(KeyboardButton(text="Отправить Telegram профиль", request_contact=True))
    await message.answer(
        text="Пожалуйста, поделитесь своим контактом Telegram, чтобы другие музыканты могли с Вами связаться 📲",
        request_contact=True,
        reply_markup=builder.as_markup(resize_keyboard=True)
    )


@router.message(
    Reservation_fsm.acceptance,
    F.text.in_(['Да', 'Нет'])
)
async def final_reservation(message: Message, state: FSMContext):
    if message.text.lower() == 'да':
        user_data = await state.get_data()
        # timetable_xlsx = Excel_interactions(config.EXCEL_PATH)
        session = GoogleSheet_interactions(CREDENTIALS_FILE=config.SERVICE_ACCOUNT_CREDENTIALS_PATH, spreadsheetId=config.SPREADSHEET_ID)

        pos = (convert_day_to_column_letter(user_data['day']), convert_time_to_row_number(user_data['time'])) # pos = (G, 5)

        profile = ProfileLink(username=user_data['username'],
                              fullname=message.from_user.full_name)
        session.put(data=profile, position=pos)
        await message.answer(
            text=f"Время успешно забронировано!",
            reply_markup=make_two_columns_keyboard([command[0] for command in GENERAL_FUNCTIONALITY.values()])
        )

    if message.text.lower() == 'нет':
        await message.answer(
            text=f"Бронь отменена.",
            reply_markup=make_two_columns_keyboard([command[0] for command in GENERAL_FUNCTIONALITY.values()])
        )
    await message.answer(get_timetable_pretty(), reply_markup=make_inline_buttons_for_timetable(), disable_web_page_preview=True)
    await state.clear()


@router.message(Reservation_fsm.acceptance)
async def incorrect_day(message: Message):
    await message.answer(
        text="Выберите вариант из списка ниже. Бронируем?",
        reply_markup=make_row_keyboard(['Да', 'Нет'])
    )
