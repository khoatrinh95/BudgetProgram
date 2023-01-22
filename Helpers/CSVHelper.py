import pandas as pd


def read_csv(path, index_col):
    df = pd.read_csv(path, index_col=index_col)
    return df


def write_csv(df, path, index_col):
    df.to_csv(path, index=index_col)