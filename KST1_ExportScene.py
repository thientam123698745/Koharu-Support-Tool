import requests
import json
import sys

# Kiểm tra tham số port từ dòng lệnh
if len(sys.argv) < 2:
    print("Vui lòng nhập port. Ví dụ: python script.py 4001")
    sys.exit(1)

port = sys.argv[1]

url = f"http://127.0.0.1:{port}/api/v1/scene.json"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:151.0) Gecko/20100101 Firefox/151.0",
    "Accept": "*/*",
    "Referer": f"http://127.0.0.1:{port}/",
    "Connection": "keep-alive"
}

try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    # parse JSON
    data = response.json()

    # lưu ra file
    with open("scene.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print("Đã lưu dữ liệu JSON vào scene.json")
except requests.exceptions.RequestException as e:
    print("Có lỗi khi truy cập:", e)
