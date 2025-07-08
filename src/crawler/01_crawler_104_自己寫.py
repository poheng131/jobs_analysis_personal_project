import requests
import time
import random

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


#開始請求回傳資料

all_data=[]  #將蒐集的資料存在這個空list當中
max_page=1
while page <= max_page:
    try:
        response=requests.get(url=url,params=params,headers=headers)
        data=response.json()
        all_data.extend(data["data"])     #因為104回傳的json格式是  {"data": [ { 
        time.sleep(random.uniform(1.5,3.5)) #模擬人操作，隨機時間間隔換頁
        page+=1
    except Exception as e:
        print(e)
        print("錯誤，解析json失敗!!")
        break
