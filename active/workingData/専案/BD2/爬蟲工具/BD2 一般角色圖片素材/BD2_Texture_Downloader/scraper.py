# scraper.py
# 負責處理「雜湊值更新」與「雙語對應」的邏輯。

import requests
import re
from config import BASE_URL, HEADERS

def get_latest_js_url():
    """動態從首頁獲取最新的 db-histories 網址"""
    try:
        res = requests.get(f"{BASE_URL}/tw/characters", headers=HEADERS, timeout=10)
        match = re.search(r'/assets/db-histories-[a-zA-Z0-9_-]+\.js', res.text)
        if match:
            return BASE_URL + match.group(0)
    except Exception as e:
        print(f"定位資產失敗: {e}")
    return "https://browndust2-db.souseha.com/assets/db-histories-Bf9IE8eb.js"

def fetch_mapping():
    """抓取並解析雙語對照表"""
    js_url = get_latest_js_url()
    print(f"📡 正在從數據源抓取: {js_url}")
    
    try:
        res = requests.get(js_url, headers=HEADERS)
        res.encoding = 'utf-8' # 強制 UTF-8 解決亂碼
        
        # 提取英文 ID 與 中文名稱
        pattern = r'costumeId:"([a-zA-Z0-9]+)_\d+",character:"([^"]+)"'
        matches = re.findall(pattern, res.text)
        
        mapping = {}
        for en_id, zh_name in matches:
            if zh_name not in mapping:
                mapping[zh_name] = en_id
        return mapping
    except Exception as e:
        print(f"解析對照表失敗: {e}")
        return {}