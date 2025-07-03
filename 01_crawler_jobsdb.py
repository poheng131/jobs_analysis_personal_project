import requests
import csv
import time

def fetch_jobs_list_format(keyword="data analysis", pages=10):
    all_jobs = []
    base_url = "https://hk.jobsdb.com/api/jobsearch/v5/search"

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json"
    }

    for page in range(1, pages + 1):
        print(f"正在抓取第 {page} 頁...")
        params = {
            "siteKey": "HK-Main",
            "page": page,
            "keywords": keyword,
            "pageSize": 32,
            "locale": "en-HK"
        }

        response = requests.get(base_url, params=params, headers=headers)
        if response.status_code != 200:
            print(f"第 {page} 頁請求失敗，狀態碼：{response.status_code}")
            continue

        data = response.json()
        print(f"第{page}頁回傳資料型態：", type(data))

        raw_data = data.get("data", [])

        if isinstance(raw_data, dict):
            jobs = raw_data.get("jobs", [])
        elif isinstance(raw_data, list):
            jobs = raw_data
        else:
            jobs = []


        all_jobs.extend(jobs)
        time.sleep(1)

    return all_jobs


def save_jobs_to_csv(jobs, filename="jobsdb_jobs.csv"):
    if not jobs:
        print("沒有資料可存")
        return

    # 根據實際欄位調整
    fieldnames = ["id", "title", "companyName", "listingDate", "locations", "salaryLabel", "teaser"]

    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for job in jobs:
            location = ""
            if job.get("locations"):
                location = job["locations"][0].get("label", "")
            writer.writerow({
                "id": job.get("id", ""),
                "title": job.get("title", ""),
                "companyName": job.get("companyName", ""),
                "listingDate": job.get("listingDate", ""),
                "locations": location,
                "salaryLabel": job.get("salaryLabel", ""),
                "teaser": job.get("teaser", "")
            })

    print(f"✅ 已存檔 {filename}")

if __name__ == "__main__":
    jobs = fetch_jobs_list_format(keyword="data analysis", pages=10)
    save_jobs_to_csv(jobs)
