from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtWidgets import QWidget, QApplication, QMessageBox


class BaseWidget(QWidget):
    """Base Widget có sẵn chức năng căn giữa."""

    def __init__(self, navigation):
        super().__init__()
        self.navigation = navigation  # Nhận tham chiếu đến bộ điều hướng
        self.center_windown()
    def show_message(self, message):
        """ Hiển thị thông báo khi nhấn nút """
        QMessageBox.information(self, "Thông báo", message)

    def set_dark_mode(self):
        """ Cài đặt giao diện tối cho toàn bộ ứng dụng """
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor("#121212"))  # Màu nền cửa sổ
        palette.setColor(QPalette.ColorRole.WindowText, QColor("#FFFFFF"))  # Màu chữ
        palette.setColor(QPalette.ColorRole.Button, QColor("#1e1e1e"))  # Màu nền nút
        palette.setColor(QPalette.ColorRole.ButtonText, QColor("#FFFFFF"))  # Màu chữ nút
        palette.setColor(QPalette.ColorRole.Base, QColor("#1e1e1e"))  # Màu nền input
        palette.setColor(QPalette.ColorRole.Text, QColor("#FFFFFF"))  # Màu chữ input
        palette.setColor(QPalette.ColorRole.Highlight, QColor("#BB86FC"))  # Màu khi chọn
        palette.setColor(QPalette.ColorRole.HighlightedText, QColor("#000000"))  # Chữ trên nền chọn
        QApplication.instance().setPalette(palette)  # Áp dụng cho toàn bộ app
    def center_windown(self):
        """Căn giữa màn hình."""
        screen = QApplication.primaryScreen()
        if not screen:
            return

        screen_geometry = screen.geometry()  # Kích thước màn hình
        widget_geometry = self.frameGeometry()  # Kích thước widget

        x = (screen_geometry.width() - widget_geometry.width()) // 2
        y = (screen_geometry.height() - widget_geometry.height()) // 2

        self.move(x, y)  # Di chuyển widget đến vị trí trung tâm