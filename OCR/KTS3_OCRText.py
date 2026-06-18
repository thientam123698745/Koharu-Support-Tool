import json
import os
from PIL import Image
import numpy as np
import easyocr

# Khởi tạo EasyOCR (tiếng Trung giản thể: 'ch_sim', phồn thể: 'ch_tra')
reader = easyocr.Reader(['ch_tra'])  # hoặc ['ch_tra'] nếu muốn chữ phồn thể

file_path = "PageInfor.json"
input_dir = "Webp/Source"
output_dir = "Webp/OCR"
os.makedirs(output_dir, exist_ok=True)

# Các phần mở rộng ảnh có thể gặp
possible_exts = [".jpg", ".jpeg", ".png", ".webp"]

with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

for page in data:
    base_name = os.path.splitext(page.get("name"))[0]  # chỉ lấy tên gốc, bỏ phần mở rộng
    img_path = None

    # Thử tìm file với nhiều phần mở rộng
    for ext in possible_exts:
        candidate = os.path.join(input_dir, base_name + ext)
        if os.path.exists(candidate):
            img_path = candidate
            break

    if not img_path:
        print(f"Không tìm thấy ảnh cho {base_name} với các phần mở rộng {possible_exts}")
        continue

    image = Image.open(img_path)

    for idx, tf in enumerate(page.get("textTransforms", [])):
        x, y, w, h = tf["x"], tf["y"], tf["width"], tf["height"]
        crop_box = (x, y, x + w, y + h)
        cropped_img = image.crop(crop_box)

        # Chuyển sang numpy array để EasyOCR xử lý
        cropped_np = np.array(cropped_img)

        # OCR với EasyOCR
        result = reader.readtext(cropped_np)
        texts = [text for (_, text, _) in result]
        tf["ocrText"] = texts

        # Lưu ra file txt (tuỳ chọn)
        output_txt = os.path.join(output_dir, f"{base_name}_block{idx+1}.txt")
        with open(output_txt, "w", encoding="utf-8") as f_out:
            f_out.write("\n".join(texts))

        print(f"Đã OCR khối {idx+1} của {base_name}, lưu tại {output_txt}")

# Ghi lại vào JSON
with open(file_path, "w", encoding="utf-8") as f_out:
    json.dump(data, f_out, ensure_ascii=False, indent=2)

print("Đã cập nhật OCR vào PageInfor.json")
