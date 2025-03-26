from PyQt6.QtCore import pyqtSignal, QThread
from PyQt6.QtWidgets import QVBoxLayout, QPushButton, QLabel, QSizePolicy

from base.base_widget import BaseWidget
from ui.feature_google_sheet_to_json_ad_screen import FeatureGoogleSheetToJsonAdScreen
from utils.check_inter_net import is_internet_available
from utils.token_check import google_login, google_logout, get_user_info2


class LoginThread(QThread):
    login_finished = pyqtSignal(dict)  # Trả về thông tin user

    def run(self):
        if is_internet_available():
            print("Có internet")
            user_info = get_user_info2()
            if user_info is not None:
                print("Đã login")
                self.login_finished.emit(user_info)  # Gửi kết quả về UI
            else:
                print("Login thất bại")
                self.login_finished.emit({})
        else:
            print("Không có internet")
            self.login_finished.emit({})


class FeatureConvertJsonAdScreen(BaseWidget):
    """Màn hình chung cho tính năng A, B, C có nút quay về Home."""

    def click_convert_online(self):
        if is_internet_available():
            print("Co internet")
            user_info = google_login()
            if user_info is not None:
                print("login thanh cong")
                self.navigation.pop_screen()
                # self.navigation.push_screen(FeatureConvertJsonAdScreen)
                self.navigation.push_screen(FeatureGoogleSheetToJsonAdScreen)
            else:
                self.show_message("Đăng nhập thất bại !")
        else:
            self.show_message("Không có internet. Vui lòng kiểm tra lại !")

    def click_convert_offline(self):
        google_logout()

    def click_logout(self):
        google_logout()
        self.navigation.pop_screen()
        self.navigation.push_screen(FeatureConvertJsonAdScreen)

    def __init__(self, navigation):
        super().__init__(navigation)
        self.setWindowTitle("Tạo Json Ad Pro")
        layout = QVBoxLayout()
        self.setFixedSize(500, 300)

        button_convert_online = QPushButton("Google Sheet -> Json")

        button_convert_offline = QPushButton("File Excel -> Json")

        back_button = QPushButton("Quay về Home")


        button_convert_online.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        button_convert_offline.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        back_button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        layout.addWidget(button_convert_online)
        layout.addWidget(button_convert_offline)
        layout.addWidget(back_button)

        back_button.clicked.connect(lambda: self.navigation.pop_screen())
        button_convert_online.clicked.connect(lambda: self.click_convert_online())
        button_convert_offline.clicked.connect(lambda: self.click_convert_offline())

        layout.setSpacing(8)

        # Handle login // logout
        label_login = QLabel("", self)
        label_login.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        def handle_login(user_info):
            if user_info:
                label_login.setText(f"Đã login: {user_info['email']}")
                button_logout = QPushButton("Đăng xuất", self)
                button_logout.clicked.connect(lambda: self.click_logout())
                layout.addWidget(button_logout)
                layout.addWidget(label_login)
            else:
                # label_login.setText("Chưa login")
                print("Chua login")


        if is_internet_available():
            self.login_thread = LoginThread()
            self.login_thread.login_finished.connect(handle_login)
            self.login_thread.start()
        else:
            label_login.setText("Không có internet !")
            layout.addWidget(label_login)

        self.setLayout(layout)


