# Script for generating charts based on pandas dataframe

from turtle import color
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np


def drawGroupByAndCount(df: pd.DataFrame, column_names, column_values = None) -> pd.DataFrame:

    if column_values:
        whereStatement = ' & '.join([f"{kolumn_name} == \"{kolumn_value}\"" for kolumn_name, kolumn_value in zip(column_names, column_values)])
        print(whereStatement)
        return df.groupby(list(column_names))[column_names[-1]].agg(['count']).query(whereStatement)
    else:
        return df.groupby(list(column_names))[column_names[-1]].agg(['count'])

def drawFeatureOverTime(df: pd.DataFrame, x: str, y: str):
    data_to_plot = df.loc[:,[x,y]].groupby(x).agg(['mean'])
    fig, ax = plt.subplots()
    plt.title(f"wykres zależności {y} od {x}")
    ax.plot(data_to_plot, '-b', label=y)
    ax.set_xlabel(x)
    ax.set_ylim(ymin=0)
    leg = ax.legend()

def drawHistogramWithYourPosition(filtered_data: pd.DataFrame, column_name: str, your_salary= None, number_of_bins=10):
    plt.hist(filtered_data[column_name], bins = number_of_bins, facecolor='blue', alpha=0.5, ec='black')
    if your_salary:
        plt.axvline(your_salary, color='r')
        plt.legend(["Your Montly income", "Histogram"])
    else:
        plt.legend(["foo"])
    plt.show()

