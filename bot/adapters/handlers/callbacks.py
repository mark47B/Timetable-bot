from buttons import inline_days, inline_reserve, inline_timetable
import bot as tt

from aiogram import types

from loader import bot, dp

# Необходимо переписать через фабрику callback-ов

@dp.callback_query_handler(lambda c: c.data == 'get_timetable_btn')
async def process_callback_button1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, '`' + str(tt.get_timetable_pretty()) + '`', parse_mode="MarkdownV2", reply_markup=inline_days)


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('get_day'))
async def process_callback_day(callback_query: types.CallbackQuery):
    day = callback_query.data[-1]
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, '`' + str(tt.get_timetable_day_pretty(int(day))) + '`', parse_mode="MarkdownV2", reply_markup=inline_reserve)


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('reserve_time'))
async def process_callback_reserve(callback_query: types.CallbackQuery):
    reserve_time = int(callback_query.data[-6]) + 1
    reserve_day = int(callback_query[-1])
    tt.put_cell_into_timetable(message='Reserved', position=(reserve_time, 2))
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, '`' + str(tt.get_timetable_pretty()) + '`', parse_mode="MarkdownV2", reply_markup=inline_timetable)
