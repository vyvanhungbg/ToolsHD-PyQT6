from PyQt6.QtWidgets import QVBoxLayout, QPushButton

from base.base_widget import BaseWidget
from login_google import LoginWindow
from ui.feature_convert_json_ad import FeatureConvertJsonAdScreen
from ui.feature_preview_json_export_screen import FeaturePreviewJsonExportScreen
from ui.feature_screen import FeatureScreen


class HomeScreen(BaseWidget):
    """Màn hình chính với các nút điều hướng."""

    def __init__(self, navigation):
        super().__init__(navigation)
        self.setWindowTitle("Home")
        self.resize(500, 300)
        layout = QVBoxLayout(self)
        btn_a = QPushButton("Tạo Json Ad Pro")
        btn_b = QPushButton("Tính năng B")
        btn_c = QPushButton("Tính năng C")

        layout.addWidget(btn_a)
        layout.addWidget(btn_b)
        layout.addWidget(btn_c)

        test_json = """
            {
    "name": "John Doe",
    "age": 30,
    "email": "johndoe@example.com",
    "address": {
        "street": "123 Main St",
        "city": "New York",
        "zip": "10001"
    },
    "phones": [
        "+1-202-555-0123",
        "+1-202-555-0456"
    ],
    "isActive": true,
    "preferences": {
        "notifications": true,
        "theme": "dark",
        "language": "en-US"
    }
}

        """
        btn_a.clicked.connect(lambda: self.navigation.push_screen(FeatureConvertJsonAdScreen))
        btn_b.clicked.connect(lambda: self.navigation.push_screen(LoginWindow, ))
        btn_c.clicked.connect(lambda: self.navigation.push_screen(FeaturePreviewJsonExportScreen, test_json))
