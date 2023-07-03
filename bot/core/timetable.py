from openpyxl import load_workbook, worksheet
from service.store import Excel_interactions, GoogleSheet_interactions
from core.entities import ProfileLink
from config import config

days_nums = {'понедельник': 1, 'вторник': 2, 'среда': 3, 'четверг': 4, 'пятница': 5, 'суббота': 6}
nums_days = {1: 'понедельник', 2: 'вторник', 3: 'среда', 4:'четверг', 5:'пятница', 6: 'суббота'}

available_days = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота']
available_days_short = ['ПН', 'ВТ', 'СР', 'ЧТ', 'ПТ', 'СБ']
available_time = ['18:00-19:00', '19:00-20:00', '20:00-21:00', '21:00-22:00']


INTERACT_WITH_DB = Excel_interactions(config.EXCEL_PATH)
# INTERACT_WITH_DB = GoogleSheet_interactions(CREDENTIALS_FILE=config.SERVICE_ACCOUNT_CREDENTIALS_PATH, spreadsheetId=config.SPREADSHEET_ID)


def get_timetable_pretty(day: int = None) -> str:
    
    # Connect time with whole table
    timetable = [[available_time[n]] + i for n, i in enumerate(INTERACT_WITH_DB.extract(day))]

    # Calculating max length of string
    max_columns = [] # Max length of fields
    for col in zip(*timetable):
        len_el = []
        [len_el.append(len(el)+1) for el in col]
        max_columns.append(max(len_el))
    
    prettyTimetable = str()
    fields = ['Время']
    fields += available_days if day is None else [available_days[day]]

    for column in fields:
        prettyTimetable += f'{column:{max(max_columns)+1}}'
    prettyTimetable += '\n'
    # Head and body separator
    prettyTimetable += f'{"="*max(max_columns)*(len(fields)+1)}'
    # Body of timetable
    prettyTimetable += '\n'
    for el in timetable:
        for cell in el:
            if type(cell) == type(ProfileLink(id='123', fullname='123')): # crutch
                data = f'</code><a href="tg://user?id={cell.id}">{cell.fullname}</a><code>'
                data += ' '*(max(max_columns)+1 - len(cell))
                prettyTimetable += data
            else:
                prettyTimetable += f'{cell:{max(max_columns)+1}}'
        prettyTimetable += '\n'
                
    return '<code>' + prettyTimetable + '</code>'


def put_cell_into_timetable(message: str, position: tuple[str, str]) -> bool:
    INTERACT_WITH_DB.put(message, position)
    return False
