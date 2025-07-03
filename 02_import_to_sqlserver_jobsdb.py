# -*- coding: utf-8 -*-
"""
Created on Tue Jun 17 13:54:23 2025

@author: student
"""
import pandas as pd
from sqlalchemy import create_engine
import urllib

params = urllib.parse.quote_plus(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=FMPC\\SQLEXPRESS;"
    "DATABASE=數據分析職缺_專題;"
    "Trusted_Connection=yes;"
)

engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")

# 假設你已經有扁平化好的 CSV
df = pd.read_csv("jobsdb_jobs.csv")

df.to_sql("jobsdb_jobs", con=engine, if_exists="replace", index=False)
print("✅ 匯入完成")

