import json
import os
import cv2
import numpy as np

inpaint_dir = "Webp/Inpaint"
brush_dir = "Webp/Inpaint2"
json_file = "extracted_nodes.json"

os.makedirs(brush_dir, exist_ok=True)

with open(json_file, "r", encoding="utf-8") as f:
    nodes = json.load(f)

pages = {}
for node in nodes:
    page_name = node.get("page_name")
    transform = node.get("transform")
    kind = node.get("kind", {})
    if "text" in kind:
        base_name = os.path.splitext(page_name)[0]
        pages.setdefault(base_name, []).append(transform)

def find_image(base_name):
    for ext in [".jpg", ".jpeg", ".png", ".webp"]:
        candidate = os.path.join(inpaint_dir, base_name + ext)
        if os.path.exists(candidate):
            return candidate
    return None

for base_name, transforms in pages.items():
    img_path = find_image(base_name)
    if not img_path:
        print(f"Không tìm thấy ảnh cho {base_name}")
        continue

    img = cv2.imread(img_path)
    if img is None:
        print(f"Lỗi đọc ảnh: {img_path}")
        continue

    # Tạo mask cho vùng cần xóa
    mask = np.zeros(img.shape[:2], dtype=np.uint8)

    for transform in transforms:
        x, y, w, h = int(transform["x"]), int(transform["y"]), int(transform["width"]), int(transform["height"])
        mask[y:y+h, x:x+w] = 255  # vùng chữ cần inpaint

    # Dùng inpainting để lấp vùng chữ bằng texture xung quanh
    result = cv2.inpaint(img, mask, inpaintRadius=2, flags=cv2.INPAINT_TELEA)

    out_name = os.path.basename(img_path)
    out_path = os.path.join(brush_dir, out_name)
    cv2.imwrite(out_path, result)
    print(f"Đã xử lý và lưu: {out_path}")