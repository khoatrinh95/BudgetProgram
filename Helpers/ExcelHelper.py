import pandas as pd
from openpyxl.formatting.rule import CellIsRule
from openpyxl.utils import get_column_letter

def writeDfToExcel(df, excelBook, sheetName, startRow, startCol):
    book = excelBook.book
    path = excelBook.path
    with pd.ExcelWriter(path, engine='openpyxl') as writer:
        writer.book = book
        try:
            writer.book.remove(writer.book[sheetName])
            print("Worksheet: ", sheetName, " already existed")
            print("Deleting old sheet to save new one ...")
        except:
            print("Saving new worksheet: ", sheetName)
        finally:
            df.to_excel(writer, sheet_name=sheetName, startrow=startRow, startcol=startCol, engine='openpyxl')


def adjustColumnWidth(excelBook, sheetName):
    path = excelBook.path
    book = excelBook.book
    with pd.ExcelWriter(path, engine='openpyxl') as writer:
        writer.book = book
        # Auto-adjust columns' width
        sheet = book[sheetName]
        for column_cells in sheet.columns:
            new_column_length = max(len(str(cell.value)) for cell in column_cells)
            new_column_letter = (get_column_letter(column_cells[0].column))
            if new_column_length > 0:
                sheet.column_dimensions[new_column_letter].width = new_column_length * 1.23

def insertRows(excelBook, sheetName, insertRowIndex, numOfRows):
    path = excelBook.path
    book = excelBook.book
    with pd.ExcelWriter(path, engine='openpyxl') as writer:
        writer.book = book
        ws = excelBook.book[sheetName]
        while numOfRows > 0:
            ws.insert_rows(insertRowIndex)
            numOfRows = numOfRows - 1

def insertRowsAtEnd(excelBook, sheetName, numOfRows):
    path = excelBook.path
    book = excelBook.book
    ws = excelBook.book[sheetName]
    insertRowIndex = ws.max_row + 1
    with pd.ExcelWriter(path, engine='openpyxl') as writer:
        writer.book = book
        while numOfRows > 0:
            ws.insert_rows(insertRowIndex)
            numOfRows = numOfRows - 1

def writeToCell(excelBook, sheetName, cellRow, cellColumn, value, cellStyle):
    path = excelBook.path
    book = excelBook.book
    ws = excelBook.book[sheetName]
    with pd.ExcelWriter(path, engine='openpyxl') as writer:
        writer.book = book
        cell = ws.cell(row=cellRow, column=cellColumn, value=value)
        if cellStyle:
            cell.style = cellStyle

def getColumnLetter(index):
    return get_column_letter(index)

def comparingConditionalFormatting(excelBook, sheetName, comparedCell, comparingCell, positiveFill, negativeFill):
    ws = excelBook.book[sheetName]
    ws.conditional_formatting.add(comparedCell, CellIsRule(operator='greaterThan', formula=[comparingCell], fill=negativeFill))
    ws.conditional_formatting.add(comparedCell, CellIsRule(operator='lessThan', formula=[comparingCell], fill=positiveFill))