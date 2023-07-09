from ..buttons import get_timetable

import core.timetable as tt

from typing import Optional

from aiogram import types, Router
from aiogram.filters.callback_data import CallbackData
from aiogram.filters.text import Text

from loader import bot, dp

from ..buttons import GetTimetableCallbackFactory

router = Router()

@router.callback_query(GetTimetableCallbackFactory.filter())
async def callbacks_get_timetable(
        callback: types.CallbackQuery,
        callback_data: GetTimetableCallbackFactory
):
    day = int(callback_data.day) if callback_data.day is not None else None
    if day is None:
        await callback.message.answer(str(tt.get_free_slots()), reply_markup=get_timetable())
    else:
        await callback.message.answer(str(tt.get_timetable_pretty(day)), reply_markup=get_timetable())
    await callback.answer()
