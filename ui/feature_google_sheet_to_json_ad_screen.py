

from PyQt6.QtWidgets import QVBoxLayout, QPushButton

from base.base_widget import BaseWidget
from utils.check_inter_net import is_internet_available
from utils.token_check import google_login, google_logout


class FeatureGoogleSheetToJsonAdScreen(BaseWidget):
    """Màn hình chung cho tính năng A, B, C có nút quay về Home."""


    def click_convert_online(self):
        if is_internet_available():
            print("Co internet")
            user_info = google_login()
            if user_info is not None:
                print("Da login")
            else:
                print("Login that bai")
        else:
            self.show_message("Không có internet. Vui lòng kiểm tra lại !")


    def click_convert_offline(self):
        google_logout()

    def __init__(self, navigation):
        super().__init__(navigation)
        self.setWindowTitle("Chuyển đổi Google Sheet về Json Ad Pro")
        layout = QVBoxLayout()

        button_convert_online = QPushButton("Chuyển đổi qua link google sheet online")

        button_convert_offline = QPushButton("Chuyển đổi qua file excel offline")

        back_button = QPushButton("Quay về Home")

        layout.addWidget(button_convert_online)
        layout.addWidget(button_convert_offline)
        layout.addWidget(back_button)

        back_button.clicked.connect(lambda: self.navigation.pop_screen())
        button_convert_online.clicked.connect(lambda: self.click_convert_online())
        button_convert_offline.clicked.connect(lambda: self.click_convert_offline())
        self.setLayout(layout)