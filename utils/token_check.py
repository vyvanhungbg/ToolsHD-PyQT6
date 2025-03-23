import base64
import json
import os

import requests
from google_auth_oauthlib.flow import InstalledAppFlow

from utils.encrypt_utils import encrypt_and_save_token, load_and_decrypt_token
from utils.path_utils import CONFIG_FILE, TOKEN_URL, TOKEN_FILE


def get_user_info(access_token):
    """🔎 Lấy thông tin user từ Google bằng access_token."""
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get("https://www.googleapis.com/oauth2/v2/userinfo", headers=headers)

    if response.status_code == 200:
        print(response.json())
        return response.json()  # ✅ Trả về thông tin user (email, name, picture)
    else:
        print(f"⚠ Lỗi lấy thông tin user: {response.status_code} - {response.text}")
        return None


def load_client_config():
    """📂 Đọc client_id và client_secret từ file JSON."""
    try:
        with open(CONFIG_FILE, "r") as file:
            config = json.load(file)
            client_id = config["installed"]["client_id"]
            client_secret = config["installed"]["client_secret"]
            return client_id, client_secret
    except (FileNotFoundError, KeyError, json.JSONDecodeError) as e:
        print(f"⚠ Lỗi đọc client config: {e}")
        return None, None


def is_token_valid(access_token):
    url = "https://www.googleapis.com/oauth2/v3/tokeninfo"
    params = {"access_token": access_token}

    try:
        response = requests.get(url, params=params, timeout=5)
        return response.status_code == 200  # ✅ Token live nếu HTTP 200
    except requests.RequestException:
        return False  # ⛔ Nếu lỗi mạng, coi như token hết hạn


def refresh_access_token(refresh_token):
    """🔄 Dùng refresh token để lấy access token mới từ Google."""
    client_id, client_secret = load_client_config()
    if not client_id or not client_secret:
        print("❌ Không thể làm mới token do thiếu client_id hoặc client_secret.")
        return None, None

    try:
        response = requests.post(
            TOKEN_URL,
            data={
                "client_id": client_id,
                "client_secret": client_secret,
                "refresh_token": refresh_token,
                "grant_type": "refresh_token"
            }
        )
        if response.status_code == 200:
            new_tokens = response.json()
            return new_tokens.get("access_token"), new_tokens.get("expires_in")
        else:
            print("❌ Lỗi làm mới token:", response.json())
            return None, None
    except requests.RequestException as e:
        print("⚠ Lỗi mạng khi làm mới token:", str(e))
        return None, None




def google_login():
    """🔑 Đăng nhập Google hoặc làm mới token nếu có."""
    token_data = load_and_decrypt_token()
    creds = None  # Mặc định chưa có token hợp lệ

    if token_data:
        try:
            creds = json.loads(token_data)
            access_token = creds.get("access_token")
            refresh_token = creds.get("refresh_token")

            # ✅ Nếu access token hết hạn, thử làm mới bằng refresh token
            if not is_token_valid(access_token) and refresh_token:
                print("🔄 Token hết hạn, thử làm mới bằng refresh token...")
                new_access_token, expires_in = refresh_access_token(refresh_token)
                if new_access_token:
                    creds["access_token"] = new_access_token
                    creds["expires_in"] = expires_in
                    encrypt_and_save_token(json.dumps(creds))  # 🔒 Lưu lại token

                    # 🔹 Khi làm mới token, KHÔNG có `id_token`, cần yêu cầu đăng nhập mới
                    user_info = get_user_info(creds["access_token"])
                    if user_info:
                        print(f"📧 Email: {user_info['email']}")
                        return user_info
                    else:
                        print("⚠ Không lấy được thông tin user từ Google API!")
                        return None

                else:
                    creds = None  # Không làm mới được, yêu cầu đăng nhập lại

        except json.JSONDecodeError:
            print("❌ Token lỗi, yêu cầu đăng nhập lại.")
            creds = None

    if not creds:
        # 🔹 Yêu cầu đăng nhập mới
        flow = InstalledAppFlow.from_client_secrets_file(
            CONFIG_FILE,
            scopes=[
                "https://www.googleapis.com/auth/spreadsheets.readonly",
                "https://www.googleapis.com/auth/userinfo.email",
                "openid"  # 🔥 Đảm bảo yêu cầu OpenID để nhận `id_token`
            ]
        )
        creds_obj = flow.run_local_server(port=0)

        if creds_obj and creds_obj.token:
            token_data = creds_obj.to_json()
            encrypt_and_save_token(token_data)  # 🔒 Lưu token mã hóa
            print("✅ Đăng nhập thành công!")

            # 🏆 Giải mã ID token lấy thông tin user
            user_info = get_user_info(creds_obj.token)
            if user_info:
                print(f"📧 Email: {user_info['email']}")
                return user_info  # ✅ Trả về thông tin user

            else:
                print("⚠ Không lấy được thông tin user từ ID token!")
                return None

        else:
            print("❌ Đăng nhập thất bại!")
            return None

    else:
        # 🔹 Nếu token còn hợp lệ, giải mã ID token lấy thông tin user
        user_info = get_user_info(creds["access_token"])
        if user_info:
            print(f"📧 Email: {user_info['email']}")
            return user_info
        else:
            print("⚠ Không lấy được thông tin user từ Google API!")
            return None


def google_logout():
    """🚪 Đăng xuất Google: Xóa token và thu hồi quyền truy cập."""
    token_data = load_and_decrypt_token()
    if not token_data:
        print("⚠ Không có token để đăng xuất!")
        return False

    try:
        creds = json.loads(token_data)
        access_token = creds.get("access_token")

        # 🔹 Gọi API thu hồi token nếu có
        if access_token:
            revoke_url = f"https://accounts.google.com/o/oauth2/revoke?token={access_token}"
            response = requests.post(revoke_url)

            if response.status_code == 200:
                print("✅ Token đã bị thu hồi thành công.")
            else:
                print(f"⚠ Lỗi khi thu hồi token: {response.status_code} - {response.text}")

        # 🔥 Xóa file/token lưu trữ để đăng xuất hoàn toàn
        if os.path.exists(TOKEN_FILE):
            os.remove(TOKEN_FILE)  # Xóa token khi đăng xuất
        print("✅ Đã đăng xuất khỏi Google.")
        return True

    except Exception as e:
        print("❌ Lỗi khi đọc token.")
        return False