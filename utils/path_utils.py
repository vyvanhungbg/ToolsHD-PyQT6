import os
import appdirs

APP_NAME = "MyApp"
TOKEN_FILE = os.path.join(appdirs.user_data_dir(APP_NAME), "token.enc")
KEY_FILE = os.path.join(appdirs.user_data_dir(APP_NAME), "key.key")

# Tạo thư mục nếu chưa có
os.makedirs(os.path.dirname(TOKEN_FILE), exist_ok=True)


CONFIG_FILE = "environment/client_toolshd.json"
TOKEN_URL = "https://oauth2.googleapis.com/token"