import cv2
import os

# Thư mục chứa ảnh
source_dir = "Webp/Source"
segment_dir = "Webp/Segment"
output_dir = "Webp/Inpaint"

os.makedirs(output_dir, exist_ok=True)

for filename in os.listdir(source_dir):
    if filename.endswith(".webp"):
        # Đọc ảnh gốc và mask
        source_path = os.path.join(source_dir, filename)
        segment_path = os.path.join(segment_dir, filename)

        img = cv2.imread(source_path)
        mask = cv2.imread(segment_path, cv2.IMREAD_GRAYSCALE)

        # Làm mờ biên mask để tránh vết vá quá sắc nét
        mask_blurred = cv2.GaussianBlur(mask, (5, 5), 0)

        # Inpainting với thuật toán TELEA
        result = cv2.inpaint(img, mask_blurred, inpaintRadius=5, flags=cv2.INPAINT_TELEA)

        # Hậu xử lý: làm mịn để đồng bộ màu sắc
        result = cv2.bilateralFilter(result, d=9, sigmaColor=75, sigmaSpace=75)

        # Lưu kết quả dưới dạng PNG
        output_path = os.path.join(output_dir, filename.replace(".webp", ".png"))
        cv2.imwrite(output_path, result)

        print(f"Đã xử lý: {output_path}")
