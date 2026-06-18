import json
import requests
import time
import sys

# Lấy port từ tham số dòng lệnh (mặc định 4001 nếu không truyền)
if len(sys.argv) > 1:
    port = sys.argv[1]
else:
    port = "4001"

# Đọc file Expanded_scene.json
with open("Expanded_scene.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# URL động theo port
url = f"http://127.0.0.1:{port}/api/v1/history/apply"

headers = {
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

for page_id, page in data.get("pages", {}).items():
    for node in page.get("nodes", []):
        node_id = node.get("node_id")
        transform = node.get("transform")

        # Bỏ qua nếu không có transform hoặc width/height <= 0
        if not transform:
            continue
        if transform.get("width", 0) <= 0 or transform.get("height", 0) <= 0:
            continue

        payload = {
            "updateNode": {
                "page": page_id,
                "id": node_id,
                "patch": {
                    "transform": {
                        "x": transform.get("x", 0),
                        "y": transform.get("y", 0),
                        "width": transform.get("width", 0),
                        "height": transform.get("height", 0),
                        "rotationDeg": 0
                    },
                    "data": {
                        "text": {
                            "lockLayoutBox": True
                        }
                    }
                }
            }
        }

        response = requests.post(url, headers=headers, json=payload)

        print(f"Page {page_id}, Node {node_id}, Status: {response.status_code}")
        try:
            print("Response:", response.json())
        except Exception:
            print("Response text:", response.text)

        # Chờ 0.1 giây trước khi gửi request tiếp theo
        time.sleep(0.1)

print(f"Script chạy với port: {port}")
