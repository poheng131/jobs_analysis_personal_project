# -*- coding: utf-8 -*-
"""
Created on Fri Jun 20 13:28:29 2025

@author: student
"""

import pandas as pd
import pyodbc

# 🔌 連接 SQL Server
conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
                      'SERVER=fmpc\SQLEXPRESS;'
                      'DATABASE=104職缺;'
                      'Trusted_Connection=yes;')

# 📥 讀取清理後的資料表
df = pd.read_sql("SELECT jobNo, jobName, description FROM dbo.jobs_104_cleaned", conn)

# 🎯 抽樣 100 筆
df_sample = df.sample(n=100, random_state=42).reset_index(drop=True)

# ➕ 加入標註欄位（預設空白）
df_sample['is_data_analysis_job'] = ''  # 你之後可以填 1=是, 0=否

# 💾 輸出成 Excel 或 CSV
df_sample.to_excel('職缺人工標註樣本.xlsx', index=False)  # Excel
# 或 df_sample.to_csv('職缺人工標註樣本.csv', index=False, encoding='utf-8-sig')
