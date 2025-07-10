import requests
import time
import random
import pandas as pd
from datetime import datetime 
import os  

#先F12開啟開發者模式，確認參數
keywords="數據分析"
page=1

url="https://www.104.com.tw/jobs/search/api/jobs"

params={
    "jobsource":"m_joblist_search",
    "keyword":keywords,
    "mode":"s",
    "order":15,
    "page":page,
    "pagesize":20,
}

headers={
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
    "Referer":"https://www.104.com.tw/",
}


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
    title=title.lower()
    return any(good in title for good in WHITELIST_KEYWORDS) and not any(bad in title for bad in EXCLUDE_WORDS)


#開始請求回傳資料

all_data=[]  #將蒐集的資料存在這個空list當中
max_page=20
while page <= max_page:
    try:
        params["page"]=page
        print(f"🔍 抓取「{keywords}」第 {page} 頁")
        response=requests.get(url=url,params=params,headers=headers)
        data=response.json()
        filter_jobs=[job for job in data["data"] if is_relevant_job(job["jobName"])] 
        all_data.extend(filter_jobs)      
        time.sleep(random.uniform(1.5,3.5)) #模擬人操作，隨機時間間隔換頁
        page+=1
    except Exception as e:
        print(e)
        print("錯誤，解析json失敗!!")
        break

#將回傳內容儲存成檔案
df=pd.DataFrame(all_data)  
today=datetime.today().strftime("%Y-%m-%d")
filename=f"104_rawdata_{today}.csv"
folder=r"C:\Users\FM_pc\Desktop\jobs_analysis_project\data"
os.makedirs(folder,exist_ok=True)  #確保資料夾存在，無則建立
df.to_csv(os.path.join(folder,filename),index=False,encoding="utf-8-sig")
print(f"爬蟲完成，儲存成{filename}")
