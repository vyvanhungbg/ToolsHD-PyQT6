import sys
import os
import json
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from base.base_widget import BaseWidget
from utils import token_check
from utils.check_inter_net import is_internet_available
from utils.encrypt_utils import encrypt_and_save_token, load_and_decrypt_token


class LoginWindow(BaseWidget):
    def __init__(self, navigation):
        super().__init__(navigation)

        self.setWindowTitle("Đăng nhập bằng Google")
        self.resize(400, 300)
        self.center_on_screen()

        # Layout chính
        layout = QVBoxLayout()

        # Tiêu đề
        self.label = QLabel("Nhấn vào nút dưới để đăng nhập Google")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label)

        # Nút đăng nhập
        self.login_button = QPushButton("Đăng nhập bằng Google")
        self.login_button.clicked.connect(self.google_login)
        layout.addWidget(self.login_button)

        self.setLayout(layout)

    def google_login(self):
        token_data = load_and_decrypt_token()

        if token_data:
            try:
                creds = json.loads(token_data)  # 🔹 Kiểm tra JSON hợp lệ
                access_token = creds.get("access_token")
                if not token_check.is_token_valid(access_token) and is_internet_available():
                    creds = None
            except json.JSONDecodeError:
                print("Token lỗi, yêu cầu đăng nhập lại.")
                creds = None
        else:
            creds = None  # Nếu không có token → Đăng nhập lại

        # 🔹 Nếu chưa có token hợp lệ, yêu cầu người dùng đăng nhập
        if not creds:
            flow = InstalledAppFlow.from_client_secrets_file(
                "environment/client_toolshd.json",
                scopes=["https://www.googleapis.com/auth/spreadsheets.readonly",  # 🔹 Quyền đọc Google Sheets
                        "https://www.googleapis.com/auth/userinfo.email",
                        "openid"]
            )
            creds_obj = flow.run_local_server(port=0)  # ⏳ Chờ người dùng đăng nhập

            # ✅ Kiểm tra nếu đăng nhập thành công
            if creds_obj and creds_obj.token:
                encrypt_and_save_token(creds_obj.to_json())  # 🔒 Lưu token đã mã hóa

                self.label.setText("✅ Đăng nhập thành công!")  # 🎯 Cập nhật UI
            else:
                print("⚠ Đăng nhập thất bại. Thử lại!")
                self.label.setText("❌ Đăng nhập thất bại. Vui lòng thử lại!")

    def center_on_screen(self):
        screen = QApplication.primaryScreen().geometry()
        self.move(
            (screen.width() - self.width()) // 2,
            (screen.height() - self.height()) // 2
        )
