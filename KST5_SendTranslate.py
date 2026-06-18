import json
import requests
import time
import sys

# lấy port từ tham số dòng lệnh
port = sys.argv[1]

url = f"http://127.0.0.1:{port}/api/v1/history/apply"

headers = {
    "Host": f"127.0.0.1:{port}",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:151.0) Gecko/20100101 Firefox/151.0",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Referer": f"http://127.0.0.1:{port}/",
    "Content-Type": "application/json",
    "Origin": f"http://127.0.0.1:{port}",
    "Connection": "keep-alive",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "Priority": "u=0"
}

# đọc file chứa tất cả text/translation
with open(r"all_texts_translated.json", "r", encoding="utf-8") as f:
    data = json.load(f)

for item in data:
    page_id = item.get("page_id")
    text_id = item.get("text_id")
    translation = item.get("translation")

    # bỏ qua nếu translation null hoặc rỗng
    if not translation or translation == "null":
        continue

    payload = {
        "updateNode": {
            "page": page_id,
            "id": text_id,
            "patch": {
                "data": {
                    "text": {
                        "translation": translation
                    }
                }
            }
        }
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        print(f"Đã gửi {text_id} ({page_id}) -> {translation}")
    except requests.exceptions.RequestException as e:
        print(f"Lỗi khi gửi {text_id}: {e}")

    # chờ 0.2 giây trước khi gửi tiếp
    time.sleep(0.2)
