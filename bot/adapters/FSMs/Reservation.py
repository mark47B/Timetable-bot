from aiogram import Router, F
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters.command import Command
from aiogram.types import Message
from adapters.buttons import make_row_keyboard, available_days, available_time, agreement

from aiogram.types import ReplyKeyboardRemove

from core.timetable import days_nums
from service.store import Excel_interactions, GoogleSheet_interactions
import core.timetable as tt
from ..buttons import get_timetable

from config import config

router = Router()


class Reservation_fsm(StatesGroup):
    day_selection = State()
    time_selection = State()
    acceptance = State()

    async def clear(self) -> None:
        await self.set_state(state=None)
        await self.set_data({})


# Entrypoint handler for 'reserve'
@router.message(Command("reserve"))
async def entrypoint(message: Message, state: FSMContext):
    await message.answer(
        text="Выберите день ",
        reply_markup=make_row_keyboard(available_days)
    )
    await state.set_state(Reservation_fsm.day_selection)


# Handler for day selection
@router.message(
    Reservation_fsm.day_selection,
    F.text.in_(available_days)
)
async def select_day(message: Message, state: FSMContext):
    await state.update_data(day=message.text.lower())
    user_data = await state.get_data()
    await message.answer(
        text=f"Вы выбрали '{user_data['day']}'. Спасибо. Теперь, пожалуйста, выберите время",
        reply_markup=make_row_keyboard(available_time)
    )
    await state.set_state(Reservation_fsm.time_selection)


@router.message(Reservation_fsm.day_selection)
async def incorrect_day(message: Message):
    await message.answer(
        text="Некорректный формат дня недели!  \n\n"
             "Пожалуйста, выберите день из списка ниже:",
        reply_markup=make_row_keyboard(available_days)
    )


@router.message(
    Reservation_fsm.time_selection,
    F.text.in_(available_time)
)
async def select_time(message: Message, state: FSMContext):
    await state.update_data(time=message.text.lower())
    user_data = await state.get_data()
    await message.answer(
        text=f"Вы выбрали день '{user_data['day']}' и время '{user_data['time']}'. Бронируем?",
        reply_markup=make_row_keyboard(agreement)
    )
    await state.set_state(Reservation_fsm.acceptance)


@router.message(Reservation_fsm.time_selection)
async def incorrect_time(message: Message):
    await message.answer(
        text="Неправильный формат времени! \n\n"
             "Пожалуйста, выберите один из слотов из списка ниже:",
        reply_markup=make_row_keyboard(available_time)
    )


@router.message(
    Reservation_fsm.acceptance,
    F.text.in_(agreement)
)
async def final_reservation(message: Message, state: FSMContext):
    if message.text.lower() == 'да':
        user_data = await state.get_data()
        # timetable_xlsx = Excel_interactions(config.EXCEL_PATH)
        timetable_xlsx = GoogleSheet_interactions(CREDENTIALS_FILE=config.SERVICE_ACCOUNT_CREDENTIALS_PATH, spreadsheetId=config.SPREADSHEET_ID)
        # Translation (time, day) to excel cell (letter, number), should be decompose
        day_to_letter= { d.lower():chr(n+66) for n, d in enumerate(available_days)}
        time_to_number = { t:str(n+2) for n, t in enumerate(available_time) }

        pos = (day_to_letter[user_data['day']], time_to_number[user_data['time']])

        user_data = await state.get_data()
        timetable_xlsx.put(data=f'</code><a href="tg://user?id={message.from_user.id}">{message.from_user.full_name}</a><code>', position=pos)
        await message.answer(
            text=f"Время успешно забронировано!",
            reply_markup=ReplyKeyboardRemove()
        )
        await message.answer(tt.get_timetable_pretty(), reply_markup=get_timetable())

    if message.text.lower() =='нет':
        await message.answer(
            text=f"Бронь отменена.",
            reply_markup=ReplyKeyboardRemove()
        )
        await message.answer(tt.get_timetable_pretty(), reply_markup=get_timetable())
    await state.clear()


@router.message(Reservation_fsm.acceptance)
async def incorrect_day(message: Message):
    await message.answer(
        text="Выберите вариант из списка ниже. Бронируем?",
        reply_markup=make_row_keyboard(agreement)
    )
