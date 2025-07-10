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

# ✅ 白名單：只保留這些職缺名稱關鍵字的職缺
WHITELIST_KEYWORDS = [
    "數據分析", "資料分析", "data analyst", "data analysis", 
    "data analytic", "資料科學", "data scientist",
    "資料工程", "data engineer", "商業分析", "bi", 
    "bi工程師", "bi analyst", "powerbi", "business intelligence",
    "business analyst", "machine learning", "AI分析"
]

# ❌ 黑名單：排除這些明顯不相關的職缺
EXCLUDE_WORDS = ["助理", "客服", "門市", "儲備幹部", "工讀", "講師", "作業員", "行政", "業務", "外包", "設計"]

def is_relevant_job(title):
    title = title.lower()
    return any(good in title for good in WHITELIST_KEYWORDS) and not any(bad in title for bad in EXCLUDE_WORDS)

# ✅ 主爬蟲函式
def get_104_jobs_raw(keyword, max_pages=100):
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://www.104.com.tw/jobs/search/",
    }
    jobs = []
    page = 1

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
    # 👉 關鍵字可只設為 "資料"、"數據"，因為篩選邏輯改由 is_relevant_job 控制
    SEARCH_KEYWORDS = ["數據", "資料", "分析", "data"]

    for kw in SEARCH_KEYWORDS:
        jobs = get_104_jobs_raw(kw, max_pages=100)
        all_jobs.extend(jobs)

    df = pd.DataFrame(all_jobs)

    # ✅ 去除重複職缺（根據職缺名稱、公司名稱、職缺編號）
    df.drop_duplicates(subset=["jobName", "custName", "jobNo"], inplace=True)

    # ✅ 儲存資料
    today = datetime.today().strftime("%Y-%m-%d")
    filename = f"104_jobs_filtered_{today}.csv"
    df.to_csv(filename, index=False, encoding="utf-8-sig")

    print(f"\n🎉 完成！共儲存 {len(df)} 筆符合白名單的職缺 ➜ {filename}")
