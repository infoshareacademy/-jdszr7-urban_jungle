# Contains help-functions for report preparation
import pandas as pd
import drawChart as dc

def getByDepartmentJobRoleLevelAndMonthlyIncome(data: pd.DataFrame, department, job_role, job_level, monthly_income):
    return data.loc[(data['Department'] == department) & (data['JobRole'] == job_role) & (data['JobLevel'] == job_level) & (data['MonthlyIncome'] > monthly_income)]

def prepareReport(data: pd.DataFrame, user_department, user_job_role, user_job_level, user_monthly_income):
    filteredData = getByDepartmentJobRoleLevelAndMonthlyIncome(data, user_department, user_job_role, user_job_level, user_monthly_income)
    dc.drawHistogramWithYourPosition(data, "MonthlyIncome", user_monthly_income)
    dc.drawPyplot(filteredData)
    

    
