import requests
from PIL import Image
from io import BytesIO

url = "http://127.0.0.1:4002/api/v1/blobs/275b3ae978a522fd13a4a704174047fd2e141432818c955cc80f23a0e36cf4cf"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:151.0) Gecko/20100101 Firefox/151.0",
    "Accept": "*/*",
    "Referer": "http://127.0.0.1:4001/",
    "Connection": "keep-alive"
}

response = requests.get(url, headers=headers)
response.raise_for_status()

# Lưu ra file
with open("output.webp", "wb") as f:
    f.write(response.content)

# Mở bằng Pillow
image = Image.open(BytesIO(response.content))
image.show()  # hiển thị ảnh
