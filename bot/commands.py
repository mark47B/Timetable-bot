from aiogram import Dispatcher
from aiogram import types


async def set_default_commands(dp: Dispatcher) -> None:
    await dp.bot.set_my_commands(
        [
            types.BotCommand("help", "help"),
            types.BotCommand("start", "start"),
            types.BotCommand("Забронировать", "reserve"),
        ]
    )
