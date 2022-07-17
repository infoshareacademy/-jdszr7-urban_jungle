# Contains help-functions for report preparation
import pandas as pd

def getByDepartmentJobRoleLevelAndMonthlyIncome(data: pd.DataFrame, department, job_role, job_level, monthly_income):
    return data.loc[(data['Department'] == department) & (data['JobRole'] == job_role) & (data['JobLevel'] == job_level) & (data['MonthlyIncome'] > monthly_income)]
