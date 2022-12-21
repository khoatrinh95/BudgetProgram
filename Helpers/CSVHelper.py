import pandas as pd

def readCsv(path, indexCol):
    df = pd.read_csv(path, index_col=indexCol)
    return df

def writeCsv(df, path, indexCol):
    df.to_csv(path, index=indexCol)