import pandas as pd

def createNewColumnWithValue(df, columnName, value):
    df[columnName] = value

def filterDf(df, condition):
    df = df[condition]
    return df

def convertColumnToProperDate(df, columnName):
    df[columnName] = pd.to_datetime(df[columnName]).dt.date

def updateDFOnCondition(df, condition, columnName, value):
    df.loc[condition, columnName] = value

def updateDFWithoutCondition(df, columnName, value):
    df.loc[:, columnName] = value