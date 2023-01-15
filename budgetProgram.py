import pandas as pd
from Helpers import CSVHelper, DFHelper, JsonHelper, ExcelHelper, DateTimeHelper, ExcelStyleHelper, MaintainHelper, Prompts
import constants
from Models.ExcelBook import ExcelBook

# Config
pd.set_option('display.max_rows', None)
# pd.set_option('display.max_columns', None)


# Greetings
Prompts.greeting()

# User input
droppedFile = input("Please drop your bank statement in the window\n")
constants.BANKING_CSV_PATH = droppedFile.strip()
year = input("For which year you want to analyze?\n")
constants.YEAR = int(year.strip())
month = input("For which month you want to analyze?\n")
constants.MONTH = int(month.strip())
print("Got cha! Let's go!...")

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

# Mask account number
DFHelper.updateDFWithoutCondition(df, constants.ACCOUNT_NUMBER, "*********" + df[constants.ACCOUNT_NUMBER].str[-4:])

# Analyze
for category in categories:
    condition = description.apply(lambda d: any([word in d.lower() for word in categoryDict[category]]))
    DFHelper.updateDFOnCondition(df, condition, constants.CATEGORY, category)

# Write result to csv
CSVHelper.writeCsv(df, constants.CSV_RESULT_PATH, False)

# Append result to Excel
excelPath = constants.OUTPUT_EXCEL_PATH
sheetName = "%s-%s" % (year, month)

# Save backup of current Excel sheet
# go through backup folder, see if there's any file older than 60 days -> if yes then delete
# save current file to backup folder
MaintainHelper.createBackupFolder()
MaintainHelper.cleanBackupFolder()
MaintainHelper.saveFileToBackupFolder()

# Append result to Excel
excelBook = ExcelBook(excelPath)
ExcelHelper.writeDfToExcel(df, excelBook, sheetName, 0, 0)

# Add summary at the end of Excel sheet
lastRow = excelBook.book[sheetName].max_row
startRowSummary = lastRow + 3
currentRow = startRowSummary
amountColumnLetter = ExcelHelper.getColumnLetter(df.columns.get_loc(constants.CAD) + 2)  # H
categoryColumnLetter = ExcelHelper.getColumnLetter(df.columns.get_loc(constants.CATEGORY) + 2)  # J
headerStyle = ExcelStyleHelper.registerStyles(excelBook)

# Conditional format
redFillStyle = ExcelStyleHelper.getStyle('redFill')["fill"]
redFill = ExcelStyleHelper.createPatternFill(**redFillStyle)

# Add summary header
ExcelHelper.writeToCell(excelBook, sheetName, cellRow=currentRow, cellColumn=1, value="", cellStyle=constants.STYLE_NAME_HEADER1)
ExcelHelper.writeToCell(excelBook, sheetName, cellRow=currentRow, cellColumn=2, value="SUMMARY", cellStyle=constants.STYLE_NAME_HEADER1)
ExcelHelper.writeToCell(excelBook, sheetName, cellRow=currentRow, cellColumn=3, value="", cellStyle=constants.STYLE_NAME_HEADER1)
currentRow = currentRow + 1

# Add Category, Actual Cost, Projected Cost headers
ExcelHelper.writeToCell(excelBook, sheetName, cellRow=currentRow, cellColumn=1, value="CATEGORY", cellStyle=constants.STYLE_NAME_HEADER3_LEFT)
ExcelHelper.writeToCell(excelBook, sheetName, cellRow=currentRow, cellColumn=2, value="ACTUAL COST", cellStyle=constants.STYLE_NAME_HEADER3_RIGHT)
ExcelHelper.writeToCell(excelBook, sheetName, cellRow=currentRow, cellColumn=3, value="PROJECTED COST", cellStyle=constants.STYLE_NAME_HEADER3_RIGHT)
currentRow = currentRow + 1


for category in categories:
    if category.lower() == constants.IGNORE.lower():
        continue

    # =-1*SUMIF(J2:J<end> , <category> , H2:H<end>)
    formula = f"=-1*SUMIF({categoryColumnLetter}2:{categoryColumnLetter}{lastRow},\"{category}\",{amountColumnLetter}2:{amountColumnLetter}{lastRow})"
    # print(formula)
    ExcelHelper.writeToCell(excelBook, sheetName, cellRow=currentRow, cellColumn=1, value=category.capitalize(), cellStyle=constants.STYLE_NAME_ALIGN_LEFT)
    ExcelHelper.writeToCell(excelBook, sheetName, cellRow=currentRow, cellColumn=2, value=formula, cellStyle=constants.STYLE_NAME_ALIGN_RIGHT)
    ExcelHelper.writeToCell(excelBook, sheetName, cellRow=currentRow, cellColumn=3, value=budgetDict[category], cellStyle=constants.STYLE_NAME_ALIGN_RIGHT)
    comparedCell = ExcelHelper.getColumnLetter(2) + str(currentRow)
    ExcelHelper.comparingConditionalFormatting(excelBook, sheetName, comparedCell, budgetDict[category], None, redFill)
    currentRow = currentRow + 1

# Add Total at end
actualSumFormula = f"=SUM(B{startRowSummary}:B{currentRow-1})"
projectedSumFormula = f"=SUM(C{startRowSummary}:C{currentRow-1})"
ExcelHelper.writeToCell(excelBook, sheetName, cellRow=currentRow, cellColumn=1, value="TOTAL", cellStyle=constants.STYLE_NAME_HEADER2_LEFT)
ExcelHelper.writeToCell(excelBook, sheetName, cellRow=currentRow, cellColumn=2, value=actualSumFormula, cellStyle=constants.STYLE_NAME_HEADER2_RIGHT)
ExcelHelper.writeToCell(excelBook, sheetName, cellRow=currentRow, cellColumn=3, value=projectedSumFormula, cellStyle=constants.STYLE_NAME_HEADER2_RIGHT)

# Format Excel sheet
ExcelHelper.adjustColumnWidth(excelBook, sheetName)

# Clean up Excel sheet
workbook = excelBook.book
sheetNames = workbook.sheetnames
if 'Sheet' in sheetNames:
    std = workbook['Sheet']
    workbook.remove(std)
    workbook.save(excelPath)
print(df)

# TODO: how to let users input their banking statement and it produces an excel sheet outside of the exe
# TODO: how to let users modify their budget categories outside of exe
# TODO: save input category and learn from it


# TODO: [Defect] Intel computers can't run



# command to run pyinstaller
"""
pyinstaller --paths=/Users/khoatrinh/DevSpace/Budget/lib/python3.9/site-packages --add-data Profiles:Profiles --add-data data:data --add-data output:output budgetProgram.py
"""