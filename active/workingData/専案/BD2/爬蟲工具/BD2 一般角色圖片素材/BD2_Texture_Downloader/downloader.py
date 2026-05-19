# downloader.py
# 這是主程式，調用前兩個模組來完成作業。

import os
import requests
import time
from config import IMAGE_DOMAIN, HEADERS, IMAGE_CONFIGS, SAVE_ROOT
from scraper import fetch_mapping

def download_file(url, dest_path):
    """通用的文件下載邏輯"""
    try:
        response = requests.get(url, headers=HEADERS, stream=True, timeout=5)
        if response.status_code == 200:
            with open(dest_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            return True
    except:
        pass
    return False

def start_process():
    # 1. 獲取數據
    mapping = fetch_mapping()
    if not mapping:
        print("無法取得角色清單，任務終止。")
        return

    print(f"🚀 開始下載流程，預計處理 {len(mapping)} 位角色...")

    # 2. 遍歷角色
    for zh_name, en_id in mapping.items():
        save_dir = os.path.join(SAVE_ROOT, zh_name)
        os.makedirs(save_dir, exist_ok=True)
        
        print(f"\n[處理中] {zh_name}...")
        
        for i in range(1, 10):
            found_at_this_index = False
            for cfg in IMAGE_CONFIGS:
                file_name = f"{en_id}_{i}{cfg['suffix']}.webp"
                target_url = f"{IMAGE_DOMAIN}{cfg['path']}{file_name}"
                dest_path = os.path.join(save_dir, file_name)
                
                if download_file(target_url, dest_path):
                    print(f"  └─ 下載成功: {file_name}")
                    found_at_this_index = True
            
            # 智慧跳過：如果該編號完全沒圖，且已經嘗試過基礎服裝，則跳過後續編號
            if not found_at_this_index and i > 3:
                break
        
        time.sleep(0.3) # 禮貌性延遲

if __name__ == "__main__":
    start_process()