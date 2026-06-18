import json
import requests
from PIL import Image
from io import BytesIO
import os
import sys

# Lấy port từ tham số dòng lệnh (mặc định 4002 nếu không truyền)
if len(sys.argv) > 1:
    port = sys.argv[1]
else:
    port = "4002"

# Đường dẫn tới file JSON
file_path = r"extracted_nodes.json"

# Thư mục lưu ảnh
output_dir = "Webp/Segment"
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
    kind = node.get("kind", {})
    mask = kind.get("mask")
    if mask and mask.get("role") == "segment":
        blob = mask.get("blob")
        # Lấy name nếu có, nếu không thì fallback sang page_name
        name = mask.get("name")
        if not name:
            name = node.get("page_name", blob)

        # Tạo URL từ blob với port động
        url = f"http://127.0.0.1:{port}/api/v1/blobs/{blob}"

        # Gửi request
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        # Lưu ra file .webp
        output_path = os.path.join(output_dir, f"{os.path.splitext(name)[0]}.webp")
        with open(output_path, "wb") as f_out:
            f_out.write(response.content)

        # # Mở bằng Pillow (tuỳ chọn)
        # mask_obj = Image.open(BytesIO(response.content))
        # mask_obj.show()

        print(f"Đã lưu: {output_path}")

print(f"Script chạy với port: {port}")
