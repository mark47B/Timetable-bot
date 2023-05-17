from prettytable import PrettyTable
from openpyxl import load_workbook, worksheet

days_nums = {'Понедельник': 1, 'Вторник': 2, 'Среда': 3, 'Четверг': 4, 'Пятница': 5, 'Суббота': 6}
nums_days = {1: 'Понедельник', 2: 'Вторник', 3: 'Среда', 4:'Четверг', 5:'Пятница', 6: 'Суббота'}

available_days = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота']
available_days_short = ['ПН', 'ВТ', 'СР', 'ЧТ', 'ПТ', 'СБ']
available_time = ['18:00-19:00', '19:00-20:00', '20:00-21:00', '21:00-22:00']

def get_timetable_from_xlsx(filename: str = '/home/jim/Prjoects/github/rehearsal_room_timetable_bot/bot/service/store/Расписание репетиционной комнаты ДКиН Шайба .xlsx') -> worksheet:
    # Здесь будет подгрузка с google_tables
    excel = load_workbook(filename=filename)
    return excel['Лист1']


def get_timetable_pretty(day: int = None) -> PrettyTable:
    timetable_xlsx = get_timetable_from_xlsx()

    table = PrettyTable()
    fields = ['Время']
    fields += available_days if day is None else [available_days[day]]
    table.field_names = fields
    for row in timetable_xlsx.iter_rows(min_row=2, max_col=7, max_row=12):
        row_as_lst = list()
        for n, cell in enumerate(row):
            if day is None or day == n-1 or n == 0:
                row_as_lst.append(cell.value)
        table.add_row(row_as_lst)
    return table


def put_cell_into_timetable(message: str, position: tuple[int, int]) -> bool:
    # Стоит отловить ошибку, если файл не откроется
    if position[0] <= 0 or position[1] <= 0:
        return True
    excel_wb = load_workbook(filename='../service/store/Расписание репетиционной комнаты ДКиН Шайба .xlsx')
    excel_ws = excel_wb['Лист1']
    excel_ws.cell(row=position[0], column=position[1], value=message)
    excel_wb.save('Расписание репетиционной комнаты ДКиН Шайба .xlsx')
    return False
