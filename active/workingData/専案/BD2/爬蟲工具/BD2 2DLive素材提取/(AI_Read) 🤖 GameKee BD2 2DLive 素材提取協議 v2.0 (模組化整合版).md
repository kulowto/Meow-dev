---
reviewed: false
version: v2.1
updated: 2026-05-07
---

# 🤖 GameKee BD2 2DLive 素材提取協議 v2.1（模組化整合版）

> 本文件供 AI 閱讀與協作使用，同時作為開發規格書與封裝指引。
> `reviewed: false`，為 AI 輔助整理版本，作為執行依據前請確認。

---

## 文件用途

記錄《棕色塵埃 2》2DLive（Spine）素材自動提取工具的完整設計協議，涵蓋：

1. AI 執行指令（Prompt 範本）
2. 模組化架構與各模組職責
3. 完整執行流程與核心邏輯
4. 命名與儲存規範
5. 封裝與客戶端發布規劃（含非 Python 使用者方案）

---

## AI 執行指令（Prompt 範本）

> 「請根據下列協議，分析角色 ID [填入ID]，使用**智慧掃描**與**增量更新**邏輯（檔案已存在則跳過）編寫完整可執行的 Python 腳本，並確保正確處理多貼圖命名與分類。模組化版本請依 config / network / processor / file_io / main 五模組拆分。」

---

## 專案架構

```
BD2_2DLive_Downloader/         ← 模組化版本（現行 V1.5）
├── config.py                  # 核心配置、Header、角色清單（60 個）
├── network.py                 # 網路請求與 Session 管理
├── processor.py               # 素材分析與智慧掃描邏輯
├── file_io.py                 # 檔案系統操作與 OpenCC 繁體化
└── main.py                    # 任務調度主程式（唯一進入點）

Downloads/                     ← 執行後自動生成（相對路徑）
└── [繁體角色名]/
    └── [繁體皮膚名]/
        ├── [spine_name].json
        ├── [spine_name].atlas
        ├── [spine_name].png
        ├── [spine_name]_2.png   ← 智慧掃描產出（_2 至 _5，視存在與否）
        └── 背景_[filename].jpg
```

> 另有 `(Code) GameKee BD2 2DLive素材提取 (Python代碼).md`：單檔版本（V1.0 原型），邏輯相同但未解耦，供對照與 AI 快速理解用。

---

## 1. 專案背景

| 項目 | 說明 |
|------|------|
| 目標 | 自動化提取 GameKee Wiki 上《棕色塵埃 2》的 Spine 2DLive 素材 |
| 資料來源 | `https://www.gamekee.com/v1/content/detail/{id}` |
| 核心挑戰一 | API 需攜帶 `Game-Id: 50118` Header 才能通過校驗 |
| 核心挑戰二 | API 不回傳完整貼圖路徑，需靠「試探掃描」補齊 `_2`～`_5` 後綴貼圖 |
| 預期行為 | 「智慧掃描」確保貼圖完整；「增量更新」避免重複下載 |
| 角色數量 | 60 個（含跨界合作角色：哥布林殺手、劍之聖女、女神官） |

---

## 2. 核心哲學

- **自動化優先**：程式自行完成從 API 請求到本地儲存的全自動閉環，無需人工干預。
- **增量思維**：所有下載動作前以 `os.path.exists()` 判斷，已存在則跳過，支援中斷續傳。
- **解耦合架構**：網路層、處理層、儲存層、配置層完全分離，任一模組失效不影響整體穩定性。

---

## 3. 技術棧

| 層級 | 工具 / 做法 |
|------|------------|
| 語言 | Python 3.x |
| 網路 | `requests.Session()`，timeout 10s |
| Header 偽裝 | `User-Agent` + `Referer` + `Game-Id: 50118`（必備，否則 API 拒絕） |
| 語系轉換 | `opencc`（s2twp 模式），簡→繁（台灣慣用詞彙） |
| 路徑策略 | 相對路徑 `./Downloads/`，以執行目錄為基準 |
| 必裝依賴 | `requests`、`opencc-python-reimplemented` |

---

## 4. 模組化架構說明（解耦合設計）

