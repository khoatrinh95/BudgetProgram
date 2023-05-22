import os
import sys


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

# CSV HEADERS
ACCOUNT_TYPE = 'Account Type'
ACCOUNT_NUMBER = 'Account Number'
TRANSACTION_DATE = 'Transaction Date'
CHEQUE_NUMBER = 'Cheque Number'
DESCRIPTION_ONE = 'Description 1'
DESCRIPTION_TWO = 'Description 2'
CAD = 'CAD$'
USD = 'USD$'
CATEGORY = "Category"

# CATEGORIES
IGNORE = "ignore"

# INCOME
MONTHLY = "monthly"

# STYLE CONFIG
STYLE_NAME = 'name'
STYLE_FONT = 'font'
STYLE_BORDER = 'border'
STYLE_FILL = 'fill'
STYLE_ALIGNMENT = 'alignment'
STYLE_PROTECTION = 'protection'
STYLE_NAME_HEADER1 = 'header1'
STYLE_NAME_HEADER2_LEFT = 'header2-left'
STYLE_NAME_HEADER2_RIGHT = 'header2-right'
STYLE_NAME_HEADER3_LEFT = 'header3-left'
STYLE_NAME_HEADER3_RIGHT = 'header3-right'
STYLE_NAME_ALIGN_LEFT = "align-left"
STYLE_NAME_ALIGN_RIGHT = "align-right"

# FOLDER PATHS
absolute_path = os.path.dirname(__file__)
PROFILE_FOLDER_PATH = 'profiles/'
BACKUP_FOLDER_PATH = 'backup/'
DATA_FOLDER_PATH = 'data/'
OUTPUT_FOLDER_PATH = 'output/'

# BUDGET TO COMPARE
BUDGET_PROFILE = "profile1"

# INPUT
MONTH = None
YEAR = None

# CONVERT ALL PATHS TO WORK WITH PYINSTALLER
WORDS_JSON_PATH = resource_path(PROFILE_FOLDER_PATH + BUDGET_PROFILE + '/' + 'words.json')
STYLE_JSON_PATH = resource_path(DATA_FOLDER_PATH + 'style.json')
BUDGET_JSON_PATH = resource_path(PROFILE_FOLDER_PATH + BUDGET_PROFILE + '/' + 'budget.json')
INCOME_JSON_PATH = resource_path(PROFILE_FOLDER_PATH + BUDGET_PROFILE + '/' + 'income.json')
BACKUP_FOLDER_PATH = resource_path(BACKUP_FOLDER_PATH)
OUTPUT_FOLDER_PATH = resource_path(OUTPUT_FOLDER_PATH)
OUTPUT_EXCEL_PATH = resource_path(OUTPUT_FOLDER_PATH + "BUDGET.xlsx")

# SUMMARY TABLE
FIRST_COLUMN_INDEX = 1
SECOND_COLUMN_INDEX = 2
THIRD_COLUMN_INDEX = 3