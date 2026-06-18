import requests
from PIL import Image
import json
import os
import sys

# Lấy port từ tham số dòng lệnh (mặc định 4002 nếu không truyền)
if len(sys.argv) > 1:
    port = sys.argv[1]
else:
    port = "4002"

# Đường dẫn thư mục chứa ảnh Webp/Inpaint2
input_dir = "Webp/Inpaint2"
# File JSON chứa danh sách page_id và page_name
json_path = "extracted_nodes.json"

# Đọc file JSON
with open(json_path, "r", encoding="utf-8") as f:
    nodes = json.load(f)

# Lặp qua từng node trong JSON
for node in nodes:
    page_id = node.get("page_id")
    page_name = node.get("page_name")  # ví dụ "99.jpg"
    
    # đổi phần mở rộng sang webp để tìm file gốc
    base_name, _ = os.path.splitext(page_name)
    input_path = os.path.join(input_dir, base_name + ".png")

    if not os.path.exists(input_path):
        print(f"Không tìm thấy file {input_path}, bỏ qua.")
        continue

    # Bước 2: gửi file PNG đến API với port động
    url = f"http://127.0.0.1:{port}/api/v1/pages/{page_id}/masks/brushInpaint"

    headers = {
        "Content-Type": "image/png",
        "User-Agent": "Mozilla/5.0",
        "Accept": "*/*",
        "Connection": "keep-alive",
        "Referer": f"http://127.0.0.1:{port}/"
    }

    with open(input_path, "rb") as f:
        png_data = f.read()

    try:
        response = requests.put(url, headers=headers, data=png_data)
        response.raise_for_status()
        print(f"[{page_name}] Status:", response.status_code)
        print("Response:", response.text)
    except requests.exceptions.RequestException as e:
        print(f"Có lỗi khi gửi PUT cho {page_name}:", e)

print(f"Script chạy với port: {port}")
