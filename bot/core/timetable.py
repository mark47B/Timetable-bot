from prettytable import PrettyTable
from openpyxl import load_workbook, worksheet

days_nums = {'Понедельник': 1, 'Вторник': 2, 'Среда': 3, 'Четверг': 4, 'Пятница': 5, 'Суббота': 6}
nums_days = {1: 'Понедельник', 2: 'Вторник', 3: 'Среда', 4:'Четверг', 5:'Пятница', 6: 'Суббота'}

def get_timetable_from_xlsx(filename: str = '../service/store/Расписание репетиционной комнаты ДКиН Шайба .xlsx') -> worksheet:
    # Здесь будет подгрузка с google_tables
    excel = load_workbook(filename=filename)
    return excel['Лист1']


def get_timetable_pretty() -> PrettyTable:
    timetable_xlsx = get_timetable_from_xlsx()

    table = PrettyTable()
    table.field_names = [
        'Время', 'Понедельник', 'Вторник', 'Среда',
        'Четверг', 'Пятница', 'Суббота'
        ]

    for row in timetable_xlsx.iter_rows(min_row=2, max_col=7, max_row=12):
        row_as_lst = list()
        for cell in row:
            row_as_lst.append(cell.value)
        table.add_row(row_as_lst)
    return table


def get_timetable_day_pretty(day: int) -> PrettyTable:
    
    timetable_xlsx = get_timetable_from_xlsx()

    table = PrettyTable()
    table.field_names = [
        'Время', nums_days[day]
        ]

    for row in timetable_xlsx.iter_rows(min_row=2, max_col=7, max_row=12):
        row_as_lst = list()
        for n, cell in enumerate(row):
            if n == day or n == 0:
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






# table = PrettyTable()
# table.field_names = ['Время', 'Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота']

# for row in excel.iter_rows(min_row=2, max_col=7, max_row=12):
#     row_as_lst = list()
#     for cell in row:
#         row_as_lst.append(cell.value)
#     table.add_row(row_as_lst)
#     print('\n')

# print(table)

# Code generator
# for i in range(11, 23):
#     time = datetime.datetime(year=2023, month=2, day=4, hour=i, minute=0, second=0)
#     print('table.add_row([\'', time.time().strftime("%H:%M"),'\', \' \', \' \', \' \', \' \', \' \', \' \'])', sep='')

# table.add_row(['12:00-13:00', ' ', ' ', ' ', ' ', ' ', ' '])
# table.add_row(['13:00-14:00', ' ', ' ', ' ', ' ', ' ', ' '])
# table.add_row(['14:00-15:00', ' ', ' ', ' ', ' ', ' ', ' '])
# table.add_row(['15:00-16:00', ' ', ' ', ' ', ' ', ' ', ' '])
# table.add_row(['16:00-17:00', ' ', ' ', ' ', ' ', ' ', ' '])
# table.add_row(['17:00-18:00', ' ', ' ', ' ', ' ', ' ', ' '])
# table.add_row(['18:00-19:00', ' ', ' ', ' ', ' ', ' ', ' '])
# table.add_row(['19:00-20:00', ' ', ' ', ' ', ' ', ' ', ' '])
# table.add_row(['20:00-21:00', ' ', ' ', ' ', ' ', ' ', ' '])
# table.add_row(['21:00-22:00', ' ', ' ', ' ', ' ', ' ', ' '])
# table.add_row(['22:00-23:00', ' ', ' ', ' ', ' ', ' ', ' '])