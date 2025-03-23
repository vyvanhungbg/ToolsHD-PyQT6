from base.base_navigation import BaseNavigation
from ui.home_screen import HomeScreen

# Tạo ứng dụng
if __name__ == "__main__":
    app = BaseNavigation(HomeScreen)
    app.run()
