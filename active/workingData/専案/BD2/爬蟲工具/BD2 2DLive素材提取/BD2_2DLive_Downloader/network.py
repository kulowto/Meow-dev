# network.py
# 封裝請求邏輯，並預留了處理 data: null 的空間。

import requests
import time
from config import HEADERS, API_DETAIL_URL

class NetworkManager:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(HEADERS)

    def get_content_detail(self, content_id):
        """獲取 API 詳細資料"""
        url = API_DETAIL_URL.format(content_id=content_id)
        try:
            response = self.session.get(url, timeout=10)
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"  [!] 網路請求失敗: {e}")
        return None

    def download_file(self, url, save_path):
        """通用下載函數"""
        if not url.startswith("http"):
            url = "https:" + url
        try:
            r = self.session.get(url, timeout=10)
            if r.status_code == 200:
                with open(save_path, "wb") as f:
                    f.write(r.content)
                return True
        except:
            pass
        return False