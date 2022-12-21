from openpyxl import load_workbook

class ExcelBook:
    def __init__(self, path):
        self.path = path
        self.book = load_workbook(path)


