from openpyxl import load_workbook, worksheet, workbook


from core.entities import ProfileLink


class Excel_interactions:
    path: str

    def __init__(self, excel_filename) -> None:
        self.path = excel_filename

    def read_xlsx(self) -> worksheet:
        excel = load_workbook(filename=self.path)
        return excel['Лист1']
    
    def write_xlsx(self) -> workbook.Workbook:
        return load_workbook(filename=self.path)

    def extract(self, day: int = None) -> list[list]:
        timetable_cells = list()

        timetable_xlsx = self.read_xlsx()
        for row in timetable_xlsx.iter_rows(min_row=2, min_col=2, max_col=7, max_row=5):
            row_as_lst = list()
            for n, cell in enumerate(row):
                if day is None or (day == n and day is not None):
                    if "<a" in cell.value:

                        row_as_lst.append(
                            ProfileLink(
                            **{
                                'id': cell.value.split('id=')[1].split('"')[0],
                                'fullname': cell.value.split('</a>')[0].split('">')[1]
                            }))
                    else:
                        row_as_lst.append(cell.value)
            timetable_cells.append(row_as_lst)

        return timetable_cells

    def put(self, data, position: tuple[str, str]) -> worksheet:
        timetable_wb = self.write_xlsx()
        timetable_sheet = timetable_wb['Лист1']

        timetable_sheet[position[0] + position[1]] = data
        timetable_wb.save(self.path)
        return timetable_sheet


class DB_interactions:
    pass
    def extracting_from_excel():

        pass


    def put_to_excel():
        pass

    def put_to_db():
        pass
