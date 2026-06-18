import json

# Đọc file scene.json
with open("scene.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Giá trị transform mặc định cần bỏ qua
default_transform = {
    "x": 0.0,
    "y": 0.0,
    "width": 0.0,
    "height": 0.0,
    "rotationDeg": 0.0
}

def normalize_transform(t):
    return {
        "x": float(t.get("x", 0)),
        "y": float(t.get("y", 0)),
        "width": float(t.get("width", 0)),
        "height": float(t.get("height", 0)),
        "rotationDeg": float(t.get("rotationDeg", 0)),
    }

output_pages = {}

for page_id, page in data.get("scene", {}).get("pages", {}).items():
    page_info = {
        "page_id": page_id,
        "width": page.get("width"),
        "height": page.get("height"),
        "nodes": []
    }
    for node_id, node in page.get("nodes", {}).items():
        transform = normalize_transform(node.get("transform", {}))
        # chỉ giữ node hợp lệ
        if transform != default_transform:
            node_info = {
                "node_id": node_id,
                "transform": transform
            }
            page_info["nodes"].append(node_info)
    output_pages[page_id] = page_info

# Tạo dữ liệu mới
output_data = {"pages": output_pages}

# Lưu ra file JSON riêng
with open("Filtered_scene.json", "w", encoding="utf-8") as f:
    json.dump(output_data, f, ensure_ascii=False, indent=2)

print("Đã tạo file Filtered_scene.json")
