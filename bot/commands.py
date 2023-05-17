from aiogram import Bot
from aiogram.types import BotCommand


async def set_default_commands(bot: Bot) -> None:
    await bot.set_my_commands(commands=
        [
            BotCommand(command="help", description="help"),
            BotCommand(command="start", description="start"),
            BotCommand(command="reserve", description="Забронировать"),
        ]
    )
