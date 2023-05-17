from aiogram import Router, F
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters.command import Command
from aiogram.types import Message
from adapters.buttons import make_row_keyboard, available_days, available_time

router = Router()


class Reservation_fsm(StatesGroup):
    choosing_day = State()
    choosing_time = State()

    async def clear(self) -> None:
        await self.set_state(state=None)
        await self.set_data({})


@router.message(Command("reserve"))
async def cmd_food(message: Message, state: FSMContext):
    await message.answer(
        text="Выберите день ",
        reply_markup=make_row_keyboard(available_days)
    )
    await state.set_state(Reservation_fsm.choosing_day)


@router.message(
    Reservation_fsm.choosing_day, 
    F.text.in_(available_days)
)
async def day_chosen(message: Message, state: FSMContext):
    await state.update_data(chosen_day=message.text.lower())
    user_data = await state.get_data()
    await message.answer(
        text=f"Вы выбрали '{user_data['chosen_day']}'\. Спасибо\. Теперь, пожалуйста, выберите время",
        reply_markup=make_row_keyboard(available_time)
    )
    await state.set_state(Reservation_fsm.choosing_time)


@router.message(Reservation_fsm.choosing_day)
async def day_chosen_incorrectly(message: Message):
    await message.answer(
        text="Некорректный формат дня\!  \n\n"
             "Пожалуйста, выберите день из списка ниже:",
        reply_markup=make_row_keyboard(available_days)
    )


@router.message(Reservation_fsm.choosing_time)
async def day_chosen_incorrectly(message: Message):
    await message.answer(
        text="Неправильный формат времени\! \n\n"
             "Пожалуйста, выберите один из слотов из списка ниже:",
        reply_markup=make_row_keyboard(available_time)
    )
