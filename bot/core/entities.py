from pydantic import BaseModel


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

class ProfileLink(BaseModel):
    id: str
    fullname: str

    def __len__(self):
        return len(self.fullname)
