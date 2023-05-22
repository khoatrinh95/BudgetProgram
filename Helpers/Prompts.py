import datetime
from Helpers.CSVHelper import read_csv


def greeting():
    print(
        '''
        ==============================
        |                            |
        |                            |
        |       BUDGET PROGRAM       |
        |                            |
        |             -Khoa Trinh-   |
        ==============================
        
        Hello!
        '''
    )


def end():
    print_break_lines(3)
    print("Thanks for using the Budget Program. You can close this window!")


def prompt_for_file():
    while True:
        file = input("Please drop your bank statement in the window\n")
        try:
            read_csv(file, False)
            return file
        except:
            print("Cannot read file")



def prompt_for_year():
    while True:
        year = input("For which year you want to analyze?\n")
        if check_is_digit(year) and check_is_year(year):
            return year
        else:
            print("Invalid input")


def prompt_for_month():
    while True:
        month = input("For which month you want to analyze?\n")
        if check_is_digit(month) and check_is_month(month):
            return int(month.strip())
        if check_is_month_str(month):
            return check_is_month_str(month)
        print("Invalid input")


def prompt_ok():
    print("Got cha! Let's go!...")
    print_break_lines(4)


def prompt_after_run():
    while True:
        new_file = input("Would you like to run the program again? (y/n)")
        new_file = new_file.lower()
        if new_file == "y" or new_file == "yes":
            return True
        if new_file == "n" or new_file == "no":
            return False
        print("Invalid input")


def print_break_lines(num_of_lines):
    while num_of_lines > 0:
        print(".")
        num_of_lines = num_of_lines - 1


def check_is_digit(input_str):
    return input_str.strip().isdigit()


def check_is_year(input_str):
    year = int(input_str)
    return 1900 <= year <= 3000


def check_is_month(input_str):
    month = int(input_str)
    return 1 <= month <= 12


def check_is_month_str(input_str):
    month_type = "%b"
    while True:
        try:
            datetime_object = datetime.datetime.strptime(input_str.strip(), month_type)
            month_num = datetime_object.month
            return month_num
        except:
            if month_type == "%B":
                break
            month_type = "%B"
