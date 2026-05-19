# main.py
# 串聯所有模塊的最高指揮部。

import json
import time
from config import CHARACTER_LIST
from network import NetworkManager
from file_io import FileHandler
from processor import AssetProcessor

def run_downloader():
    net = NetworkManager()
    io = FileHandler()
    proc = AssetProcessor(net, io)

    print("=== 棕色塵埃2 素材增量更新系統 V1.5 ===")
    
    for char in CHARACTER_LIST:
        print(f"\n>>> 檢查任務: {io.to_tchinese(char['name'])} (ID: {char['id']})")
        
        # 獲取 API 資料
        result = net.get_content_detail(char['id'])
        if not result or not result.get('data'):
            print(f"  [!] 無法獲取資料，跳過。")
            continue

        try:
            content_json = json.loads(result['data']['content_json'])
            
            for style in content_json.get('styleData', []):
                style_name = style.get('name', '預設')
                # 建立/取得資料夾路徑 (自動處理繁體化與相對路徑)
                target_dir = io.get_safe_path(char['name'], style_name)
                
                print(f"    -> 分類: {io.to_tchinese(style_name)}")
                
                for row in style.get('data', []):
                    for item in row:
                        if item.get('type') == 'live2d':
                            val = item['value']
                            # 執行 Spine 下載與掃描
                            proc.process_live2d(val, target_dir)
                            # 執行背景下載
                            proc.process_background(val.get('bg'), target_dir)

            time.sleep(0.2) # 友善爬取間隔
            
        except Exception as e:
            print(f"  [❌] 解析出錯: {e}")

    print("\n>>> 任務結束！素材儲存於 Downloads 資料夾。")

if __name__ == "__main__":
    run_downloader()