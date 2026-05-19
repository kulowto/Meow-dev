# file_io.py
# 負責相對路徑管理與 OpenCC 繁體化處理。

import os
from opencc import OpenCC

class FileHandler:
    def __init__(self):
        # 使用 s2twp 確保轉換為台灣慣用詞彙與繁體
        self.cc = OpenCC('s2twp')
        self.base_dir = os.path.join(os.getcwd(), "Downloads")

    def to_tchinese(self, text):
        """將任何傳入的文字（簡體或繁體）統一轉為繁體"""
        if not text:
            return ""
        return self.cc.convert(text)

    def get_safe_path(self, char_name, style_name):
        """
        處理角色與皮膚資料夾路徑。
        這裡會先將名稱轉繁體，並過濾掉 Windows 不允許的特殊符號。
        """
        # 統一轉繁體
        t_char = self.to_tchinese(char_name)
        t_style = self.to_tchinese(style_name)
        
        # 組合路徑：Downloads/角色名/皮膚名
        target_path = os.path.join(self.base_dir, t_char, t_style)
        
        if not os.path.exists(target_path):
            os.makedirs(target_path, exist_ok=True)
            
        return target_path

    def exists(self, folder, filename):
        """檢查檔案是否已存在，實現增量更新邏輯"""
        return os.path.exists(os.path.join(folder, filename))