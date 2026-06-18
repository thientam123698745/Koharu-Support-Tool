import json

# Config: có export page không có text hay không
export_page_without_text = False  # đổi thành True nếu muốn export page không có text

# Đọc file scene.json
with open("scene.json", "r", encoding="utf-8") as f:
    data = json.load(f)

pages = data["scene"]["pages"]

result = []
for page_id, page_info in pages.items():
    nodes = page_info.get("nodes", {})

    has_text_node = False
    all_translated = True
    render_blob = None  # lưu blob của node rendered nếu có

    for node_id, node_info in nodes.items():
        kind = node_info.get("kind", {})

        # Kiểm tra text node
        text_info = kind.get("text")
        if text_info is not None:
            has_text_node = True
            translation = text_info.get("translation")
            if translation is None:
                all_translated = False

        # Kiểm tra image node với role = rendered
        image_info = kind.get("image")
        if image_info is not None and image_info.get("role") == "rendered":
            render_blob = image_info.get("blob")

    # Quyết định Export cho page
    if has_text_node:
        export_flag = all_translated
    else:
        export_flag = export_page_without_text

    page_entry = {
        "page_id": page_id,
        "name": page_info.get("name"),
        "Export": export_flag
    }

    # Nếu có RenderBlob thì thêm vào output
    if render_blob:
        page_entry["RenderBlob"] = render_blob

    result.append(page_entry)

# Xuất ra file json mới
with open("pages_output.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print("Đã xuất ra file pages_output.json")
