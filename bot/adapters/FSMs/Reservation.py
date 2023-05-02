from aiogram import StatesGroup, Router
from aiogram.dispatcher.filters.state import State
from aiogram.dispatcher.filters import Command
from aiogram.types import Message
from buttons import make_row_keyboard, available_days, available_time
router = Router()


class Reservation(StatesGroup):
    choosing_day = State()
    choosing_time = State()

    async def clear(self) -> None:
        await self.set_state(state=None)
        await self.set_data({})


@router.message(Command("reserve"))
async def cmd_food(message: Message, state: FSMContext):
    await message.answer(
        text="Выберите день: ",
        reply_markup=make_row_keyboard()
    )
    # Устанавливаем пользователю состояние "выбирает название"
    await state.set_state(Reservation.choosing_day)

@router.message(Reservation.choosing_day)
async def day_chosen_incorrectly(message: Message):
    await message.answer(
        text="Некорректный формат! \n\n"
             "Пожалуйста, выберите день из списка ниже:",
        reply_markup=make_row_keyboard(available_days)
    )


@router.message(
    Reservation.choosing_day, 
    F.text.in_(available_days)
)
async def food_chosen(message: Message, state: FSMContext):
    await state.update_data(chosen_day=message.text.lower())
    user_data = await state.get_data()
    await message.answer(
        text=f"Вы выбрали '{user_data['choosing_day']}'. Спасибо. Теперь, пожалуйста, выберите время:",
        reply_markup=make_row_keyboard(available_time)
    )
    await state.set_state(Reservation.choosing_time)


@router.message(Reservation.choosing_time)
async def day_chosen_incorrectly(message: Message):
    await message.answer(
        text="Неправильный формат времени! \n\n"
             "Пожалуйста, выберите один из слотов из списка ниже:",
        reply_markup=make_row_keyboard(available_time)
    )


@router.message(Reservation.choosing_food_size, F.text.in_(available_time))
async def food_size_chosen(message: Message, state: FSMContext):
    user_data = await state.get_data()
    await message.answer(
        text=f"Вы выбрали {message.text.lower()} порцию {user_data['chosen_food']}.\n"
             f"Попробуйте теперь заказать напитки: /drinks",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.clear()


@router.message(OrderFood.choosing_food_size)
async def food_size_chosen_incorrectly(message: Message):
    await message.answer(
        text="Я не знаю такого размера порции.\n\n"
             "Пожалуйста, выберите один из вариантов из списка ниже:",
        reply_markup=make_row_keyboard(available_food_sizes)
    )