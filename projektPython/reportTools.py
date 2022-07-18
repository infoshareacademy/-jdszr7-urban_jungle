# Contains help-functions for report preparation
import pandas as pd
import drawChart as dc
import ipywidgets as widgets

def getByDepartmentJobRoleLevelAndMonthlyIncome(data: pd.DataFrame, department, job_role, monthly_income=0):
    return data.loc[(data['Department'] == department) & (data['JobRole'] == job_role) & (data['MonthlyIncome'] >= monthly_income)]

def prepareReport(data: pd.DataFrame, user_department, user_job_role, user_monthly_income):

    dc.drawHistogramWithYourPosition(getByDepartmentJobRoleLevelAndMonthlyIncome(data, user_department, user_job_role, 0), "MonthlyIncome", user_monthly_income)
    
    filteredData = getByDepartmentJobRoleLevelAndMonthlyIncome(data, user_department, user_job_role, user_monthly_income)
    dc.drawPyplot(filteredData)
    dc.drawScatterPlot(filteredData['TotalWorkingYears'], filteredData['MonthlyIncome'], filteredData['JobLevel'])
    
def prepare_widgets(data, trigger_function):
    
    output = widgets.Output()
    
    dropdown_dpt = widgets.Dropdown(options = data.Department.unique(), description = 'Department: ')
    dropdown_jr = widgets.Dropdown(options = data.loc[data['Department']==dropdown_dpt.value, 'JobRole'].unique(), description = 'Job Role: ')
    slider_monthly_income = widgets.IntSlider(
        value=10000,
        min=0,
        max=data.loc[(data['Department']==dropdown_dpt.value) & (data['JobRole']==dropdown_jr.value),'MonthlyIncome'].max(),
        step=100,
        description='Monthly Income:',
        disabled=False,
        continuous_update=False,
        orientation='horizontal',
        readout=True,
        readout_format='d'
    )
    
    def trigger_widgets():
        output.clear_output()
        with output:
            trigger_function(data, dropdown_dpt.value, dropdown_jr.value, slider_monthly_income.value)
    def dropdown_dpt_eventhandler(change):
        dropdown_jr.options = data.loc[data['Department']==dropdown_dpt.value, 'JobRole'].unique()
        current_max = data.loc[(data['Department']==dropdown_dpt.value) & (data['JobRole']==dropdown_jr.value),'MonthlyIncome'].max()
        slider_monthly_income.value = current_max
        slider_monthly_income.max = current_max
        trigger_widgets()
    def dropdown_jr_eventhandler(change):
        current_max = data.loc[(data['Department']==dropdown_dpt.value) & (data['JobRole']==dropdown_jr.value),'MonthlyIncome'].max()
        slider_monthly_income.value = current_max
        slider_monthly_income.max = current_max
        trigger_widgets()
    def slider_monthly_income_eventhandler(change):
        trigger_widgets()
        
    dropdown_dpt.observe(dropdown_dpt_eventhandler, names='value')
    dropdown_jr.observe(dropdown_jr_eventhandler, names='value')
    slider_monthly_income.observe(slider_monthly_income_eventhandler, names='value')
    
    input_widgets = widgets.VBox([dropdown_dpt, dropdown_jr, slider_monthly_income])
    display(input_widgets)
    display(output)
    

    
