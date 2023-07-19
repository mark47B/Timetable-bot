from view.timetable import get_pretty_free_slots, get_timetable_pretty
from view.buttons import make_inline_buttons_for_timetable, GetTimetableCallbackFactory

from aiogram import types, Router


router = Router()

@router.callback_query(GetTimetableCallbackFactory.filter())
async def callbacks_get_timetable(
        callback: types.CallbackQuery,
        callback_data: GetTimetableCallbackFactory
):
    day = int(callback_data.day) if callback_data.day is not None else None
    if day is None:
        await callback.message.answer(get_pretty_free_slots(), reply_markup=make_inline_buttons_for_timetable())
    else:
        await callback.message.answer(get_timetable_pretty(day), reply_markup=make_inline_buttons_for_timetable(), disable_web_page_preview=True)
    await callback.answer()
