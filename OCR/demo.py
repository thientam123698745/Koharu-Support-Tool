import json
import os
import numpy as np
from PIL import Image
from paddleocr import PaddleOCR
# import paddle
# paddle.set_device('cpu')
# Khởi tạo OCR
ocr = PaddleOCR(use_textline_orientation=True, lang='ch')

# Đường dẫn tới file JSON
file_path = "PageInfor.json"

# Thư mục chứa ảnh gốc
input_dir = "Webp/Source"

# Thư mục lưu kết quả OCR
output_dir = "Webp/OCR"
os.makedirs(output_dir, exist_ok=True)

# Đọc file JSON
with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# Lấy danh sách file trong thư mục input_dir
files = os.listdir(input_dir)
file_map = {os.path.splitext(f)[0]: os.path.join(input_dir, f) for f in files}

# Duyệt qua từng page
for page in data:
    img_name = page.get("name")
    base_name = os.path.splitext(img_name)[0]

    img_path = file_map.get(base_name)
    if not img_path or not os.path.exists(img_path):
        print(f"Không tìm thấy ảnh cho tên: {img_name}")
        continue

    image = Image.open(img_path)

    for idx, tf in enumerate(page.get("textTransforms", [])):
        x, y = tf["x"], tf["y"]
        w, h = tf["width"], tf["height"]

        crop_box = (x, y, x + w, y + h)
        cropped_img = image.crop(crop_box)

        # Chuyển sang numpy array
        cropped_np = np.array(cropped_img)

        # Dùng API mới predict()
        result = ocr.predict(cropped_np)

        texts = []
        if result and result[0]:
            for line in result[0]:
                texts.append(line[1][0])

        output_txt = os.path.join(output_dir, f"{base_name}_block{idx+1}.txt")
        with open(output_txt, "w", encoding="utf-8") as f_out:
            f_out.write("\n".join(texts) if texts else "EMPTY")

        print(f"Đã OCR khối {idx+1} của {img_name}, lưu tại {output_txt}")
