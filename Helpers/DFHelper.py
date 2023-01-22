import pandas as pd


def create_new_column_with_value(df, column_name, value):
    df[column_name] = value


def filter_df(df, condition):
    df = df[condition]
    return df


def convert_column_to_proper_date(df, column_name):
    df[column_name] = pd.to_datetime(df[column_name]).dt.date


def update_df_on_condition(df, condition, column_name, value):
    df.loc[condition, column_name] = value


def update_df_without_condition(df, column_name, value):
    df.loc[:, column_name] = value
