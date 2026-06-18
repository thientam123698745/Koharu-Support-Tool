import json
import asyncio
from googletrans import Translator

async def main():
    with open("all_texts_NotTranslated.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    translator = Translator()

    for item in data:
        if item.get("translation") in (None, "", "null"):
            text_to_translate = item.get("text", "")
            if text_to_translate:
                translated = await translator.translate(text_to_translate, src="zh", dest="en")
                item["translation"] = translated.text
                print(f"{text_to_translate} -> {translated.text}")

    with open("all_texts_Translated.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

asyncio.run(main())
