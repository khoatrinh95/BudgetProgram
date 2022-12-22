import pandas as pd
from Helpers import CSVHelper, DFHelper, JsonHelper, ExcelHelper, DateTimeHelper, ExcelStyleHelper
import constants

# Config
from Models.ExcelBook import ExcelBook

pd.set_option('display.max_rows', None)
# pd.set_option('display.max_columns', None)

# Read words json
categoryDict = JsonHelper.readJson(constants.WORDS_JSON_PATH)
categories = categoryDict.keys()

# Read budget json
budgetDict = JsonHelper.readJson(constants.BUDGET_JSON_PATH)[constants.BUDGET_TYPE]

# Read csv
csvPath = constants.BANKING_CSV_PATH
df = CSVHelper.readCsv(csvPath, False)
description = df[constants.DESCRIPTION_ONE]

# Create Category column
DFHelper.createNewColumnWithValue(df, constants.CATEGORY, "")

# Remove non-expense transactions
df = DFHelper.filterDf(df, df[constants.CAD] < 0)

# Convert Transaction Date to proper date format
DFHelper.convertColumnToProperDate(df, constants.TRANSACTION_DATE)

# Filter a specific month
year = constants.YEAR
month = constants.MONTH
firstAndLastDateOfMonth = DateTimeHelper.getFirstAndLastDateOfMonth(year, month)
df = DFHelper.filterDf(df, (df[constants.TRANSACTION_DATE] >= firstAndLastDateOfMonth[0]) & (
            df[constants.TRANSACTION_DATE] <= firstAndLastDateOfMonth[1]))

# Filter to ignore transactions in IGNORE
for word in categoryDict[constants.IGNORE]:
    df = DFHelper.filterDf(df, df[constants.DESCRIPTION_ONE].str.contains(word, case=False) == False)

# Analyze
for category in categories:
    condition = description.apply(lambda d: any([word in d.lower() for word in categoryDict[category]]))
    DFHelper.updateDF(df, condition, constants.CATEGORY, category)

# Write result to csv
CSVHelper.writeCsv(df, constants.CSV_RESULT_PATH, False)

# Append result to Excel
excelPath = constants.OUTPUT_EXCEL_PATH
sheetName = "%s-%s" % (year, month)

# Append result to Excel
excelBook = ExcelBook(excelPath)
ExcelHelper.writeDfToExcel(df, excelBook, sheetName, 0, 0)

# Add summary at the end of Excel sheet
lastRow = excelBook.book[sheetName].max_row
startRowSummary = lastRow + 3
amountColumnLetter = ExcelHelper.getColumnLetter(df.columns.get_loc(constants.CAD) + 2)  # H
categoryColumnLetter = ExcelHelper.getColumnLetter(df.columns.get_loc(constants.CATEGORY) + 2)  # J
headerStyle = ExcelStyleHelper.registerStyles()

# Conditional format
redFill = ExcelStyleHelper.createPatternFill(startColor='EE1111', endColor='EE1111', fillType='solid')
blueFill = ExcelStyleHelper.createPatternFill(startColor='0000CCFF', endColor='0000CCFF', fillType='solid')

for category in categories:
    if category.lower() == constants.IGNORE.lower():
        continue

    # =-1*SUMIF(J2:J<end> , <category> , H2:H<end>)
    formula = f"=-1*SUMIF({categoryColumnLetter}2:{categoryColumnLetter}{lastRow},\"{category}\",{amountColumnLetter}2:{amountColumnLetter}{lastRow})"
    # print(formula)
    ExcelHelper.writeToCell(excelBook, sheetName, cellRow=startRowSummary, cellColumn=1, value=category.upper(), cellStyle="header")
    ExcelHelper.writeToCell(excelBook, sheetName, cellRow=startRowSummary, cellColumn=2, value=formula, cellStyle=None)
    comparedCell = ExcelHelper.getColumnLetter(2) + str(startRowSummary)
    ExcelHelper.comparingConditionalFormatting(excelBook, sheetName, comparedCell, budgetDict[category], blueFill, redFill)
    startRowSummary = startRowSummary + 1

# Format Excel sheet
ExcelHelper.adjustColumnWidth(excelBook, sheetName)


print(df)
