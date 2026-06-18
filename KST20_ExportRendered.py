import json
import os
import requests
import sys

# Lấy port từ tham số dòng lệnh
port = sys.argv[1]

# Đọc file JSON
with open("pages_output.json", "r", encoding="utf-8") as f:
    pages = json.load(f)

# Tạo thư mục Export nếu chưa có
os.makedirs("Export", exist_ok=True)

# Headers cho request
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:151.0) Gecko/20100101 Firefox/151.0",
    "Accept": "*/*",
    "Referer": f"http://127.0.0.1:{port}/",
    "Connection": "keep-alive"
}

# Lặp qua từng trang
for page in pages:
    if page.get("Export"):
        blob = page["RenderBlob"]
        name = page["name"]
        url = f"http://127.0.0.1:{port}/api/v1/blobs/{blob}"

        print(f"Đang export {name} từ {url}...")

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()

            # Lưu file vào thư mục Export
            filepath = os.path.join("Export", name)
            with open(filepath, "wb") as f:
                f.write(response.content)

            print(f"✔ Đã lưu {filepath}")
        except Exception as e:
            print(f"✘ Lỗi khi export {name}: {e}")
    else:
        print(f"Bỏ qua {page['name']} (Export = false)")
