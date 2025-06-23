# -*- coding: utf-8 -*-
"""
Created on Tue Jun 17 13:07:35 2025

@author: student
"""

import requests
import time
import pandas as pd
from datetime import datetime
from urllib.parse import quote

# 🔍 只抓特定兩個關鍵字
KEYWORDS = ["數據分析", "Data Analytic"]

# ❌ 排除不相關職缺（根據職缺名稱）
EXCLUDE_WORDS = ["助理", "客服", "門市", "儲備幹部", "工讀", "講師", "作業員", "行政", "業務", "外包", "設計"]

def is_relevant_job(title):
    if any(bad in title for bad in EXCLUDE_WORDS):
        return False
    return True

# ✅ 主爬蟲函式（保留所有欄位）
def get_104_jobs_raw(keyword, max_pages=100):
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://www.104.com.tw/jobs/search/",
    }
    jobs = []
    page = 1
    page_size = 20

    while page <= max_pages:
        url = (
            "https://www.104.com.tw/jobs/search/list?"
            f"ro=0&kwop=7&keyword={quote(keyword)}&order=11&asc=0&page={page}&mode=s&jobsource=2018indexpoc"
        )

        print(f"🔍 抓取「{keyword}」第 {page} 頁")
        resp = requests.get(url, headers=headers)
        try:
            data = resp.json()
        except Exception:
            print("⚠️ 無法解析 JSON，跳過")
            break

        if "data" not in data or "list" not in data["data"]:
            print("⚠️ 資料格式錯誤，結束")
            break

        job_list = data["data"]["list"]
        if not job_list:
            print("✅ 無更多職缺")
            break

        today = datetime.today().strftime("%Y-%m-%d")
        for job in job_list:
            title = job.get("jobName", "")
            if is_relevant_job(title):
                job["爬蟲日期"] = today
                jobs.append(job)

        print(f"✅ 第 {page} 頁完成，共累積 {len(jobs)} 筆")
        page += 1
        time.sleep(1)

    return jobs

# ✅ 主流程
if __name__ == "__main__":
    all_jobs = []
    for kw in KEYWORDS:
        jobs = get_104_jobs_raw(kw, max_pages=100)
        all_jobs.extend(jobs)

    df = pd.DataFrame(all_jobs)
    
    # 分類函式
    def classify_job(title):
        title = str(title).lower()
    
        core_keywords = [
            'data analyst', '資料分析', '數據分析', 'data analysis', 
            'bi工程師', 'bi analyst', 'business intelligence', '商業分析'
        ]
    
        applied_keywords = [
            '行銷分析', '營運分析', 'crm分析', '產品分析', '電商分析',
            'marketing analyst', 'operation analyst', 'crm', 'insight'
        ]
    
        unrelated_keywords = [
            '助理', '研究助理', '企劃', '行銷企劃', '行政', '客服',
            'pm', 'sales', '業務', 'driver', '設計', '工讀', '外包'
        ]
    
        if any(k in title for k in core_keywords):
            return 'core'
        elif any(k in title for k in applied_keywords):
            return 'applied'
        elif any(k in title for k in unrelated_keywords):
            return 'unrelated'
        else:
            return 'unknown'
    
    # ✅ 套用分類，增加 job_category 欄位
    df['job_category'] = df['jobName'].apply(classify_job)

    
    df.drop_duplicates(subset=["jobName", "custName", "jobNo"], inplace=True)

    today = datetime.today().strftime("%Y-%m-%d")
    filename = f"104_jobs_raw_{today}.csv"
    df.to_csv(filename, index=False, encoding="utf-8-sig")

    print(f"\n🎉 完成！共儲存 {len(df)} 筆原始職缺資料 ➜ {filename}")

