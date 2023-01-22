import datetime


def get_first_and_last_date_of_month(year, month):
    date = datetime.date(year, month, 1)
    return date, last_date_of_month(date)


def last_date_of_month(any_day):
    # The day 28 exists in every month. 4 days later, it's always next month
    next_month = any_day.replace(day=28) + datetime.timedelta(days=4)
    # subtracting the number of the current day brings us back one month
    return next_month - datetime.timedelta(days=next_month.day)
