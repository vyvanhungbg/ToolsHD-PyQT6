


from PyQt6.QtWidgets import QWidget, QApplication
from PyQt6.QtGui import QScreen


def center_window(widget: QWidget):
    """Căn giữa màn hình cho bất kỳ QWidget."""
    screen = QApplication.primaryScreen()
    screen_geometry = screen.geometry()  # Lấy kích thước màn hình
    widget_geometry = widget.frameGeometry()  # Lấy kích thước widget

    # Tính toán vị trí giữa màn hình
    x = (screen_geometry.width() - widget_geometry.width()) // 2
    y = (screen_geometry.height() - widget_geometry.height()) // 2

    widget.move(x, y)  # Di chuyển widget đến vị trí đã tính
