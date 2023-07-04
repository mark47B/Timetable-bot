from aiogram import Router, F
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters.command import Command
from adapters.buttons import agreement, make_row_keyboard
from config import config
from service.store import GoogleSheet_interactions
from aiogram.types import Message, ReplyKeyboardRemove

from core.entities import ProfileLink


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
        reply_markup=make_row_keyboard(agreement)
    )
    await state.set_state(Free_slot_FSM.acceptance)


@router.message(
    Free_slot_FSM.acceptance,
    F.text.in_(agreement)
)
async def free_slots(message: Message, state: FSMContext):
    user_data = await state.get_data()
    
    for r, row in enumerate(user_data['INTERACT_WITH_DB'].extract()):
        for c, cell in enumerate(row):
            if type(cell) == type(ProfileLink(id='123', fullname='123')) and int(cell.id) == message.from_user.id:
                pos = (chr(c+66), r+2)
                user_data['INTERACT_WITH_DB'].put(position=pos, data=None)

    await message.answer(
        text=f"Ваши слоты успешно очищены",
              reply_markup=ReplyKeyboardRemove()
    )
    await state.clear()


@router.message(Free_slot_FSM.acceptance)
async def incorrect_time(message: Message):
      await message.answer(
        text="Вы действительно хотите освободить все свои слоты?",
        reply_markup=make_row_keyboard(agreement)
    )
