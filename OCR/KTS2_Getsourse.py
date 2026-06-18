import json
import requests
import os
import sys

# Lấy port từ tham số dòng lệnh
port = sys.argv[1]

# Đường dẫn tới file JSON
file_path = r"PageInfor.json"

# Thư mục lưu ảnh
output_dir = "Webp/Source"
os.makedirs(output_dir, exist_ok=True)

# Headers cho request (tham chiếu tới port động)
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:151.0) Gecko/20100101 Firefox/151.0",
    "Accept": "*/*",
    "Referer": f"http://127.0.0.1:{port}/",
    "Connection": "keep-alive"
}

# Đọc file JSON
with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# Duyệt qua các node
for node in data:
    blob = node.get("sourceBlob")
    name = node.get("name", blob)  # dùng tên ảnh nếu có, nếu không thì blob

    if blob:
        # Tạo URL từ blob với port động
        url = f"http://127.0.0.1:{port}/api/v1/blobs/{blob}"

        # Gửi request
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        # Lưu ra file .webp
        output_path = os.path.join(output_dir, f"{os.path.splitext(name)[0]}.webp")
        with open(output_path, "wb") as f_out:
            f_out.write(response.content)

        print(f"Đã lưu: {output_path}")
