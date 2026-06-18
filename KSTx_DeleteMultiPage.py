import json
import requests
import sys

# Lấy port từ tham số dòng lệnh
port = 4000

# Cấu hình khoảng page cần xóa
START_PAGE = 1
END_PAGE = 151

url = f"http://127.0.0.1:{port}/api/v1/history/apply"

headers = {
    "Host": f"127.0.0.1:{port}",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:151.0) Gecko/20100101 Firefox/151.0",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Referer": f"http://127.0.0.1:{port}/",
    "Content-Type": "application/json",
    "sentry-trace": "f0d51a9a6cf842109be6a71a1a7e6c48-966b159c6925134e",
    "baggage": "sentry-environment=production,sentry-release=35f3e6d1a418d9617fd922e2bc865fe5b8fff818,sentry-public_key=8bdbe0ecdeeccd201da90456692824a3,sentry-trace_id=f0d51a9a6cf842109be6a71a1a7e6c48,sentry-org_id=4511181517815808",
    "Origin": f"http://127.0.0.1:{port}",
    "Connection": "keep-alive",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "Priority": "u=0"
}

# Đọc file scene.json
with open("scene.json", "r", encoding="utf-8") as f:
    data = json.load(f)

pages = list(data["scene"]["pages"].values())

# Lặp qua các page trong khoảng cần xóa
for idx in range(START_PAGE - 1, END_PAGE):
    page = pages[idx]
    page_id = page["id"]

    payload = {
        "removePage": {
            "id": page_id,
            "prev_page": page,   # giữ nguyên thông tin page trước khi xóa
            "prev_index": idx
        }
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        print(f"Đã xóa page {idx+1} (id={page_id}) - Status:", response.status_code)
    except requests.exceptions.RequestException as e:
        print(f"Lỗi khi xóa page {idx+1} (id={page_id}):", e)
