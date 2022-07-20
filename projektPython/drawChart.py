# Script for generating charts based on pandas dataframe

import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

#matplotlib settings
plt.style.use('fivethirtyeight')
plt.rcParams.update({'figure.autolayout': True})
font = {'family' : 'DejaVu Sans',
        'weight' : 'bold',
        'size'   : 22}

matplotlib.rc('font', **font)

__education2description = {1: 'Below College', 2: 'College', 3: 'Bachelor', 4: 'Master', 5: 'Doctor'}
__colors_dict =['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
__figSize = (25,11)
__axis_font_size=35
__labelpad=15
__linewidth=3
__scatter_point_size=700

def drawGroupByAndCount(df: pd.DataFrame, column_names, column_values = None) -> pd.DataFrame:

    if column_values:
        whereStatement = ' & '.join([f"{kolumn_name} == \"{kolumn_value}\"" for kolumn_name, kolumn_value in zip(column_names, column_values)])
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
    fig, ax = plt.subplots(1,2 ,figsize=__figSize)
    size = 1
    
    educationUnique = filteredData['Education'].unique()
    educationCounts = filteredData['Education'].value_counts()
    ax[0].pie(educationCounts, radius=size, 
       labels = [__education2description[e] for e in educationUnique],
       wedgeprops=dict(width=size, edgecolor='w'), autopct='%1.1f%%')
    ax[0].set_title("Education Level")
    
    educationFieldUnique = filteredData['EducationField'].unique()
    educationFieldCounts = filteredData['EducationField'].value_counts()
    ax[1].pie(educationFieldCounts, radius=size,
       labels= educationFieldUnique,
       wedgeprops=dict(width=size, edgecolor='w'), autopct='%1.1f%%')
    ax[1].set_title("Education Field")
    
    plt.show()

def drawHistogramWithYourPosition(filtered_data: pd.DataFrame, column_name: str, your_salary= 0, number_of_bins=10):
    fig, ax = plt.subplots(figsize=__figSize)
    ax.hist(filtered_data[column_name], bins = number_of_bins, facecolor='blue', alpha=0.5, ec='black', linewidth=__linewidth)
    if your_salary > 0:
        plt.axvline(your_salary, color='r', ls='--', linewidth=__linewidth+3)
        plt.legend(["Your Monthly Income"])

    set_x_y_label(ax, 'Monthly Income', 'Number of employees')
    ax.set_title("Monthly Income histogram", fontsize=__axis_font_size)
    plt.show()
    
def drawScatterPlot(x_data, y_data, color_data):
    fig, ax = plt.subplots(figsize=__figSize)
    for (color_number,color) in enumerate(color_data.unique()):
        drawSingleColorScatterPlot(x_data[color_data == color], y_data[color_data == color], color, ax, color_number)
        
    set_x_y_label(ax, x_data.name, y_data.name)
    ax.set_title(f"{x_data.name} to {y_data.name} scatter plot", fontsize=__axis_font_size)
    ax.legend(title=color_data.name ,loc='lower right')
    plt.show()
    
def drawSingleColorScatterPlot(x_data, y_data, color, ax, color_number):
    scatter = ax.scatter(x_data, y_data, s=__scatter_point_size, c=__colors_dict[color_number], alpha=0.5, ec='black', label=color)
    
def set_x_y_label(ax, x_title, y_title):
    ax.set_xlabel(x_title, fontsize=__axis_font_size, labelpad=__labelpad)
    ax.set_ylabel(y_title, fontsize=__axis_font_size, labelpad=__labelpad);

    


