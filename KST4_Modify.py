import json
import re

def capitalize_sentences(text: str) -> str:
    # Viết hoa ký tự đầu tiên nếu là chữ thường
    text = text.strip()
    if text and text[0].isalpha():
        text = text[0].upper() + text[1:]

    # Viết hoa ký tự sau \n, ., !, ?
    def repl(match):
        return match.group(0)[0] + " " + match.group(1).upper()

    # regex tìm dấu kết thúc câu + chữ cái thường ngay sau
    text = re.sub(r'([\.\!\?\n])\s*([a-z])', repl, text)
    return text

# đọc file JSON
with open(r"all_texts_Translated.json", "r", encoding="utf-8") as f:
    data = json.load(f)

for item in data:
    translation = item.get("translation")
    if translation:
        # thay thế dấu ':' bằng '...' và nếu sau đó là chữ thì thêm khoảng trắng
        new_translation = re.sub(r":([A-Za-z])", r"... \1", translation)
        new_translation = new_translation.replace(":", "...")
        new_translation = new_translation.replace("Ming", "Uhm")

        # chuẩn hóa chữ hoa đầu câu và sau dấu ngắt
        new_translation = capitalize_sentences(new_translation)

        item["translation"] = new_translation

# ghi lại file
with open(r"all_texts_Translated.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Đã cập nhật translation: thay dấu ':' và chuẩn hóa chữ hoa đầu câu.")
