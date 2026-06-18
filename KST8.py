import requests
from PIL import Image
import io

# Bước 1: chuyển đổi từ webp sang png
input_path = r"output.webp"
output_path = r"output.png"

# mở file webp và lưu thành png
img = Image.open(input_path).convert("RGBA")
img.save(output_path, "PNG")

# Bước 2: gửi file PNG đến API
url = "http://127.0.0.1:4002/api/v1/pages/019ec3c5-6c29-7cf1-8749-8431348709b6/masks/brushInpaint"

headers = {
    "Host": "127.0.0.1:4002",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:151.0) Gecko/20100101 Firefox/151.0",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Referer": "http://127.0.0.1:4002/",
    "Content-Type": "image/png",
    "sentry-trace": "0a4715d362594604a4a444eb915f8e93-bed95829f288e945",
    "baggage": "sentry-environment=production,sentry-release=35f3e6d1a418d9617fd922e2bc865fe5b8fff818,sentry-public_key=8bdbe0ecdeeccd201da90456692824a3,sentry-trace_id=0a4715d362594604a4a444eb915f8e93,sentry-org_id=4511181517815808",
    "Origin": "http://127.0.0.1:4002",
    "Connection": "keep-alive",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "Priority": "u=4"
}

# đọc file PNG dưới dạng binary
with open(output_path, "rb") as f:
    png_data = f.read()

try:
    response = requests.put(url, headers=headers, data=png_data)
    response.raise_for_status()
    print("Status:", response.status_code)
    print("Response:", response.text)
except requests.exceptions.RequestException as e:
    print("Có lỗi khi gửi PUT:", e)
