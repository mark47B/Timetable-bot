from pydantic import BaseModel
import enum


GENERAL_FUNCTIONALITY = {
                 'info': ['Информация'],
                 'timetable': ['Расписание'],
                 'check_free_slots': ['Свободнные слоты', ],
                 'reserve': ['Забронировать', 'Зарезервировать'],
                 'free_my_slots': ['Освободить мои слоты'],
                 }

ADDITIONAL_COMMANDS = {
      'start': ['начать'],
      'cancel': ['отмена'],
}

AVAILABLE_DAYS = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота']
AVAILABLE_DAYS_SHORT = ['ПН', 'ВТ', 'СР', 'ЧТ', 'ПТ', 'СБ']
AVAILABLE_TIME = ['18:00-19:00', '19:00-20:00', '20:00-21:00', '21:00-22:00']

TELEGRAM_LINK = 'https://t.me/' # tg://user?id=


class AGREEMENT(enum.Enum):
    yes = 'да'
    no = 'нет'


# class app_constructions(enum.Enum):
#     NOT_RESERVED = 'Not Reserved'

# Translation (time, day) to excel cell (letter, number)
DAY_TO_LETTER = { d.lower():chr(n+66) for n, d in enumerate(AVAILABLE_DAYS)}
TIME_TO_NUMBER = { t:str(n+2) for n, t in enumerate(AVAILABLE_TIME) }

def convert_day_to_column_letter(day: str):
    return DAY_TO_LETTER[day]

def convert_time_to_row_number(time: str):
    return TIME_TO_NUMBER[time]





class ProfileLink(BaseModel):
    fullname: str
    username: str

    def __len__(self):
        return len(self.fullname)

    def excel_repr(self):
        return f"fullname='{self.fullname}';/nusername='@{self.username}'"

    def __str__(self) -> str:
        return f'<a href="{TELEGRAM_LINK}{self.username}">@{self.username}</a>'


def parse_cell_to_ProfileLink(cell: str) -> ProfileLink:
    parts_of_cell = cell.split("'") # ['fullname=', 'FULLNAME', ';/nusername=', '@USERNAME', '']
    return ProfileLink(fullname=parts_of_cell[1], username=parts_of_cell[3][1:])
