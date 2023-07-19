from openpyxl import load_workbook, worksheet
from service.store import GoogleSheet_interactions
from core.entities import ProfileLink, AVAILABLE_DAYS, AVAILABLE_TIME, TELEGRAM_LINK
from config import config


# INTERACT_WITH_DB = Excel_interactions(config.EXCEL_PATH)
INTERACT_WITH_DB = GoogleSheet_interactions(CREDENTIALS_FILE=config.SERVICE_ACCOUNT_CREDENTIALS_PATH, spreadsheetId=config.SPREADSHEET_ID)


def calc_max_len_of_string_in_list(items: list[str]):
    # Calculating max length of string
    max_column_len = list()
    for col in zip(*items):
        len_el = []
        [len_el.append(len(el)+1) for el in col]
        max_column_len.append(max(len_el))
    return max_column_len


def make_excellent_table(fields, data, row_sep=None) -> str:
    # Creating an aligned table 
    table = str()

    max_column_len = calc_max_len_of_string_in_list(fields + data)

    # Head of table
    for n, column in enumerate(fields):
        table += f'{column:{max_column_len[n]+1}}'
    table += '\n'

    # Separator between Head and body
    table += f'{"="*sum(max_column_len) + "="*5}'
    table += '\n'

    # Body of timetable
    for el in data:
        for n, cell in enumerate(el):
            if isinstance(cell, ProfileLink):
                excellent_cell = f'</code>{str(cell)}<code>' # Close visual block, insert link to person and close
                excellent_cell += ' '*(max_column_len[n] - len(cell.username) + 1) # Add space before str. max_len - len of fullname
                table += excellent_cell
            else:
                table += f'{cell:{max_column_len[n]+1}}'
        if row_sep is not None:
            table += '\n'
            table += f'{row_sep*sum(max_column_len) + row_sep*5}'
        table += '\n'
    return '<code>' + table + '</code>'


def get_timetable_pretty(day: int = None) -> str:
    """
    Generate pretty timetable
    """
    # Add AVAILABLE_TIME to data
    timetable_data = [[AVAILABLE_TIME[n]] + i for n, i in enumerate(INTERACT_WITH_DB.extract(day))]
    fields = ['Время']
    fields += AVAILABLE_DAYS if day is None else [AVAILABLE_DAYS[day]]

    return make_excellent_table(fields=fields, data=timetable_data)


def get_pretty_free_slots() -> str:
    """
    return free slots in pretty view
    """
    # Searching free slots
    free_slots = INTERACT_WITH_DB.get_free_slots()

    fields = ['День', 'Время']

    # Construct list for table from dict with free slots day:[time]
    table_data = list()
    for day_, time_ in free_slots.items():
        table_data.append([day_, time_[0]])
        for time_item in time_[1:]:
            table_data.append(['', time_item])

    return make_excellent_table(fields, table_data, row_sep='-')
