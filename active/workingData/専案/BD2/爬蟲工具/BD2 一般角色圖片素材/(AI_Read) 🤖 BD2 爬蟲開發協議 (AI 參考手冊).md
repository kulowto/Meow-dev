1. 背景與目標
   目標是實現自動化、具備自癒能力的素材抓取流程。開發重點已從「硬編碼網址」進化為「入口點掃描」，以應對現代 Web 框架（如 Vite/Webpack）中頻繁變動的資產雜湊值 (Hash)。

2. 網域與 URL 規則
   網頁網域： [https://browndust2-db.souseha.com/](https://browndust2-db.souseha.com/)

素材網域： [https://image-bd2db.souseha.com](https://image-bd2db.souseha.com)

檔案命名： {英文 ID}\_{編號}{後綴}.webp

編號：1 至 9（考量人氣角色服裝擴充）。

後綴：\_large (大型立繪), \_idle (待機圖), "" (標準圖)。

3. 動態資產定位 (核心自癒邏輯)
   由於數據檔案（如 db-histories-Bf9IE8eb.js）的檔名包含隨機雜湊值，必須實施動態追蹤：

追蹤流程：

請求主頁 /tw/characters。

利用 Regex db-histories-[a-zA-Z0-9_-]+\.js 掃描 HTML 以獲取最新路徑。

解碼防護： 請求 JS 資料時，必須顯式指定 response.encoding = 'utf-8'，否則中文名稱（如「莎赫拉查德」）會解析為亂碼。

4. 數據映射與提取 (Mapping)
   不再依賴單一 JSON，而是從歷史數據 JS 中提取「雙語對照表」：

英文 ID 提取： 從 costumeId 鍵值中過濾編號，例如 Scheherazade_3 -> Scheherazade。

中文名稱提取： 匹配 character:"中文名稱" 欄位。

對照邏輯： 請求伺服器時使用「英文 ID」，儲存資料夾時使用「中文名稱」，以優化使用者管理體驗。

5. 架構設計：解耦合 (Decoupling)
   為提高維護性，系統拆分為三個模組：

config.py (配置層)： 管理網域、Headers、路徑配置與下載後綴。

scraper.py (邏輯層)： 負責入口點掃描、編碼修正、雙語對照表生成。

downloader.py (執行層)： 負責批次下載、自動建立資料夾及智慧編號跳過機制。

6. 更新後的邏輯偽代碼
   Python

# 核心自動化流水線：

1. [初始化] 從 Config 載入 Headers 與 網域
2. [偵查] 爬取 HTML 入口點，提取帶有 Hash 的最新數據檔網址
3. [解析] 以 UTF-8 讀取數據檔，建立 { "中文名": "英文 ID" } 映射表
4. [執行] 遍歷映射表：
   FOR 角色中文名, 角色英文 ID IN 映射表:
   建立目錄: "BD2 角色素材/{中文名}/"
   FOR 編號 1 TO 9:
   FOR 每個 配置(後綴, 路徑):
   嘗試下載: 素材網域 + 路徑 + 英文 ID + 編號 + 後綴 + .webp
   IF 成功: 儲存檔案
   IF 該編號(i)所有格式均 404 AND i > 3:
   BREAK (判定該角色無更多服裝，切換下一位)
   AI 備忘錄 (給未來協作者)
   遇到 404 或 0 角色時的排錯順序：

Hash 過期？ 檢查 scraper.py 是否成功從首頁拿到新的 .js 網址。

編碼錯誤？ 檢查是否因未設定 utf-8 導致無法匹配中文 Key。

結構變更？ 檢查 JS 檔案內的 costumeId 或 character 關鍵字是否被更換。
