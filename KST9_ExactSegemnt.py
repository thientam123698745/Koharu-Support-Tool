import json

# Đọc file gốc
with open(r"scene.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Chuẩn bị dữ liệu mới
output = []

for page_id, page in data.get("scene", {}).get("pages", {}).items():
    for node_id, node in page.get("nodes", {}).items():
        node_info = {
            "page_id": page_id,
            "page_name": page.get("name", ""),   # thêm tên trang
            "node_id": node_id,
            "transform": node.get("transform", {}),
            "kind": node.get("kind", {})
        }
        output.append(node_info)

# Lưu ra file JSON mới
with open(r"extracted_nodes.json", "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print("Đã lưu dữ liệu vào extracted_nodes.json")
