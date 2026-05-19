# config.py
# 將所有「變數」抽離，未來若網站換網域或目錄名稱，改這裡即可。

BASE_URL = "https://browndust2-db.souseha.com"
IMAGE_DOMAIN = "https://image-bd2db.souseha.com"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Referer": BASE_URL
}

# 圖片路徑配置
IMAGE_CONFIGS = [
    {"suffix": "_large", "path": "/characters-large/"},
    {"suffix": "",       "path": "/characters/"},
    {"suffix": "_idle",  "path": "/characters/"}
]

# 儲存路徑
SAVE_ROOT = "BD2角色素材"