import os
import re
import importlib.util
import subprocess
import sys

def get_imports_from_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()
        # Tìm các dòng import và from ... import ...
        imports = re.findall(r'^\s*(?:import|from)\s+([a-zA-Z0-9_\.]+)', content, re.MULTILINE)
        # Lấy tên module chính (loại bỏ phần sau dấu chấm)
        modules = {imp.split('.')[0] for imp in imports}
        return modules
    except Exception as e:
        print(f"[❌] Lỗi khi đọc file {filepath}: {e}")
        return set()

def is_module_installed(module_name):
    return importlib.util.find_spec(module_name) is not None

def install_module(module_name):
    print(f"[+] Cài đặt thư viện: {module_name}")
    subprocess.check_call([sys.executable, "-m", "pip", "install", module_name])

def main():
    current_file = os.path.abspath(__file__)
    current_dir = os.path.dirname(current_file)
    all_modules = set()

    # Duyệt qua tất cả các file .py trong thư mục hiện tại và các thư mục con
    for root, dirs, files in os.walk(current_dir):
        for filename in files:
            if filename.endswith('.py'):
                filepath = os.path.join(root, filename)
                if os.path.abspath(filepath) == current_file:
                    continue  # bỏ qua file hiện tại
                print(f"[🔍] Đang kiểm tra file: {filepath}")
                modules = get_imports_from_file(filepath)
                all_modules.update(modules)

    # Kiểm tra và cài đặt nếu cần
    for module in sorted(all_modules):
        if not is_module_installed(module):
            try:
                install_module(module)
            except Exception as e:
                print(f"[❌] Không thể cài đặt {module}: {e}")

if __name__ == "__main__":
    main()
