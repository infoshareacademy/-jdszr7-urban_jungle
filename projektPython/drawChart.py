# Script for generating charts based on pandas dataframe

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def drawGroupByAndCount(df: pd.DataFrame, column_names, column_values = None) -> pd.DataFrame:

    if column_values:
        whereStatement = ' & '.join([f"{kolumn_name} == \"{kolumn_value}\"" for kolumn_name, kolumn_value in zip(column_names, column_values)])
        print(whereStatement)
        return df.groupby(list(column_names))[column_names[-1]].agg(['count']).query(whereStatement)
    else:
        return df.groupby(list(column_names))[column_names[-1]].agg(['count'])

def drawFeatureOverTime(df: pd.DataFrame, x: str, y: str):
    fig, ax = plt.subplots()
    plt.title(f"wykres zależności {y} od {x}")
    ax.plot(df.loc[:,[x,y]].groupby(x).agg(['mean']), '-b', label=y)
    ax.set_xlabel(x)
    leg = ax.legend()
