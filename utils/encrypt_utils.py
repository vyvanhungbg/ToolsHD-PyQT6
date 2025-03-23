import json
import os

from cryptography.fernet import Fernet

from utils.path_utils import KEY_FILE, TOKEN_FILE


def generate_key():
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as key_file:
            key_file.write(key)


def load_key():
    with open(KEY_FILE, "rb") as key_file:
        return key_file.read()


def encrypt_and_save_token(token_data):
    generate_key()  # Đảm bảo có key
    key = load_key()
    cipher = Fernet(key)
    encrypted_token = cipher.encrypt(token_data.encode())

    with open(TOKEN_FILE, "wb") as token_file:
        token_file.write(encrypted_token)

def load_and_decrypt_token():
    if not os.path.exists(TOKEN_FILE):
        return None  # 🔹 Không có file → Yêu cầu đăng nhập lại

    key = load_key()
    cipher = Fernet(key)

    try:
        with open(TOKEN_FILE, "rb") as token_file:
            encrypted_token = token_file.read()

        if not encrypted_token:  # 🔹 File trống
            return None

        decrypted_token = cipher.decrypt(encrypted_token).decode()

        # 🔹 Kiểm tra xem nội dung có phải JSON hợp lệ không
        try:
            json.loads(decrypted_token)  # Kiểm tra JSON
            return decrypted_token
        except json.JSONDecodeError:
            return None  # Dữ liệu lỗi → Yêu cầu đăng nhập lại

    except Exception as e:
        print(f"Lỗi khi đọc token: {e}")
        return None  # Nếu lỗi xảy ra, coi như chưa đăng nhập