### config.py — 核心配置

統一管理所有可調整參數，API 或 Header 若有變動只需修改此處，其他模組無感：

```python
HEADERS = { "User-Agent": "...", "Referer": "https://www.gamekee.com/", "Game-Id": "50118" }
API_DETAIL_URL = "https://www.gamekee.com/v1/content/detail/{content_id}"
TEXTURE_EXTENSIONS = ["", "_2", "_3", "_4", "_5"]  # 智慧掃描後綴規則
CHARACTER_LIST = [{"id": 689646, "name": "葛拉娜德"}, ...]  # 60 個角色，允許混簡繁
```

---

### network.py — 網路請求層

封裝 `requests.Session`，所有 HTTP 操作集中於此，與業務邏輯完全隔離：

```python
class NetworkManager:
    def get_content_detail(self, content_id) → dict | None  # 呼叫 API，失敗回傳 None
    def download_file(self, url, save_path) → bool           # 通用下載，自動補 https: 前綴
```

- Session 複用：同一 Session 維護 Cookie 與 Header，提升請求效率
- 協議修正：`url` 若以 `//` 開頭，自動補全為 `https://`

---

### processor.py — 素材處理層

解析 API 資料，執行 Spine 下載的核心邏輯，依賴 `NetworkManager` 和 `FileHandler` 注入：

```python
class AssetProcessor:
    def process_live2d(self, val, target_dir)        # 下載 .json/.atlas + 智慧掃描貼圖
    def process_background(self, bg_url, target_dir) # 下載背景圖，加 背景_ 前綴
```

**智慧掃描流程（process_live2d）**：
1. 從 `val['json']` 提取基底路徑（去掉 `.json` / `.atlas` / `.png` 副檔名）
2. 下載 `base.json`、`base.atlas`（各自檢查是否已存在）
3. 依序嘗試 `base.png`、`base_2.png` … `base_5.png`，HTTP 200 才寫入磁碟

---

### file_io.py — 檔案系統層

負責路徑管理與語系轉換，與網路和業務邏輯完全解耦：

```python
class FileHandler:
    def to_tchinese(self, text) → str                        # OpenCC s2twp 轉繁體
    def get_safe_path(self, char_name, style_name) → str     # 繁體化 + 建立目錄 + 回傳路徑
    def exists(self, folder, filename) → bool                # 增量更新判斷
```

**相對路徑存取策略**：
- `base_dir = os.path.join(os.getcwd(), "Downloads")`
- `Downloads/` 永遠建立在「執行 main.py 時的工作目錄」下，而非腳本所在路徑
- 封裝成 `.exe` 後此行為不變，客戶在哪個資料夾執行，素材就存在哪裡

---

### main.py — 任務調度（進入點）

串接所有模組，職責只有「遍歷 → 委派 → 等待」：

```python
def run_downloader():
    net  = NetworkManager()
    io   = FileHandler()
    proc = AssetProcessor(net, io)

    for char in CHARACTER_LIST:
        result = net.get_content_detail(char['id'])
        content_json → styleData → for 每個皮膚:
            target_dir = io.get_safe_path(char['name'], style['name'])
            for 每個 live2d item:
                proc.process_live2d(item['value'], target_dir)
                proc.process_background(item['value']['bg'], target_dir)
        time.sleep(0.2)  # 友善爬取間隔，避免被封鎖
```

---

## 5. 執行流程

```
啟動 python main.py
        │
        ▼
for 每個角色 in CHARACTER_LIST（60 個，依序處理）
        │
        ├─ GET https://www.gamekee.com/v1/content/detail/{id}
        │       ├─ 失敗（網路錯誤 / data: null）→ 印出警告，跳過此角色
        │       └─ 成功 → JSON.parse(data['content_json'])
        │
        └─ for 每個 styleData（皮膚分類，如「預設」「聖誕節」）
                │
                ├─ get_safe_path() → 建立 ./Downloads/角色名/皮膚名/
                │
                └─ for 每個 live2d 類型的 item
                        │
                        ├─ process_live2d(val, target_dir)
                        │       ├─ 下載 base.json     （已存在 → 跳過）
                        │       ├─ 下載 base.atlas    （已存在 → 跳過）
                        │       └─ 試探 base.png ... base_5.png（HTTP 200 → 存，否則跳過）
                        │
                        └─ process_background(bg_url, target_dir)
                                └─ 下載 背景_xxx.jpg  （已存在 → 跳過）

        sleep(0.2) ← 每個角色結束後暫停

任務結束 → 印出完成訊息
```

