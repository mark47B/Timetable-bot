from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder, KeyboardButton, ReplyKeyboardMarkup

from typing import Optional
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import KeyboardButton

from core.entities import GENERAL_FUNCTIONALITY, AVAILABLE_DAYS, AVAILABLE_DAYS_SHORT


class GetTimetableCallbackFactory(CallbackData, prefix='get_timetable'):
    day: Optional[int]


def make_capital_first(word: str):
    return chr(ord(word[0])-32) + word[1:]


def make_two_columns_keyboard(items: list[str]) -> ReplyKeyboardMarkup:
    """
    Creating reply keyboard with two columns of buttons
    """
    builder = ReplyKeyboardBuilder()
    for button in items:
        builder.add(KeyboardButton(text=button))
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)


def make_row_keyboard(items: list[str] = AVAILABLE_DAYS_SHORT) -> ReplyKeyboardMarkup:
    """
    Creating reply-keyboard with buttons if row
    :items: list of labels of buttons
    """
    row = [KeyboardButton(text=item) for item in items]
    return ReplyKeyboardMarkup(keyboard=[row], resize_keyboard=True)


def make_inline_buttons_for_timetable() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    for n, day in enumerate(AVAILABLE_DAYS):
        builder.button(text=day, callback_data=GetTimetableCallbackFactory(day=n))
    builder.button(text='Свободные слоты 🆓', callback_data=GetTimetableCallbackFactory())
    # builder.button(text='Полное расписание репетиционной комнаты 🗓', callback_data=GetTimetableCallbackFactory())
    builder.adjust(3)
    return builder.as_markup(resize_keyboard=True)
