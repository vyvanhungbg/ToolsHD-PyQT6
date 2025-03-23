from PyQt6.QtWidgets import QApplication, QStackedWidget, QWidget, QVBoxLayout, QPushButton


class BaseNavigation:
    """Bộ điều hướng quản lý các màn hình."""

    def __init__(self, initial_screen):
        self.app = QApplication([])
        self.window = QWidget()
        self.window.setWindowTitle("Menu Tools HD")

        self.stack = QStackedWidget()
        self.screen_stack = []  # Danh sách màn hình theo thứ tự

        # 🏠 Thêm màn Home vào stack
        self.push_screen(initial_screen)

        layout = QVBoxLayout(self.window)
        layout.addWidget(self.stack)
        self.window.setLayout(layout)

        screen = QApplication.primaryScreen().geometry()
        width = screen.width() // 2
        height = screen.height() // 2
        self.window.resize(width, height)
        self.window.show()

    def push_screen(self, screen_class, *args):
        """Thêm màn hình mới vào stack bằng class."""
        for widget in self.screen_stack:
            if isinstance(widget, screen_class):
                self.stack.setCurrentWidget(widget)
                return  # Nếu đã có màn này, chỉ cần chuyển sang

        # Nếu chưa có, tạo mới
        widget = screen_class(self, *args)
        self.stack.addWidget(widget)
        self.stack.setCurrentWidget(widget)
        self.screen_stack.append(widget)  # Đẩy vào stack
        self.update_window_title()
        print(f"Stack = {self.get_current_stack()}")

    def pop_screen(self):
        """Quay về màn trước đó và loại bỏ màn hiện tại."""
        if len(self.screen_stack) > 1:
            widget_to_remove = self.screen_stack.pop()
            self.stack.removeWidget(widget_to_remove)
            widget_to_remove.deleteLater()
            self.stack.setCurrentWidget(self.screen_stack[-1])  # Chuyển về màn trước
        self.update_window_title()
        print(f"Stack = {self.get_current_stack()}")

    def pop_to_screen(self, target_class):
        """Quay về màn hình chỉ định, xoá tất cả màn hình trung gian."""
        target_index = -1
        for i, widget in enumerate(self.screen_stack):
            if isinstance(widget, target_class):
                target_index = i
                break

        if target_index == -1:
            print("❌ Màn hình không tồn tại trong stack!")
            return

        # Xóa tất cả màn hình sau target_index
        while len(self.screen_stack) > target_index + 1:
            widget_to_remove = self.screen_stack.pop()
            self.stack.removeWidget(widget_to_remove)
            widget_to_remove.deleteLater()

        # Chuyển về màn hình chỉ định
        self.stack.setCurrentWidget(self.screen_stack[-1])
        self.update_window_title()
        print(f"Stack = {self.get_current_stack()}")

    def get_current_stack(self):
        """Lấy danh sách màn hình trong stack."""
        return [widget.windowTitle() for widget in self.screen_stack]

    def update_window_title(self):
        """Cập nhật tiêu đề cửa sổ theo màn hình hiện tại."""
        current_widget = self.stack.currentWidget()
        if current_widget:
            self.window.setWindowTitle(current_widget.windowTitle())

    def run(self):
        """Chạy ứng dụng."""
        self.app.exec()
