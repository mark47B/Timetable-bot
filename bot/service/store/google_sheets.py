from pydantic import SecretStr
import apiclient
from oauth2client.service_account import ServiceAccountCredentials
import httplib2

from .store import Store_interaction
from core.entities import AVAILABLE_DAYS, AVAILABLE_TIME, ProfileLink, parse_cell_to_ProfileLink


class GoogleSheet_interactions(Store_interaction):
    spreadsheetId: str
    service: apiclient
    credentials: SecretStr

    def __init__(self, CREDENTIALS_FILE: str, spreadsheetId: str):
        self.spreadsheetId = spreadsheetId

        # Auth
        self.credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive'])
        httpAuth = self.credentials.authorize(httplib2.Http())
        self.service = apiclient.discovery.build('sheets', 'v4', http = httpAuth)

    def __create_table__(self):
        spreadsheet = self.service.spreadsheets().create(body = {'properties': {'title': 'Первый тестовый документ', 'locale': 'ru_RU'}, 
                                                            'sheets': [{'properties': {'sheetType': 'GRID',
                                                            'sheetId': 0,
                                                            'title': 'Лист номер один',
                                                            'gridProperties': {'rowCount': 100, 'columnCount': 15}}}]
                                                            }).execute()
        spreadsheetId = spreadsheet['spreadsheetId'] # Don't forget save spreadsheetID!
    
    def __create_sheet(self):
        # Create a sheet
        results = self.service.spreadsheets().batchUpdate(
            spreadsheetId = self.spreadsheetId,
            body = 
        {
        "requests": [
            {
            "addSheet": {
                "properties": {
                "title": "Another_list",
                "gridProperties": {
                    "rowCount": 20,
                    "columnCount": 12
                }
                }
            }
            }
        ]
        }).execute()
    
    def __get_list_of_sheets(self):
        # Get list of sheets, Id and name
        spreadsheet = self.service.spreadsheets().get(spreadsheetId = spreadsheetId).execute()
        sheetList = spreadsheet.get('sheets')
        # for sheet in sheetList:
        #     print(sheet['properties']['sheetId'], sheet['properties']['title'])
            
        sheetId = sheetList[0]['properties']['sheetId']
        return sheetList

    def __grant_permission(self, email: str):
        driveService = apiclient.discovery.build('drive', 'v3', http = httpAuth)
        driveService.permissions().create(fileId = self.spreadsheetId, body = {
            'type': 'user',
            'role': 'writer',
            'emailAddress': email
            }, fields = 'id').execute()

    def extract(self, day: int = None):
        if day is None:
            ranges = ["Лист 1!B2:G5"]
        else:
            ranges = [f"Лист 1!{chr(day+66)}2:{chr(day+66)}5"]

        results = self.service.spreadsheets().values().batchGet(spreadsheetId = self.spreadsheetId,
                                            ranges = ranges,
                                            dateTimeRenderOption = 'FORMATTED_STRING').execute()
        sheet_values = results['valueRanges'][0]['values']
        timetable_cells = list()
        for row in sheet_values:
            row_as_lst = list()
            for cell in row:
                if "username='@" in cell:
                    # tg_userId='';tg_fullName='';
                    row_as_lst.append(parse_cell_to_ProfileLink(cell))
                else:
                    row_as_lst.append(cell)
            timetable_cells.append(row_as_lst)
        return timetable_cells

    def put(self, data: ProfileLink, position: tuple[str, str]):
        if data is None:
            data = 'Not Reserved'
        else:
            data = data.excel_repr()
        
        results = self.service.spreadsheets().values().batchUpdate(spreadsheetId = self.spreadsheetId, body = {
        "valueInputOption": "USER_ENTERED", # Data is perceived as user input (the value of formulas is considered)
        "data": [
            {"range": f"Лист 1!{position[0]}{position[1]}",
            "majorDimension": "ROWS",     # First fill rows, and then columns
            "values": [
                        [data, ]
                    ]}
        ]
        }).execute()

    def get_free_slots(self) -> dict:
        whole_timetable = self.extract()

        free_slots = dict()
        for number_row, row in enumerate(whole_timetable):
            for number_column, cell in enumerate(row):
                if cell == 'Not Reserved':
                    if AVAILABLE_DAYS[number_column] in free_slots.keys():
                        free_slots[AVAILABLE_DAYS[number_column]] += [AVAILABLE_TIME[number_row] ]
                    else:
                        free_slots[AVAILABLE_DAYS[number_column]] = [AVAILABLE_TIME[number_row] ]
        return free_slots


