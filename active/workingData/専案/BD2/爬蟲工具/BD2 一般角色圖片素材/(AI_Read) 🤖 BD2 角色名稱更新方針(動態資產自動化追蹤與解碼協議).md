### 1. 現狀診斷 (Context Diagnosis)

- **資產雜湊化 (Content Hashing)**：目標數據檔案（如 `db-histories-*.js`）的檔名包含隨機雜湊值。這意味著一旦網站更新，硬編碼的 URL 將立即失效。
    
- **編碼衝突 (Encoding Mismatch)**：預設的爬蟲請求（如 `requests.get`）在處理包含中文的 JS 檔案時，常因伺服器未標註 UTF-8 而誤判編碼，導致資料呈現亂碼（例如：`æå¾·ç¾`）。
    

### 2. 核心解決方案：三階段自癒邏輯 (Three-Stage Self-Healing Logic)

#### **第一階段：入口點追蹤 (Entry-Point Tracking)**

- **邏輯**：不直接請求數據檔，而是先請求穩定路徑（例如 `/tw/characters`）。
    
- **執行**：在 HTML 源碼中利用正則表達式（Regex）掃描最新的資產路徑。
    
- **關鍵 Pattern**：`r'/assets/db-histories-[a-zA-Z0-9_-]+\.js'`。
    

#### **第二階段：強制解碼請求 (Explicit Decoding Request)**

- **邏輯**：避開自動編碼判定，強制指定解碼協議。
    
- **執行**：在獲取 Response 後，手動設定 `response.encoding = 'utf-8'`，隨後才讀取 `response.text`。
    

#### **第三階段：特徵錨點提取 (Feature-Anchor Extraction)**

- **邏輯**：利用數據結構中的「固定鍵值對（Key-Value Pairs）」進行掃描，而非解析整個 JSON。
    
- **雙語提取策略**：
    
    - **中文名稱**：尋找 `character:"([^"]+)"`。
        
    - **英文 ID**：從 `costumeId` 中提取，模式為 `costumeId:"([a-zA-Z0-9]+)_\d+"`。
        

---

### 3. 未來更新對策表 (Troubleshooting & Maintenance)

| **狀況 (Scenario)** | **解決方案 (Solution)**                                                             |
| ----------------- | ------------------------------------------------------------------------------- |
| **找不到檔案路徑**       | 檢查 HTML 中的 `<script>` 標籤載入邏輯，可能資產改由 `_buildManifest.js` 管理。                     |
| **提取到 0 個角色**     | 檢查 `characterId` 或 `character` 鍵值是否在 JS 中被混淆（例如不帶引號或改名）。                        |
| **中文名字依然亂碼**      | 檢查網頁 Response Headers 中的 `Content-Type`，或改用 `response.content.decode('utf-8')`。 |

---

### 4. 實作參考代碼 (Snippet for AI)

Python

```
import requests
import re

def scout_and_extract(base_url="https://browndust2-db.souseha.com"):
    # 1. 動態定位 (解決雜湊變動)
    home = requests.get(f"{base_url}/tw/characters").text
    asset_path = re.search(r'/assets/db-histories-[a-zA-Z0-9_-]+\.js', home).group(0)
    
    # 2. 強制 UTF-8 (解決中文亂碼)
    res = requests.get(base_url + asset_path)
    res.encoding = 'utf-8'
    
    # 3. 提取雙語對照 (建立數據基礎)
    # 提取格式: (英文ID, 中文名)
    data = re.findall(r'costumeId:"([a-zA-Z0-9]+)_\d+",character:"([^"]+)"', res.text)
    return {zh: en for en, zh in data}
```

---

### 5. 指導方針 (Guiding Principle)

**「不要尋找固定的檔名，要尋找檔案生成的規律。」** 只要掌握了 `Entry Point -> Discovery -> Explicit Decoding -> Feature Extraction` 這套流程，無論該網站的後端哈希如何變換，AI 都能在秒級內完成自癒並導出正確的數據資產。