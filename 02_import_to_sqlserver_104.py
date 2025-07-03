# -*- coding: utf-8 -*-
"""
Created on Tue Jun 17 13:54:23 2025

@author: student
"""
#第一步：安裝套件
#pip install sqlalchemy pyodbc pandas

#第二步：設定 SQL Server 資料庫連線
from sqlalchemy import create_engine
import urllib

# 資料庫連線參數
params = urllib.parse.quote_plus(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=FMPC\\SQLEXPRESS;"  # 例如：'localhost\\SQLEXPRESS' or '192.168.1.100'
    "DATABASE=數據分析職缺_專題;"
    "Trusted_Connection=yes;"
)

# 建立連線
engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")



#第三步：讀取 CSV 或使用 DataFrame 匯入

import pandas as pd

df = pd.read_csv("104_jobs_raw_2025-06-23.csv")  # 檔名請改成你的

#第四步：匯入 SQL Server 資料表

# 將資料匯入 SQL Server 中，若表格不存在就會自動建立
df.to_sql("jobs_104_raw", con=engine, if_exists="replace", index=False)

print("✅ 匯入完成！")
