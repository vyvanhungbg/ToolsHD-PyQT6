import json
import string
import sys
import pandas as pd
import gspread
from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton,
    QLineEdit, QTableView, QHBoxLayout, QLabel, QMessageBox, QComboBox
)
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from google.oauth2 import id_token
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
import pandas as pd
from utils.encrypt_utils import load_and_decrypt_token, encrypt_and_save_token
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request


class GoogleSheetViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.sheet_names = []  # 🔹 Lưu danh sách sheet để không phải gọi API lại

        # 🔹 Thiết lập giao diện
        self.setWindowTitle("Google Sheet Viewer")
        self.setGeometry(200, 200, 800, 500)

        # 🔹 Layout chính
        layout = QVBoxLayout()

        # 🔹 Label hướng dẫn
        self.label = QLabel("Nhập đường dẫn Google Sheet:")
        layout.addWidget(self.label)

        # 🔹 Ô nhập đường dẫn Sheet
        self.sheet_url_input = QLineEdit(self)
        self.sheet_url_input.setText(
            "https://docs.google.com/spreadsheets/d/1ExLQRdg1mKGPbfDD4Zpioz2eW4FW1LGWG-40dMrY2TM")
        layout.addWidget(self.sheet_url_input)

        self.label = QLabel("📜 Chọn Sheet:")
        layout.addWidget(self.label)

        # 🔹 Dropdown chọn sheet
        self.sheet_dropdown = QComboBox()
        layout.addWidget(self.sheet_dropdown)
        self.sheet_dropdown.currentIndexChanged.connect(lambda index: self.load_google_sheet(self.sheet_dropdown.currentText()))
        # self.sheet_dropdown.currentIndexChanged.connect(lambda index: QTimer.singleShot(0, lambda: self.load_google_sheet(self.sheet_dropdown.currentText())))
        # 🔹 Khu vực chứa 2 nút
        button_layout = QHBoxLayout()

        self.load_button = QPushButton("Load")
        self.load_button.clicked.connect(lambda: self.load_google_sheet(None))
        button_layout.addWidget(self.load_button)

        self.close_button = QPushButton("Đóng")
        self.close_button.clicked.connect(self.close)
        button_layout.addWidget(self.close_button)

        layout.addLayout(button_layout)

        # 🔹 Bảng hiển thị dữ liệu
        self.table_view = QTableView(self)
        layout.addWidget(self.table_view)

        self.setLayout(layout)

    def load_google_sheet(self, sheet_selected: str = None):
        """Tải dữ liệu từ Google Sheet và hiển thị vào bảng."""
        sheet_url = self.sheet_url_input.text().strip()

        if not sheet_url:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập đường dẫn Google Sheet!")
            return

        # 🛑 Nếu link Google Sheet thay đổi, reset danh sách sheet và load lại
        if not hasattr(self, "current_sheet_url") or self.current_sheet_url != sheet_url:
            self.current_sheet_url = sheet_url
            self.sheet_names = []  # Xoá danh sách sheets cũ

        try:
            # ✅ Nếu chưa có danh sách sheet, gọi API và cập nhật dropdown
            if not self.sheet_names:
                self.sheet_names = self.get_sheet_names(sheet_url)
                if not self.sheet_names:
                    QMessageBox.warning(self, "Lỗi", "Không thể lấy danh sách sheets!")
                    return

                # 🛑 Chặn tín hiệu khi cập nhật dropdown để tránh gọi lại load_google_sheet
                self.sheet_dropdown.blockSignals(True)
                self.sheet_dropdown.clear()
                self.sheet_dropdown.addItems(self.sheet_names)
                self.sheet_dropdown.blockSignals(False)

            # 📝 Nếu không chọn sheet, mặc định lấy sheet đầu tiên
            if not sheet_selected or sheet_selected not in self.sheet_names:
                sheet_selected = self.sheet_dropdown.currentText()

            # 🚀 Luôn gọi API để lấy dữ liệu mới
            df = self.get_google_sheet_data(sheet_url, sheet_selected)

            if df is not None:
                self.update_table(df)
            else:
                QMessageBox.warning(self, "Lỗi", "Không thể tải dữ liệu từ Google Sheet!")

        except Exception as e:
            print(e)
            QMessageBox.critical(self, "Lỗi", f"Lỗi tải dữ liệu: {str(e)}")

    def get_sheet_names(self, sheet_url):
        """🔹 Lấy danh sách các sheets từ Google Sheets API."""
        try:
            creds = get_google_credentials()
            if not creds:
                return []

            sheet_id = self.extract_sheet_id(sheet_url)
            service = build("sheets", "v4", credentials=creds)

            # 🟢 Chỉ lấy metadata, không tải dữ liệu
            sheet_metadata = service.spreadsheets().get(spreadsheetId=sheet_id).execute()
            sheets = sheet_metadata.get("sheets", [])
            sheet_names = [sheet["properties"]["title"] for sheet in sheets]

            return sheet_names

        except Exception as e:
            print("❌ Lỗi khi lấy danh sách sheets:", str(e))
            return []

    def get_google_sheet_data(self, sheet_url, sheet_selected):
        """🔹 Tải dữ liệu từ Google Sheets."""
        try:
            creds = get_google_credentials()
            if not creds:
                return None

            sheet_id = self.extract_sheet_id(sheet_url)
            service = build("sheets", "v4", credentials=creds)
            sheet = service.spreadsheets()

            # 📌 Chỉ đọc dữ liệu từ sheet đã chọn
            range_name = f"{sheet_selected}!A1:Z1000"
            result = sheet.values().get(spreadsheetId=sheet_id, range=range_name).execute()
            data = result.get("values", [])

            if not data:
                QMessageBox.warning(None, "Lỗi", "Không có dữ liệu trong Google Sheet!")
                return None

            print(f"✅ Đọc thành công {len(data)} dòng từ Google Sheet!")

            return self.convert_to_dataframe(data)

        except Exception as e:
            print("❌ Lỗi khi truy cập Google Sheet:", str(e))
            QMessageBox.critical(None, "Lỗi", f"Lỗi tải Google Sheet: {str(e)}")
            return None

    def convert_to_dataframe(self, data):
        """🔹 Chuyển dữ liệu Google Sheet thành Pandas DataFrame với tiêu đề A, B, C, ..."""
        if not data:
            return pd.DataFrame()

        max_columns = max(len(row) for row in data)

        def column_letters(n):
            """Chuyển số thứ tự thành A, B, C, ..., Z, AA, AB,... giống Google Sheets"""
            result = []
            while n > 0:
                n, remainder = divmod(n - 1, 26)
                result.append(string.ascii_uppercase[remainder])
            return ''.join(result[::-1])

        # 🚀 Tạo tiêu đề A, B, C, ..., Z, AA, AB,...
        header = [column_letters(i + 1) for i in range(max_columns)]

        # 🔹 Chuẩn hóa dữ liệu (đảm bảo đủ số cột)
        normalized_data = [row + [None] * (max_columns - len(row)) for row in data]

        # 🔹 Tạo DataFrame
        return pd.DataFrame(normalized_data, columns=header)

    def extract_sheet_id(self, sheet_url):
        """🔹 Trích xuất Google Sheet ID từ URL."""
        try:
            return sheet_url.split("/d/")[1].split("/")[0]
        except IndexError:
            raise ValueError("URL Google Sheet không hợp lệ! Hãy kiểm tra lại.")

    def update_table(self, df):
        """ Hàm cập nhật dữ liệu vào bảng """
        model = QStandardItemModel(df.shape[0], df.shape[1])

        # 🔹 Đặt tiêu đề cột
        model.setHorizontalHeaderLabels(df.columns)

        for row in range(df.shape[0]):
            for col in range(df.shape[1]):
                item = QStandardItem(str(df.iat[row, col]))
                model.setItem(row, col, item)

        self.table_view.setModel(model)


SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets.readonly"
]


def get_google_credentials():
    """🔹 Tải token, kiểm tra và làm mới nếu hết hạn"""
    try:
        token_data = load_and_decrypt_token()  # 🔹 Token đã được giải mã từ file

        if isinstance(token_data, str):
            token_data = json.loads(token_data)  # 🔹 Chuyển từ chuỗi JSON sang dictionary

        # 🔹 Kiểm tra xem token có đầy đủ thông tin không
        required_keys = {"token", "refresh_token", "token_uri", "client_id", "client_secret"}
        if not required_keys.issubset(token_data):
            raise ValueError("Token không hợp lệ hoặc thiếu thông tin!")

        # 🔹 Tạo credentials từ token
        creds = Credentials(
            token=token_data["token"],
            refresh_token=token_data["refresh_token"],
            token_uri=token_data["token_uri"],
            client_id=token_data["client_id"],
            client_secret=token_data["client_secret"],
            scopes=SCOPES
        )

        # 🔹 Kiểm tra token hết hạn chưa
        if creds.expired and creds.refresh_token:
            creds.refresh(Request())  # 🔹 Làm mới token
            encrypt_and_save_token(creds.to_json())  # 🔹 Lưu lại token mới

        return creds

    except Exception as e:
        print("Lỗi khi lấy token:", e)
        return None


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GoogleSheetViewer()
    window.show()
    sys.exit(app.exec())
