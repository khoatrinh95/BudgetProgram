import os

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
TRANSPORT = "transport"
PHONE = "phone"
SHOPPING = "shopping"
ACTIVITY = "activity"
FOOD = "food"
MOM = "mom"
GROCERY = "grocery"
IGNORE = "ignore"

# STYLE CONFIG
STYLE_NAME = 'name'
STYLE_FONT = 'font'
STYLE_BORDER = 'border'
STYLE_FILL = 'fill'
STYLE_ALIGNMENT = 'alignment'
STYLE_PROTECTION = 'protection'

# PATHS
absolute_path = os.path.dirname(__file__)
WORDS_JSON_PATH = os.path.join(absolute_path, 'data/words.json')
CSV_RESULT_PATH = os.path.join(absolute_path, 'data/output.csv')
STYLE_JSON_PATH = os.path.join(absolute_path, 'data/style.json')
BUDGET_JSON_PATH = os.path.join(absolute_path, 'data/budget.json')

# BUDGET TO COMPARE
BUDGET_TYPE = "ukg"


# INPUT
BANKING_CSV_PATH = os.path.join(absolute_path, 'data/bank/new.csv')
MONTH = 12
YEAR = 2022
OUTPUT_EXCEL_PATH = os.path.join(absolute_path, "output/BUDGETtest.xlsx")