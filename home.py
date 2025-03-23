import sys
import os
import json
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QStackedWidget
from PyQt6.QtCore import Qt
from google_auth_oauthlib.flow import InstalledAppFlow

from utils.encrypt_utils import load_and_decrypt_token
from utils.path_utils import TOKEN_FILE


class HomeWindow(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget

        self.setWindowTitle("Trang chủ")
        self.resize(400, 300)
        self.center_on_screen()

        layout = QVBoxLayout()
        self.label = QLabel("Đang kiểm tra đăng nhập...")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label)

        self.logout_button = QPushButton("Đăng xuất")
        self.logout_button.clicked.connect(self.logout)
        layout.addWidget(self.logout_button)

        self.setLayout(layout)

        # 🔹 Kiểm tra trạng thái đăng nhập ngay khi vào màn hình Home
        self.check_login_status()

    def check_login_status(self):
        token_data = load_and_decrypt_token()
        if token_data:
            self.label.setText("Chào mừng bạn đến Home!")
        else:
            print("Token không hợp lệ hoặc hết hạn. Yêu cầu đăng nhập lại.")
            self.stacked_widget.setCurrentIndex(0)  # Quay lại Login

    def center_on_screen(self):
        screen = QApplication.primaryScreen().geometry()
        self.move(
            (screen.width() - self.width()) // 2,
            (screen.height() - self.height()) // 2
        )
    def logout(self):
        if os.path.exists(TOKEN_FILE):
            os.remove(TOKEN_FILE)  # Xóa token khi đăng xuất
        self.stacked_widget.setCurrentIndex(0)  # Quay lại màn Login