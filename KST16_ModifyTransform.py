import json

# tham số tùy chỉnh: nhập số % muốn tăng cho từng chiều
scale_width_percent = 40   # tăng chiều rộng 20%
scale_height_percent = 20  # tăng chiều cao 10%

scale_width_factor = 1 + scale_width_percent / 100.0
scale_height_factor = 1 + scale_height_percent / 100.0

with open("Filtered_scene.json", "r", encoding="utf-8") as f:
    data = json.load(f)

for page_id, page in data.get("pages", {}).items():
    page_width = page.get("width", 0)
    page_height = page.get("height", 0)

    for node in page.get("nodes", []):
        transform = node.get("transform", {})
        x = float(transform.get("x", 0))
        y = float(transform.get("y", 0))
        w = float(transform.get("width", 0))
        h = float(transform.get("height", 0))

        if w <= 0 or h <= 0:
            continue  # bỏ qua node không hợp lệ

        # tăng theo % tùy chỉnh cho từng chiều
        new_w = min(w * scale_width_factor, page_width)
        new_h = min(h * scale_height_factor, page_height)

        dx = (new_w - w) / 2
        dy = (new_h - h) / 2

        new_x = max(0, x - dx)
        new_y = max(0, y - dy)

        # đảm bảo không vượt quá page
        if new_x + new_w > page_width:
            new_x = page_width - new_w
        if new_y + new_h > page_height:
            new_y = page_height - new_h

        # cập nhật transform
        node["transform"]["x"] = new_x
        node["transform"]["y"] = new_y
        node["transform"]["width"] = new_w
        node["transform"]["height"] = new_h

# ghi ra file mới
with open("Expanded_scene.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Đã tạo file Expanded_scene.json với tăng rộng {scale_width_percent}% và cao {scale_height_percent}%")
