import requests
import os
import json
import time
from opencc import OpenCC

cc = OpenCC('s2twp')

# 角色清單維持不變...
character_list = [
    {"id": 689646, "name": "葛拉娜德"}, {"id": 646889, "name": "黎维塔"},
    {"id": 701014, "name": "斑鸠"}, {"id": 698749, "name": "马莫尼勒"},
    {"id": 697006, "name": "帕莱特"}, {"id": 678559, "name": "达丽安"},
    {"id": 678097, "name": "提尔"}, {"id": 676671, "name": "索妮亚"},
    {"id": 593588, "name": "席比雅"}, {"id": 670435, "name": "奥利维尔"},
    {"id": 603226, "name": "杰尼斯"}, {"id": 620949, "name": "芮彼泰雅"},
    {"id": 655252, "name": "威廉明娜"}, {"id": 593603, "name": "伊柯利普斯"},
    {"id": 593531, "name": "拉德尔"}, {"id": 593608, "name": "莉亚特里斯"},
    {"id": 593601, "name": "露比雅"}, {"id": 593614, "name": "艾瑞克"},
    {"id": 593623, "name": "安娜塔西亚"}, {"id": 593626, "name": "爱丽洁"},
    {"id": 621763, "name": "罗安"}, {"id": 624137, "name": "艾莉丝"},
    {"id": 629234, "name": "莱维亚"}, {"id": 660204, "name": "哥布林杀手"},
    {"id": 662553, "name": "剑之圣女"}, {"id": 660218, "name": "女神官"},
    {"id": 593571, "name": "悠丝缇亚"}, {"id": 593630, "name": "海伦娜"},
    {"id": 597740, "name": "安洁莉卡"}, {"id": 602076, "name": "班塔纳"},
    {"id": 606610, "name": "尤里"}, {"id": 611786, "name": "格兰希特"},
    {"id": 626508, "name": "神圣悠丝缇亚"}, {"id": 633685, "name": "米卡艾拉"},
    {"id": 632282, "name": "墨菲亚"}, {"id": 593577, "name": "莎赫拉查德"},
    {"id": 593606, "name": "泰瑞丝"}, {"id": 593625, "name": "拉菲娜"},
    {"id": 600786, "name": "克蕾西亚"}, {"id": 622875, "name": "洛琪希"},
    {"id": 638795, "name": "雪泉"}, {"id": 660211, "name": "妖精弓手"},
    {"id": 593587, "name": "奥尔施塔因"}, {"id": 593624, "name": "莱克莉丝"},
    {"id": 593582, "name": "格雷"}, {"id": 603227, "name": "黛安娜"},
    {"id": 607173, "name": "达菲"}, {"id": 625113, "name": "贝那卡"},
    {"id": 625800, "name": "内布利斯"}, {"id": 637920, "name": "日影"},
    {"id": 637919, "name": "咏"}, {"id": 637922, "name": "夜樱"},
    {"id": 593586, "name": "鲁"}, {"id": 593621, "name": "赛尔"},
    {"id": 593569, "name": "西利亚"}, {"id": 593632, "name": "艾尼爾"},
    {"id": 607899, "name": "纳罗达斯"}, {"id": 640139, "name": "卢班希亚"},
    {"id": 648133, "name": "布莱德"}
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Referer": "https://www.gamekee.com/",
    "Game-Id": "50118"
}

def smart_download(base_url, folder):
    """ 智慧掃描：加入檔案存在判斷，跳過已下載檔案 """
    if not base_url: return
    
    base_no_ext = base_url.split('.json')[0].split('.atlas')[0].split('.png')[0]
    if not base_no_ext.startswith("http"): base_no_ext = "https:" + base_no_ext
    
    file_base_name = os.path.basename(base_no_ext)
    
    # 1. 下載核心數據檔 (.json, .atlas)
    for ext in [".json", ".atlas"]:
        save_path = os.path.join(folder, file_base_name + ext)
        
        # --- 新增判斷：若檔案已存在則跳過 ---
        if os.path.exists(save_path):
            # print(f"      [跳過] {file_base_name}{ext} 已存在") # 若想畫面乾淨點可註解這行
            continue
            
        target_url = base_no_ext + ext
        try:
            r = requests.get(target_url, headers=HEADERS, timeout=10)
            if r.status_code == 200:
                with open(save_path, "wb") as f: f.write(r.content)
                print(f"      [成功] 數據: {file_base_name}{ext}")
        except: pass

    # 2. 掃描貼圖 (_2, _3 等)
    potential_imgs = [f"{file_base_name}.png"] + [f"{file_base_name}_{i}.png" for i in range(2, 6)]
    
    for img_name in potential_imgs:
        save_path = os.path.join(folder, img_name)
        
        # --- 新增判斷：若貼圖已存在則跳過 ---
        if os.path.exists(save_path):
            continue
            
        img_url = os.path.dirname(base_no_ext) + "/" + img_name
        try:
            r = requests.get(img_url, headers=HEADERS, timeout=5)
            if r.status_code == 200:
                with open(save_path, "wb") as f: f.write(r.content)
                print(f"      [成功] 貼圖: {img_name}")
        except: pass

def main():
    for char in character_list:
        char_name = cc.convert(char['name'])
        print(f"\n>>> 檢查任務: {char_name} (ID: {char['id']})")
        
        if not os.path.exists(char_name): os.makedirs(char_name)
        
        try:
            api_url = f"https://www.gamekee.com/v1/content/detail/{char['id']}"
            resp = requests.get(api_url, headers=HEADERS, timeout=10)
            data = resp.json()
            
            if not data.get('data'):
                print(f"  [!] 無法從 API 獲取 {char_name} 資料，跳過。")
                continue
                
            content_json = json.loads(data['data']['content_json'])
            
            for style in content_json.get('styleData', []):
                style_name = cc.convert(style.get('name', '預設'))
                target_dir = os.path.join(char_name, style_name)
                if not os.path.exists(target_dir): os.makedirs(target_dir)
                
                print(f"    -> 分類: {style_name}")
                
                for row in style.get('data', []):
                    for item in row:
                        if item.get('type') == 'live2d':
                            val = item['value']
                            smart_download(val.get('json'), target_dir)
                            
                            # 背景圖下載判斷
                            if val.get('bg'):
                                bg_url = val['bg'] if val['bg'].startswith("http") else "https:" + val['bg']
                                bg_name = "背景_" + os.path.basename(bg_url.split('?')[0])
                                bg_save_path = os.path.join(target_dir, bg_name)
                                
                                # --- 新增判斷：若背景已存在則跳過 ---
                                if not os.path.exists(bg_save_path):
                                    r_bg = requests.get(bg_url, headers=HEADERS)
                                    if r_bg.status_code == 200:
                                        with open(bg_save_path, "wb") as f: f.write(r_bg.content)
                                        print(f"      [成功] {bg_name}")
                                # else:
                                #     print(f"      [跳過] {bg_name} 已存在")

            # 每個角色處理完稍微喘氣，如果是全跳過的話速度會非常快
            time.sleep(0.1) 
            
        except Exception as e:
            print(f"  [❌] 出錯: {e}")

if __name__ == "__main__":
    main()
    print("\n>>> 所有角色更新/檢查完成！")