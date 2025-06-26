import requests
from bs4 import BeautifulSoup

url=r"https://sg.jobsdb.com/j?sp=search&trigger_source=serp&q=data+analytics&l=" #網址尚不確定是否正確
headers={
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"
}
resp=requests.get(url,headers=headers)
soup=BeautifulSoup(resp.text,"lxml")

