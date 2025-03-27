from PyQt6.QtWidgets import QVBoxLayout, QPushButton, QDialog, QLabel

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
