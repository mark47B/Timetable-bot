from aiogram import Router, F
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters.command import Command
from config import config
from aiogram.types import Message

from service.store import GoogleSheet_interactions
from view.buttons import make_two_columns_keyboard, make_inline_buttons_for_timetable, make_row_keyboard
from view.timetable import get_timetable_pretty
from core.entities import ProfileLink, GENERAL_FUNCTIONALITY
from adapters.FSMs.common import cmd_cancel


router = Router()

class Free_slot_FSM(StatesGroup):
    acceptance = State()

    async def clear(self) -> None:
        await self.set_state(state=None)
        await self.set_data({})


# Entrypoint handler for 'free_my_slots' FSM
@router.message(Command("free_my_slots"))
async def entrypoint(message: Message, state: FSMContext):
    await state.update_data(INTERACT_WITH_DB=GoogleSheet_interactions(CREDENTIALS_FILE=config.SERVICE_ACCOUNT_CREDENTIALS_PATH, spreadsheetId=config.SPREADSHEET_ID))
    await message.answer(
        text="Вы действительно хотите освободить все свои слоты?",
        reply_markup=make_row_keyboard(['Да', 'Нет'])
    )
    await state.set_state(Free_slot_FSM.acceptance)

# Additional options for calling 'Reservation'
router.message.register(entrypoint, F.text.in_(GENERAL_FUNCTIONALITY['free_my_slots']))


@router.message(
    Free_slot_FSM.acceptance,
    F.text.in_(['Да', ])
)
async def free_slots(message: Message, state: FSMContext):
    user_data = await state.get_data()
    
    for r, row in enumerate(user_data['INTERACT_WITH_DB'].extract()):
        for c, cell in enumerate(row):
            if isinstance(cell, ProfileLink) and cell.username == message.from_user.username:
                pos = (chr(c+66), r+2)
                user_data['INTERACT_WITH_DB'].put(position=pos, data=None)

    await message.answer(
        text=f"Ваши слоты успешно очищены",
              reply_markup=make_two_columns_keyboard([command[0] for command in GENERAL_FUNCTIONALITY.values()])
    )
    await message.answer(get_timetable_pretty(), reply_markup=make_inline_buttons_for_timetable(), disable_web_page_preview=True)
    await state.clear()

router.message.register(cmd_cancel, Free_slot_FSM.acceptance, F.text.in_(['Нет', ]))


@router.message(Free_slot_FSM.acceptance)
async def incorrect_time(message: Message):
      await message.answer(
        text="Вы действительно хотите освободить все свои слоты?",
        reply_markup=make_row_keyboard(['Да', 'Нет'])
        )
