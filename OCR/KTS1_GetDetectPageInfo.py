import json

# Đọc file scene.json
with open("scene.json", "r", encoding="utf-8") as f:
    data = json.load(f)

output = []

# Duyệt qua các page
pages = data.get("scene", {}).get("pages", {})
for page_id, page in pages.items():
    page_info = {
        "pageId": page_id,
        "name": page.get("name"),
        "sourceBlob": None,
        "textTransforms": []
    }
    
    nodes = page.get("nodes", {})
    for node_id, node in nodes.items():
        kind = node.get("kind", {})
        
        # Nếu là image role=source → lấy blob
        if "image" in kind and kind["image"].get("role") == "source":
            page_info["sourceBlob"] = kind["image"].get("blob")
        
        # Nếu là text → lấy transform
        if "text" in kind:
            transform = node.get("transform")
            if transform:
                page_info["textTransforms"].append(transform)
    
    output.append(page_info)

# Lưu ra file json
with open("output.json", "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print("Đã lưu dữ liệu vào output.json")
