import json

from PyQt6.QtGui import QFont, QStandardItemModel, QStandardItem
from PyQt6.QtWidgets import QVBoxLayout, QPushButton, QDialog, QLabel, QTextEdit, QFileDialog, QTreeView, QApplication, \
    QMessageBox, QPlainTextEdit

from base.base_widget import BaseWidget


class SecondWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cửa sổ thứ hai")
        self.setGeometry(150, 150, 400, 300)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Đây là cửa sổ thứ hai"))
        self.setLayout(layout)


def open_second_window():
    second_window = SecondWindow()
    second_window.exec()


class FeaturePreviewJsonExportScreen(BaseWidget):
    """Màn hình chung cho tính năng A, B, C có nút quay về Home."""

    def __init__(self, navigation, json_export):
        super().__init__(navigation)
        self.setWindowTitle("Export")
        self.resize(800, 700)
        self.center_windown()
        # Layout chính
        layout = QVBoxLayout()

        # EditText (QTextEdit) để hiển thị JSON
        # self.text_edit = QTextEdit(self)
        # self.text_edit.setFont(QFont("Courier", 12))  # Font kiểu code
        # self.text_edit.setPlaceholderText("Nhập hoặc dán JSON tại đây...")
        # self.text_edit.setText(json_export)
        # layout.addWidget(self.text_edit)

        # TreeView để hiển thị JSON
        self.json_view = QPlainTextEdit(self)
        self.json_view.setStyleSheet("font-size: 14px;")
        self.json_view.setPlaceholderText("Nhập hoặc dán JSON vào đây...")
        layout.addWidget(self.json_view)

        self.format_json(json_export)
        # Button Export
        self.export_button = QPushButton("Export JSON", self)
        self.export_button.clicked.connect(self.export_json)
        layout.addWidget(self.export_button)

        #button back
        back_button = QPushButton("Thoát")
        layout.addWidget(back_button)

        back_button.clicked.connect(lambda: self.navigation.pop_screen())

        self.setLayout(layout)

    def export_json(self):
        """Xuất JSON ra file"""
        file_path, _ = QFileDialog.getSaveFileName(self, "Lưu JSON", "AdmobV4.json", "JSON Files (*.json)")
        if file_path:
            try:
                json_data = json.loads(self.json_view.toPlainText())  # Kiểm tra JSON hợp lệ
                with open(file_path, "w", encoding="utf-8") as file:
                    json.dump(json_data, file, indent=4, ensure_ascii=False)
                QMessageBox.information(self, "Thành công", "JSON đã được lưu!")
            except json.JSONDecodeError:
                QMessageBox.critical(self, "Lỗi", "Không thể lưu JSON do lỗi định dạng!")

    def format_json(self, raw_text):
        """Format JSON đẹp (thụt lề)"""
        try:
            parsed_json = json.loads(raw_text)  # Kiểm tra JSON hợp lệ
            formatted_json = json.dumps(parsed_json, indent=4, ensure_ascii=False)
            self.json_view.setPlainText(formatted_json)  # Hiển thị JSON đẹp
        except json.JSONDecodeError:
            QMessageBox.critical(self, "Lỗi JSON", "Dữ liệu JSON không hợp lệ!")