---

## 6. 命名與儲存規範

| 類型 | 規則 | 範例 |
|------|------|------|
| 輸出根目錄 | 執行目錄下的 `./Downloads/` | `./Downloads/` |
| 角色目錄 | 繁體中文（s2twp 轉換） | `葛拉娜德/` |
| 皮膚目錄 | 繁體中文（s2twp 轉換） | `預設/`、`聖誕節/` |
| Spine 核心檔 | 保留 API 原始檔名 | `ela.json`、`ela.atlas` |
| 貼圖檔 | 保留原始檔名，含試探後綴 | `ela.png`、`ela_2.png`、`ela_3.png` |
| 背景圖 | 原始檔名前加 `背景_` | `背景_bg_christmas.jpg` |

> 角色清單不論輸入簡繁體，`to_tchinese()` 保證輸出統一繁體；URL 參數（`?xxx`）會在下載前自動剝除。

---

## 7. 封裝與客戶端發布規劃

### 情境說明

客戶不一定具備 Python 環境，需提供「下載即用」方案。

### 方案 A：PyInstaller 打包 .exe（Windows 優先）

```bash
pip install pyinstaller requests opencc-python-reimplemented
pyinstaller --onefile --name BD2Downloader main.py
```

**重點注意事項**：
- `opencc` 需要附帶語言字典資料，打包時須用 `--add-data` 一併打入：
  ```bash
  # 先確認 opencc 資料目錄位置
  python -c "import opencc; print(opencc.__file__)"
  # 再指定加入
  pyinstaller --onefile --add-data "opencc資料路徑;opencc" main.py
  ```
- 打包後 `os.getcwd()` 依然指向「使用者執行 .exe 的目錄」，`Downloads/` 建立位置正確，不需額外處理 `sys._MEIPASS`
- 建議保存 `.spec` 設定檔，方便後續重新打包

**客戶使用流程**：
```
1. 下載 BD2Downloader.exe
2. 放到任意資料夾
3. 雙擊執行
4. 同目錄下會自動生成 Downloads/角色名/皮膚名/
```

---

### 方案 B：Nuitka（效能更好、產出更難被反編譯）

```bash
pip install nuitka
nuitka --onefile --include-data-dir=opencc資料目錄=opencc main.py
```

適合需要保護原始碼或追求執行效能的場景。

---

### 方案 C：Docker 容器（跨平台，適合有技術底的客戶）

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install requests opencc-python-reimplemented
VOLUME ["/app/Downloads"]
CMD ["python", "main.py"]
```

客戶端執行：
```bash
docker run -v $(pwd)/Downloads:/app/Downloads bd2-downloader
```

---

### 方案比較

| 方案 | 難度 | 適用平台 | 適合對象 |
|------|------|---------|---------|
| PyInstaller .exe | 低 | Windows | 一般使用者（優先推薦） |
| Nuitka | 中 | Windows / Linux | 需保護原始碼 |
| Docker | 中 | 跨平台 | 有技術背景的開發者 |

---

## 8. 未來擴充考量

| 功能 | 說明 |
|------|------|
| 多執行緒下載 | `concurrent.futures.ThreadPoolExecutor` 包 `process_live2d`，大幅提速；需注意 API 速率限制 |
| GUI 介面 | 以 `tkinter` 或 `PySimpleGUI` 包裝 `run_downloader()`，讓不懂命令列的使用者可直接操作 |
| 自動壓縮 | 下載完成後對每個角色目錄打 `.zip`，方便整包傳送 |
| data: null 處理 | API 若回傳空資料，提示使用者手動貼入 `content_json`（手動注入模式） |
| 角色清單維護 | 新角色只需在 `config.py` 的 `CHARACTER_LIST` 新增 `{"id": ..., "name": "..."}` |
