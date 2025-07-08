import requests

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


#開始請求資料

response=requests.get(url=url,params=params,headers=headers)
data=response.json()
print(data)