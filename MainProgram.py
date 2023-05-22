import pandas as pd
from Helpers import CSVHelper, DFHelper, JsonHelper, ExcelHelper, DateTimeHelper, ExcelStyleHelper, MaintainHelper, \
    Prompts
import constants
from Models.ExcelBook import ExcelBook

# Config
pd.set_option('display.max_rows', None)
# pd.set_option('display.max_columns', None)

# Read words json
categoryDict = JsonHelper.read_json(constants.WORDS_JSON_PATH)
categories = categoryDict.keys()

# Read budget json
budgetDict = JsonHelper.read_json(constants.BUDGET_JSON_PATH)

# Read income json
incomeDict = JsonHelper.read_json(constants.INCOME_JSON_PATH)

def main_program():
    # Read csv
    csv_path = constants.BANKING_CSV_PATH
    df = CSVHelper.read_csv(csv_path, False)
    description = df[constants.DESCRIPTION_ONE]

    # Create Category column
    DFHelper.create_new_column_with_value(df, constants.CATEGORY, "")

    # Remove transactions with empty amount
    df = DFHelper.filter_df(df, df[constants.CAD].notnull())

    # Remove non-expense transactions
    df[constants.CAD] = pd.to_numeric(df[constants.CAD])
    df = DFHelper.filter_df(df, df[constants.CAD] < 0)

    # Convert Transaction Date to proper date format
    DFHelper.convert_column_to_proper_date(df, constants.TRANSACTION_DATE)

    # Filter a specific month
    year = constants.YEAR
    month = constants.MONTH
    first_and_last_date_of_month = DateTimeHelper.get_first_and_last_date_of_month(year, month)
    df = DFHelper.filter_df(df, (df[constants.TRANSACTION_DATE] >= first_and_last_date_of_month[0]) & (
            df[constants.TRANSACTION_DATE] <= first_and_last_date_of_month[1]))

    # Filter to ignore transactions in IGNORE
    for word in categoryDict[constants.IGNORE]:
        df = DFHelper.filter_df(df, df[constants.DESCRIPTION_ONE].str.contains(word, case=False) == False)

    # Mask account number
    DFHelper.update_df_without_condition(df, constants.ACCOUNT_NUMBER,
                                         "*********" + df[constants.ACCOUNT_NUMBER].str[-4:])

    # Analyze
    for category in categories:
        condition = description.apply(lambda d: any([word.lower() in d.lower() for word in categoryDict[category]]))
        DFHelper.update_df_on_condition(df, condition, constants.CATEGORY, category)

    # Append result to Excel
    excel_path = constants.OUTPUT_EXCEL_PATH
    sheet_name = "%s-%s" % (year, month)

    # Save backup of current Excel sheet
    # go through backup folder, see if there's any file older than 60 days -> if yes then delete
    # save current file to backup folder
    MaintainHelper.create_backup_folder()
    MaintainHelper.clean_backup_folder()
    MaintainHelper.save_file_to_backup_folder()

    # Append result to Excel
    excel_book = ExcelBook(excel_path)
    ExcelHelper.write_df_to_excel(df, excel_book, sheet_name, 0, 0)

    # Add summary at the end of Excel sheet
    last_row = excel_book.book[sheet_name].max_row
    start_row_summary = last_row + 3
    current_row = start_row_summary
    amount_column_letter = ExcelHelper.get_letter_of_column(df.columns.get_loc(constants.CAD) + 2)  # H
    category_column_letter = ExcelHelper.get_letter_of_column(df.columns.get_loc(constants.CATEGORY) + 2)  # J
    ExcelStyleHelper.registerStyles(excel_book)

    # Conditional format
    red_fill_style = ExcelStyleHelper.getStyle('redFill')["fill"]
    red_fill = ExcelStyleHelper.createPatternFill(**red_fill_style)

    # Add summary header
    ExcelHelper.write_to_cell(excel_book, sheet_name, cell_row=current_row, cell_column=constants.FIRST_COLUMN_INDEX, value="",
                              cell_style=constants.STYLE_NAME_HEADER1)
    ExcelHelper.write_to_cell(excel_book, sheet_name, cell_row=current_row, cell_column=constants.SECOND_COLUMN_INDEX, value="SUMMARY",
                              cell_style=constants.STYLE_NAME_HEADER1)
    ExcelHelper.write_to_cell(excel_book, sheet_name, cell_row=current_row, cell_column=constants.THIRD_COLUMN_INDEX, value="",
                              cell_style=constants.STYLE_NAME_HEADER1)
    current_row = current_row + 1

    # Add Category, Actual Cost, Projected Cost headers
    ExcelHelper.write_to_cell(excel_book, sheet_name, cell_row=current_row, cell_column=constants.FIRST_COLUMN_INDEX, value="CATEGORY",
                              cell_style=constants.STYLE_NAME_HEADER3_LEFT)
    ExcelHelper.write_to_cell(excel_book, sheet_name, cell_row=current_row, cell_column=constants.SECOND_COLUMN_INDEX, value="ACTUAL COST",
                              cell_style=constants.STYLE_NAME_HEADER3_RIGHT)
    ExcelHelper.write_to_cell(excel_book, sheet_name, cell_row=current_row, cell_column=constants.THIRD_COLUMN_INDEX, value="PROJECTED COST",
                              cell_style=constants.STYLE_NAME_HEADER3_RIGHT)
    current_row = current_row + 1

    for category in budgetDict:
        if category.lower() == constants.IGNORE.lower():
            continue

        # =-1*SUMIF(J2:J<end> , <category> , H2:H<end>)
        formula = f"=-1*SUMIF({category_column_letter}2:{category_column_letter}{last_row},\"{category}\",{amount_column_letter}2:{amount_column_letter}{last_row})"
        # print(formula)
        ExcelHelper.write_to_cell(excel_book, sheet_name, cell_row=current_row, cell_column=constants.FIRST_COLUMN_INDEX, value=category.capitalize(),
                                  cell_style=constants.STYLE_NAME_ALIGN_LEFT)
        ExcelHelper.write_to_cell(excel_book, sheet_name, cell_row=current_row, cell_column=constants.SECOND_COLUMN_INDEX, value=formula,
                                  cell_style=constants.STYLE_NAME_ALIGN_RIGHT)
        ExcelHelper.write_to_cell(excel_book, sheet_name, cell_row=current_row, cell_column=constants.THIRD_COLUMN_INDEX, value=budgetDict[category],
                                  cell_style=constants.STYLE_NAME_ALIGN_RIGHT)
        compared_cell = ExcelHelper.get_letter_of_column(constants.SECOND_COLUMN_INDEX) + str(current_row)
        ExcelHelper.comparing_conditional_formatting(excel_book, sheet_name, compared_cell, budgetDict[category], None,
                                                     red_fill)
        current_row = current_row + 1

    # Add Total at end
    actual_sum_formula = f"=SUM(B{start_row_summary}:B{current_row - 1})"
    projected_sum_formula = f"=SUM(C{start_row_summary}:C{current_row - 1})"
    ExcelHelper.write_to_cell(excel_book, sheet_name, cell_row=current_row, cell_column=constants.FIRST_COLUMN_INDEX, value="TOTAL",
                              cell_style=constants.STYLE_NAME_HEADER2_LEFT)
    ExcelHelper.write_to_cell(excel_book, sheet_name, cell_row=current_row, cell_column=constants.SECOND_COLUMN_INDEX, value=actual_sum_formula,
                              cell_style=constants.STYLE_NAME_HEADER2_RIGHT)
    ExcelHelper.write_to_cell(excel_book, sheet_name, cell_row=current_row, cell_column=constants.THIRD_COLUMN_INDEX, value=projected_sum_formula,
                              cell_style=constants.STYLE_NAME_HEADER2_RIGHT)
    total_row = current_row
    current_row = current_row + 1

    # Add income at end (only add if user inputs their income in income.json)
    if len(incomeDict) != 0:
        monthly_income = incomeDict[constants.MONTHLY]
        ExcelHelper.write_to_cell(excel_book, sheet_name, cell_row=current_row, cell_column=constants.FIRST_COLUMN_INDEX, value="INCOME",
                                  cell_style=constants.STYLE_NAME_HEADER2_LEFT)
        ExcelHelper.write_to_cell(excel_book, sheet_name, cell_row=current_row, cell_column=constants.SECOND_COLUMN_INDEX, value=monthly_income,
                                  cell_style=constants.STYLE_NAME_HEADER2_RIGHT)
        ExcelHelper.write_to_cell(excel_book, sheet_name, cell_row=current_row, cell_column=constants.THIRD_COLUMN_INDEX, value=monthly_income,
                                  cell_style=constants.STYLE_NAME_HEADER2_RIGHT)
        income_row = current_row
        current_row = current_row + 1

        # Add saving/loss at end
        actual_sum = ExcelHelper.read_cell_formula_without_equal_sign(excel_book, sheet_name, total_row, constants.SECOND_COLUMN_INDEX)
        projected_sum = ExcelHelper.read_cell_formula_without_equal_sign(excel_book, sheet_name, total_row, constants.THIRD_COLUMN_INDEX)
        actual_saving_or_loss = f"=B{income_row}-{actual_sum}"
        projected_saving_or_loss = f"=C{income_row}-{projected_sum}"
        ExcelHelper.write_to_cell(excel_book, sheet_name, cell_row=current_row, cell_column=constants.FIRST_COLUMN_INDEX, value="SAVING/LOSS",
                                  cell_style=constants.STYLE_NAME_HEADER2_LEFT)
        ExcelHelper.write_to_cell(excel_book, sheet_name, cell_row=current_row, cell_column=constants.SECOND_COLUMN_INDEX, value=actual_saving_or_loss,
                                  cell_style=constants.STYLE_NAME_HEADER2_RIGHT)
        ExcelHelper.write_to_cell(excel_book, sheet_name, cell_row=current_row, cell_column=constants.THIRD_COLUMN_INDEX, value=projected_saving_or_loss,
                                  cell_style=constants.STYLE_NAME_HEADER2_RIGHT)
        compared_cell = ExcelHelper.get_letter_of_column(constants.SECOND_COLUMN_INDEX) + str(current_row)
        ExcelHelper.comparing_conditional_formatting(excel_book, sheet_name, compared_cell, 0, red_fill,
                                                     None)


    # Format Excel sheet
    ExcelHelper.adjust_column_width(excel_book, sheet_name)

    # Clean up Excel sheet
    workbook = excel_book.book
    sheet_names = workbook.sheetnames
    if 'Sheet' in sheet_names:
        std = workbook['Sheet']
        workbook.remove(std)
        workbook.save(excel_path)

    Prompts.print_break_lines(3)
    print("Analysis complete. The Excel sheet is saved in the following folder: ", constants.OUTPUT_EXCEL_PATH)


# TODO: implement logging system
# TODO: let user create Profile + their own budget + their budget words
# TODO: save input category and learn from it


# TODO: [Defect] Intel computers can't run


# command to run pyinstaller
"""
pyinstaller --paths=/Users/khoatrinh/DevSpace/Budget/lib/python3.9/site-packages --add-data profiles:profiles --add-data data:data --add-data output:output BudgetProgram.py
"""
