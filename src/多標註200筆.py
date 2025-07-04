# -*- coding: utf-8 -*-
"""
Created on Mon Jun 23 11:55:56 2025

@author: student
"""

import pandas as pd
import pyodbc

# 一、讀取你之前標註過的 Excel
annotated_df = pd.read_excel("職缺人工標註樣本.xlsx")
annotated_jobNos = annotated_df['jobNo'].astype(str).tolist()

# 二、連接 SQL Server
conn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=fmpc\\SQLEXPRESS;'
    'DATABASE=104職缺;'
    'Trusted_Connection=yes;'
)

# 三、從資料庫中排除已標職缺後，隨機抽取 200 筆
query = f"""
SELECT TOP 200 jobNo, jobName, description
FROM dbo.jobs_104_cleaned
WHERE jobNo NOT IN ({','.join(['?'] * len(annotated_jobNos))})
ORDER BY NEWID()
"""
df_new_sample = pd.read_sql(query, conn, params=annotated_jobNos)

# 四、加上空白標籤欄位
df_new_sample['is_data_analysis_job'] = ''

# 五、輸出成 Excel
df_new_sample.to_excel("職缺人工標註樣本_額外200筆.xlsx", index=False)
