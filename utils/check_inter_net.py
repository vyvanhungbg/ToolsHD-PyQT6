import requests


def is_internet_available():
    try:
        requests.get("https://www.google.com", timeout=10)
        return True  # ✅ Có mạng
    except requests.RequestException:
        return False  # ⛔ Không có mạng
