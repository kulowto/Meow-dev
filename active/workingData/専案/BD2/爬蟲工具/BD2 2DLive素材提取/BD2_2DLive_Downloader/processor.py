# processor.py
# 專門處理 Spine 的智慧掃描與背景命名規則。

import os
from config import TEXTURE_EXTENSIONS

class AssetProcessor:
    def __init__(self, network_mgr, file_handler):
        self.net = network_mgr
        self.io = file_handler

    def process_live2d(self, val, target_dir):
        """處理 Live2D 資源下載 (json, atlas, pngs)"""
        json_url = val.get('json')
        if not json_url: return

        # 取得不含副檔名的路徑基底
        base_no_ext = json_url.split('.json')[0].split('.atlas')[0].split('.png')[0]
        file_base_name = os.path.basename(base_no_ext)
        dir_url = os.path.dirname(base_no_ext)

        # 1. 核心數據檔 (.json, .atlas)
        for ext in [".json", ".atlas"]:
            fname = file_base_name + ext
            if not self.io.exists(target_dir, fname):
                if self.net.download_file(base_no_ext + ext, os.path.join(target_dir, fname)):
                    print(f"      [成功] 數據: {fname}")

        # 2. 智慧掃描貼圖 (含 _2, _3 等)
        for suffix in TEXTURE_EXTENSIONS:
            img_name = f"{file_base_name}{suffix}.png"
            if not self.io.exists(target_dir, img_name):
                img_url = f"{dir_url}/{img_name}"
                if self.net.download_file(img_url, os.path.join(target_dir, img_name)):
                    print(f"      [成功] 貼圖: {img_name}")

    def process_background(self, bg_url, target_dir):
        """處理背景圖下載"""
        if not bg_url: return
        
        # 移除 URL 參數並加上「背景_」前綴
        pure_url = bg_url.split('?')[0]
        bg_name = "背景_" + os.path.basename(pure_url)
        
        if not self.io.exists(target_dir, bg_name):
            if self.net.download_file(bg_url, os.path.join(target_dir, bg_name)):
                print(f"      [成功] {bg_name}")