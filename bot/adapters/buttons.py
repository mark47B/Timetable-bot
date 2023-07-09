from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup, ReplyKeyboardBuilder, KeyboardButton, ReplyKeyboardMarkup

from typing import Optional
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import KeyboardButton, InlineKeyboardButton

from core.entities import GENERAL_FUNCTIONALITY


class GetTimetableCallbackFactory(CallbackData, prefix='get_timetable'):
    day: Optional[int]


available_days = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота']
available_days_short = ['ПН', 'ВТ', 'СР', 'ЧТ', 'ПТ', 'СБ']
available_time = ['18:00-19:00', '19:00-20:00', '20:00-21:00', '21:00-22:00']
agreement = ['Да', 'Нет']


def capital_first(word: str): # only ru
    return chr(ord(word[0])-32) + word[1:]


def get_commands() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    for v in GENERAL_FUNCTIONALITY.values():
        builder.add(KeyboardButton(text=v[0]))
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)


def make_row_keyboard(items: list[str] = available_days_short) -> ReplyKeyboardMarkup:
    """
    Создаёт реплай-клавиатуру с кнопками в один ряд
    :param items: список текстов для кнопок
    :return: объект реплай-клавиатуры
    """
    row = [KeyboardButton(text=item) for item in items]
    return ReplyKeyboardMarkup(keyboard=[row], resize_keyboard=True)


def get_timetable() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for n, day in enumerate(available_days):
        builder.button(text=day, callback_data=GetTimetableCallbackFactory(day=n))
    builder.button(text='Свободные слоты 🆓', callback_data=GetTimetableCallbackFactory())
    # builder.button(text='Полное расписание репетиционной комнаты 🗓', callback_data=GetTimetableCallbackFactory())
    builder.adjust(3)
    return builder.as_markup()

