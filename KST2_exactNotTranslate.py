import json

# đọc file scene.json
with open("scene.json", "r", encoding="utf-8") as f:
    data = json.load(f)

output = []

# duyệt qua tất cả page_id
for page_id, page_data in data["scene"]["pages"].items():
    # duyệt qua tất cả node trong page
    for text_id, node in page_data["nodes"].items():
        # chỉ lấy node có kind.text
        if "kind" in node and "text" in node["kind"]:
            text_content = node["kind"]["text"].get("text", None)
            translation_content = node["kind"]["text"].get("translation", None)
            
            # chỉ lấy những node có translation = None và text_content khác None
            if translation_content is None and text_content is not None:
                output.append({
                    "page_id": page_id,
                    "text_id": text_id,
                    "text": text_content,
                    "translation": translation_content
                })

# lưu ra file JSON
with open("all_texts_NotTranslated.json", "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print(f"Đã xuất {len(output)} đoạn text chưa có translation và có text_content vào all_texts.json")
