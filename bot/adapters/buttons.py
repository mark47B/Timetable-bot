from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton,KeyboardButton, ReplyKeyboardMarkup

available_days = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота']
available_time = ['11:00-12:00', '12:00-13:00', '13:00-14:00', 
                  '14:00-15:00', '15:00-16:00', '16:00-17:00', 
                  '17:00-18:00', '18:00-19:00', '19:00-20:00',
                  '20:00-21:00', '21:00-22:00']


def make_row_keyboard(items: list[str] = available_days) -> ReplyKeyboardMarkup:
    """
    Создаёт реплай-клавиатуру с кнопками в один ряд
    :param items: список текстов для кнопок
    :return: объект реплай-клавиатуры
    """
    row = [KeyboardButton(text=item) for item in items]
    return ReplyKeyboardMarkup(keyboard=[row], resize_keyboard=True)


def get_days_inline() -> InlineKeyboardMarkup:
    btn_days = [InlineKeyboardButton(text=day, callback_data='get_day'+(num+1)) for num, day in enumerate(available_days)]
    return InlineKeyboardMarkup().add(*btn_get_days)

def get_time_inline() -> InlineKeyboardMarkup:
    btn_time = [InlineKeyboardButton(text=day, callback_data='get_time'+(num+1)) for num, day in enumerate(available_time)]
    InlineKeyboardMarkup().add(*btn_time)

btn_get_timetable = InlineKeyboardButton('Получить расписание репетиционной комнаты 🗓', callback_data='get_timetable_btn')
btn_get_days = (InlineKeyboardButton('Понедельник', callback_data='get_day1'),
                InlineKeyboardButton('Вторник', callback_data='get_day2'),
                InlineKeyboardButton('Среда', callback_data='get_day3'),
                InlineKeyboardButton('Четверг', callback_data='get_day4'),
                InlineKeyboardButton('Пятница', callback_data='get_day5'),
                InlineKeyboardButton('Суббота', callback_data='get_day6')
                )
btn_reserve_time = (InlineKeyboardButton('11:00-12:00', callback_data='reserve_time1_day1'),
                    InlineKeyboardButton('12:00-13:00', callback_data='reserve_time2_day1'),
                    InlineKeyboardButton('13:00-14:00', callback_data='reserve_time3_day1'),
                    InlineKeyboardButton('14:00-15:00', callback_data='reserve_time4_day1'),
                    )

inline_timetable = InlineKeyboardMarkup().add(btn_get_timetable)
inline_days = InlineKeyboardMarkup().add(*btn_get_days)
inline_reserve = InlineKeyboardMarkup().row(btn_get_timetable).row(*btn_reserve_time)
