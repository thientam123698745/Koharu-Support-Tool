import json

# Đọc file JSON
with open("all_texts_NotTranslated.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Thay thế tất cả dấu '：' trong trường "text" bằng '...'
for item in data:
    if "text" in item and item["text"]:
        item["text"] = item["text"].replace("：", "...")

# Ghi lại file JSON đã chỉnh sửa
with open("all_texts_NotTranslated.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
