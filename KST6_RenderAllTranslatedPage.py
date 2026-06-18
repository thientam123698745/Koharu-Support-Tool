import json
import requests
import time
import sys

# lấy port từ tham số dòng lệnh
port = sys.argv[1]

url = f"http://127.0.0.1:{port}/api/v1/pipelines"

headers = {
    "Host": f"127.0.0.1:{port}",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:151.0) Gecko/20100101 Firefox/151.0",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Referer": f"http://127.0.0.1:{port}/",
    "Content-Type": "application/json",
    "sentry-trace": "e596457194424d2a919f59e4ec72e4c0-a6f7be93cd2035ea",
    "baggage": "sentry-environment=production,sentry-release=35f3e6d1a418d9617fd922e2bc865fe5b8fff818,sentry-public_key=8bdbe0ecdeeccd201da90456692824a3,sentry-trace_id=e596457194424d2a919f59e4ec72e4c0,sentry-org_id=4511181517815808",
    "Origin": f"http://127.0.0.1:{port}",
    "Connection": "keep-alive",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "Priority": "u=4"
}

# đọc file JSON
with open(r"all_texts_Translated.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# lấy tất cả page_id, loại bỏ trùng lặp
page_ids = {item["page_id"] for item in data if item.get("page_id")}

for page_id in page_ids:
    payload = {
        "steps": ["koharu-renderer"],
        "pages": [page_id]
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        print(f"Đã gửi page_id {page_id}, Status: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Lỗi khi gửi page_id {page_id}: {e}")

    # chờ 0.3 giây trước khi gửi tiếp
    time.sleep(0.3)
