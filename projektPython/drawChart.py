# Script for generating charts based on pandas dataframe

from turtle import color
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

__education2description = {1: 'podstawówka', 2: 'level2', 3: 'level3', 4: 'level4', 5: 'level5'}

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
    
def drawPyplot(filteredData):
    fig, ax = plt.subplots(figsize=(24,12))
    size = 0.3
    
    innerUnique = filteredData['Education'].unique()
    innerCounts = filteredData['Education'].value_counts()
    texts_inner, autotexts_inner = ax.pie(innerCounts, radius=size, 
       labels = innerUnique,
       wedgeprops=dict(width=size, edgecolor='w'))
    
    outerUnique = filteredData.groupby(['EducationField', 'Education']).size().index
    outerCounts = filteredData.groupby(['EducationField', 'Education']).size()
    ax.pie(outerCounts, radius=1-size,
       labels=[index[0] for index in outerUnique],
       autopct='%1.1f%%',
       wedgeprops=dict(width=size, edgecolor='w'))
    
    ax.legend([__education2description[level] for level in innerUnique],
          title="Eductaion level",
          loc="center left",
          bbox_to_anchor=(1, 0, 2, 1))

    ax.set(aspect="equal", title='Pie plot with `ax.pie`')
    plt.show()

def drawHistogramWithYourPosition(filtered_data: pd.DataFrame, column_name: str, your_salary= None, number_of_bins=10):
    plt.hist(filtered_data[column_name], bins = number_of_bins, facecolor='blue', alpha=0.5, ec='black')
    if your_salary:
        plt.axvline(your_salary, color='r')
        plt.legend(["Your Montly income", "Histogram"])
    else:
        plt.legend(["foo"])
    plt.show()
    

