from aiogram import Router
from aiogram.filters import Command, Text
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from view.buttons import make_two_columns_keyboard
from core.entities import GENERAL_FUNCTIONALITY

router = Router()


@router.message(Command(commands=["cancel"]))
@router.message(Text(text="отмена", ignore_case=True))
async def cmd_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text="Действие отменено",
        reply_markup=make_two_columns_keyboard([command[0] for command in GENERAL_FUNCTIONALITY.values()])
    )