from PyQt6.QtWidgets import QVBoxLayout, QPushButton

from base.base_widget import BaseWidget


class FeatureScreen(BaseWidget):
    """Màn hình chung cho tính năng A, B, C có nút quay về Home."""

    def __init__(self, navigation, feature_name):
        super().__init__(navigation)
        self.setWindowTitle(feature_name)

        layout = QVBoxLayout()

        label = QPushButton(f"Đây là màn {feature_name}")
        back_button = QPushButton("Quay về Home")

        layout.addWidget(label)
        layout.addWidget(back_button)

        back_button.clicked.connect(lambda: self.navigation.pop_screen())

        self.setLayout(layout)