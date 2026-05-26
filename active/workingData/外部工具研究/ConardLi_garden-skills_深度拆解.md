# garden-skills 深度拆解報告

> 整理日期：2026-05-26
> 目的：工程規劃參考 — 詳細拆解每個 Skill 的設計思路與可採納的機制

---

## 一、web-design-engineer ★★★ 強烈推薦研究

> 核心定位：讓 AI 從「能用的網頁」→「令人驚艷的設計作品」

### 起源：Claude Design System Prompt

此 Skill 的靈魂來自 Anthropic 於 2026-04 發布的 Claude Design 官方系統提示（~420 行）。
ConardLi 將原版提煉成可攜式 Skill，並做了大量擴充。

> ⚠️ 注意：README 提到的 `dist/prompt/claude-design-system-prompt.md` 目前已從 repo 移除（404），
> 若要找原版 prompt 需要另外搜尋。

---

### 1.1 七步工作流（Step 0–6）

這個 Skill 最核心的設計是**強制流程**——AI 不能跳步。

| Step | 名稱 | 關鍵行為 |
|------|------|---------|
| **Step 0** | 事實查核 | **最高優先權**，在任何設計前先搜尋驗證：特定產品/SDK/事件是否存在、最新版本、規格。禁用語：「我認為...」「應該還是...」「可能還沒發布」 |
| **Step 1** | 理解需求 | 依情境決定要不要問：有完整 PRD → 直接做；只說「做個 Deck」→ 問清楚受眾/語氣；要求模糊 → 觸發 Design Direction Advisor |
| **Step 2** | 收集設計上下文 | 優先順序：使用者提供的資源 > 現有產品頁面 > 業界最佳實踐 > 使用者點名的風格錨點 > 從零開始（最後手段）。**「程式碼 >> 截圖」**——從代碼提取 token 比截圖更準確 |
| **Step 3a** | 四個定位問題 | 在寫 token 前先回答：①敘事角色（Hero/Data/Quote/Closing）②觀看距離（手機/筆電/投影）③視覺溫度（安靜/有活力/權威）④容量確認（內容塞不塞得下） |
| **Step 3** | 宣告設計系統 | **在寫第一行代碼前**，用 Markdown 宣告：顏色系統/字型/間距/圓角策略/陰影層次/動效風格。確認後才開始 → **硬性 Checkpoint 1** |
| **Step 4** | v0 草稿 | 先做骨架版（佔位符+佈局+設計 token），讓使用者早期糾偏。**不做完整版再發布** → **硬性 Checkpoint 2** |
| **Step 5** | 完整實作 | v0 確認後，補齊所有 state、動效、完整組件 → **關鍵決策點停頓 Checkpoint 3** |
| **Step 6** | 驗收清單 | 逐項走 Pre-delivery Checklist（見下方） |
| **Step 7** | 設計批評 | 5 維度評分（哲學一致性/視覺層次/工藝品質/功能性/原創性），各 0-10 分，輸出結構化診斷報告 |

---

### 1.2 Design Direction Advisor（當需求模糊時）

**觸發條件**：「做個好看的」「我不知道要什麼風格」「給我一些方向」

機制：不是問 10 個品味問題，而是從**明顯不同的流派**各挑一個，提出 3 個方向，讓使用者看到對比後做選擇。

#### 六大設計學派（25 個具名風格食譜）

| 學派 | 氣質 | 代表錨點 | 適合場景 |
|------|------|---------|---------|
| **Information Architecture（資訊架構）** | 理性、數據驅動、克制 | Pentagram / Edward Tufte / Bloomberg Terminal | 安全/專業/B2B/資料產品 |
| **Editorial / Minimalist（編輯/極簡）** | 留白、精緻排版、靜謐奢華 | Kenya Hara(MUJI) / Apple HIG / Aesop | 高端/高質感/安靜 |
| **Modern Tool / Builder SaaS（現代工具）** | 細線條、暖黑、單色調、等寬字體 | Linear / Vercel / Raycast / Notion | 開發工具/B2B SaaS/AI 工具 |
| **Motion / Experimental（動態/實驗）** | 大膽、生成性、感官衝擊 | Field.io / Active Theory / Resn | 品牌時刻/啟動影片 |
| **Brutalist / Raw（粗野）** | 反設計、誠實、未經打磨 | Balenciaga / Are.na / Bloomberg Businessweek | 差異化/反主流 |
| **Warm Humanist（溫暖人文）** | 親近、有機、手工感 | Mailchimp(早期) / Stripe Press / Headspace | 生活方式/教育/B2C |

**硬規則**：三個方向絕對不能來自同一個學派（否則使用者看不出差異）。

**25 個具名食譜（按學派分類）**：

| 學派 | 食譜 |
|------|------|
| Editorial/Minimalist | `apple-hig` · `muji-kenya-hara` · `aesop` · `dieter-rams-braun` · `monocle-magazine` |
| Information Architecture | `pentagram` · `vignelli-swiss-helvetica` · `bloomberg-terminal` · `tufte-dataink` · `nyt-the-daily` |
| Modern Tool | `linear` · `vercel-mesh` · `raycast` · `notion-pre-ai` |
| Motion/Experimental | `field-io` · `active-theory` · `resn-storytelling` |
| Brutalist/Raw | `are-na` · `bloomberg-businessweek-turley` · `balenciaga-post-2017` |
| Warm Humanist | `mailchimp-freddie` · `stripe-press` · `headspace-meditation` |
| Specialty/Genre | `y2k-retrofuturism` · `mid-century-modern` |

每個食譜是一個獨立 `.md` 文件，包含：具體色板、字型配對、間距系統、簽名動作、反模式。**按需載入，不預載全部**。

---

### 1.3 反 AI 陳腔濫調系統（Anti-Cliché）

這部分是這個 Skill 最有工程價值的思路：**不是美學偏見，而是保護品牌識別度。**

邏輯鏈：
> AI 默認 = 訓練數據平均值 = 所有品牌被平均 = **沒有任何品牌被識別出來**
> → AI 默認輸出稀釋了使用者的品牌身份

| 禁止模式 | 為什麼是垃圾 | 例外條件 |
|---------|------------|---------|
| 紫→粉→藍漸層 | 所有 SaaS/AI/Web3 都長這樣，是訓練數據收斂的結果 | 品牌本身在用，或目的是諷刺這個美學 |
| 圓角卡片+彩色左邊框 | Material/Tailwind 時代殘留，視覺噪音 | 使用者明確要求，或品牌規格包含 |
| Emoji 當 icon | 「不專業→貼 emoji」的反射行為 | 品牌本身用 emoji（Notion/Slack/早期 Linear），或受眾是兒童/輕鬆場景 |
| SVG 繪製人物/場景 | AI 畫的 SVG 人臉永遠對不齊，廉價感 | 幾乎永遠不用 |
| CSS 剪影代替產品圖 | 通用「科技感」，所有品牌都一樣 | **永遠不用**於品牌工作 |
| Inter / Roboto / Arial / Fraunces / system-ui | 太常見，讀起來像「Demo 頁」 | 品牌規格指定（且通常需要客製調整） |
| 虛假數字/Logo 牆/假見證 | 損害可信度，用戶會注意到 | **永遠不用** |

**Emoji 規則**：預設零 emoji。沒有 icon 時用 `[icon]` 佔位符，不用 emoji 填充。

---

### 1.4 品牌資產協議（Asset Protocol）

**「資產優先於規格」**——品牌識別靠資產，不靠 hex 碼。

| 資產類型 | 識別貢獻度 | 何時必須 |
|---------|----------|---------|
| **Logo（SVG/PNG，含深淺色版本）** | 最高——任何品牌都靠 Logo 被認出 | 任何品牌任務，不可妥協 |
| **產品圖**（實機/詳情/場景照） | 非常高——實體產品的主角就是產品本身 | 實體產品（硬體/包裝/消費品） |
| **UI 截圖**（最新版本，真實數據打碼） | 非常高——數位產品的主角就是介面 | 數位產品（App/SaaS/網站） |
| 色彩 token | 中——沒有上面的資產，品牌混在一起 | 輔助 |
| 字型 | 低——需要上面的資產才能落地 | 輔助 |

取得來源優先順序：官方媒體包/品牌網站 → 官方發布影片截幀 → App Store 截圖 → Wikimedia → AI 生成（基於官方參考）→ 誠實佔位符

---

### 1.5 六組顏色 × 字型起點（替代 AI 默認的 Inter + #3b82f6）

| 風格 | 主色 | 字型配對 | 適合場景 |
|------|------|---------|---------|
| 現代科技 | 藍紫 | Space Grotesk + Inter | SaaS / 開發工具 |
| 優雅編輯 | 暖棕 | Newsreader + Outfit | 內容 / 部落格 |
| 頂級品牌 | 近黑 | Sora + Plus Jakarta Sans | 奢侈品 / 金融 |
| 活潑消費 | 珊瑚紅 | Plus Jakarta Sans + Outfit | 電商 / 社交 |
| 極簡專業 | 藍綠 | Outfit + Space Grotesk | 儀表板 / B2B |
| 工藝溫暖 | 焦糖 | Caveat + Newsreader | 食品 / 教育 |

技術面：顏色使用 `oklch()` 色彩空間（感知均勻），不用 HSL 亂猜。

---

### 1.6 技術規格（關鍵硬規則）

**React + Babel（Inline JSX）三大不可違反規則：**

1. **永遠不用 `const styles = { ... }`**——多組件共存時會靜默互蓋。要加命名空間：`const terminalStyles` / `const headerStyles`，或直接用 inline `style={{...}}`，**不能用 `styles` 作為變數名**

2. **`<script type="text/babel">` 各 block 不共享 scope**——要跨檔案共享組件，必須在檔案末尾 `Object.assign(window, { Terminal, Line })`

3. **不能用 `scrollIntoView`**——在 iframe 嵌入環境裡會打斷外層捲動。改用 `element.scrollTop = ...` 或 `window.scrollTo({...})`

**動效技術選擇原則（從最輕量到最重）：**
1. CSS transitions/animations（覆蓋 80% 微互動）
2. React state + setTimeout / requestAnimationFrame
3. 自訂 `useTime + Easing + interpolate`（時間軸驅動）
4. Popmotion（兜底）
→ 避免 Framer Motion / GSAP / Lottie（bundle 過重，React 18 inline Babel 相容問題）

---

### 1.7 輸出類型規格

| 輸出類型 | 關鍵規格 |
|---------|---------|
| **互動原型** | 無標題頁、設備框架（iPhone/Browser）、至少 3 個 Tweaks 變體、完整 state 覆蓋（hover/focus/active/disabled/loading/empty/error） |
| **HTML 簡報** | 固定 1920×1080，JS `transform: scale()` 縮放，鍵盤導航（←→/Space），localStorage 持久位置，1-indexed 編號（01 Title, 02 Agenda...），`data-screen-label` 屬性 |
| **數據視覺化儀表板** | Chart.js（簡單）或 D3.js（複雜），`ResizeObserver` 響應式，深/淺色切換，高 data-ink ratio |
| **動態/影片 Demo** | 提供 play/pause + scrubber，跳過「標題頁」直接進入內容 |

---

### 1.8 Tweaks 面板（即時調參）

每個交付物都要加的調參控制器：
- 右下角浮動面板，標題統一叫「**Tweaks**」
- 關閉時完全隱藏（不影響設計展示感）
- 多變體場景用 Tweaks 的下拉/切換，而不是建多個檔案
- 即使使用者沒要求，也主動加 1-2 個創意 tweak（讓使用者看到可能性）

---

### 1.9 Pre-delivery Checklist（交付前必過的項目）

```
□ Step 0 有跑（有提到品牌/產品時）
□ 品牌任務：brand-spec.md 存在；Logo 是真的；產品圖是真的
□ 瀏覽器 console 無錯誤/警告
□ 在目標裝置/viewport 正確渲染
□ 互動組件有完整 state
□ 無文字溢出，有 text-wrap: pretty
□ 所有顏色來自 Step 3 宣告的設計系統，無流氓色調
□ 無 scrollIntoView
□ React 專案：無 const styles={}；跨檔案組件走 Object.assign(window,{})
□ 無 AI 陳腔濫調（紫粉漸層/emoji 濫用/左邊框卡片/Inter/Roboto）
□ 無填充內容，無虛假數據
□ 語義命名，結構清晰
□ 視覺品質達 Dribbble / Behance 展示水準
```

---

### 1.10 關聯參考文件

此 Skill 的內容分散在多個按需載入的文件中（不全部預載）：

| 文件 | 何時讀 |
|------|--------|
| `references/advanced-patterns.md` | 需要滑動引擎/設備框架/動效時間軸/暗色模式/圖表 |
| `references/design-directions.md` | 模糊需求時的六流派擴展說明 |
| `references/style-recipes/INDEX.md` | 瀏覽 25 個食譜目錄 |
| `references/style-recipes/<anchor>.md` | 使用者點名風格時，只讀那一個 |
| `references/critique-guide.md` | 五維度評分詳細量規 |

---

## 二、web-video-presentation ★★★ 高潛力

> 核心定位：文章/腳本 → 可錄屏的「偽裝成視頻的網頁」，可選 TTS 合成

### 2.1 四階段工作流

```
Phase 1  內容編寫        → script.md + outline.md
       ↓
Checkpoint Plan（硬節點）  → 對齊 5 件事：稿子/outline/主題/素材/開發模式
       ↓
Phase 2  網頁開發        → 脚手架 → 第1章主線程驗收 → 第2~N章（A/B/C模式）
       ↓
Checkpoint Audio（硬節點） → 是否合成音頻
       ↓
Phase 3  音頻合成（可選）
       ↓
Phase 4  錄屏 + 後期
```

### 2.2 三種開發模式

| 模式 | 流程 | 特點 |
|------|------|------|
| **A 逐章確認（默認）** | 每章做完→停→驗收→下一章 | 風險最低，節奏最穩 |
| **B 第1章後順序開發** | 第1章驗收後，2~N章主線程順序做完再統一驗收 | 速度中，不支援並行時用 |
| **C 第1章後並行（subagent）** | 第1章驗收後，2~N章用多個 subagent 並行做 | 最快，但各章風格會有差異（設計預期） |

**使用者隨時可切換模式**，第 N 章後說「剩下的並行」就切 C 模式。

### 2.3 十條核心原則（一句話版）

| # | 原則 | 說明 |
|---|------|------|
| 1 | 16:9 固定舞台 | 1920×1080 + transform scale，無響應式 |
| 2 | 全局 step 計數器 | 章節是 step 的純函數，無定時器 |
| 3 | 每步獨占整屏 | `if (step === N) return <FullScene />` |
| 4 | 口播節拍 = step | 一節拍 = 一 step = 一個聚焦想法 |
| 5 | 隱藏邊角控件 | 進度條/翻頁器默認 opacity: 0 |
| 6 | 舞台無 chrome | 無 header/footer/頁碼/品牌條 |
| 7 | **內容驅動動畫** | 先找內在動作，找不到才用入場動畫兜底 |
| 8 | 多點逐個揭示 | 1 項 = 1 step，禁同步 stagger 上 N 項 |
| 9 | 整片同一主題 | 顏色/字體走 token，其他章節自由 |
| 10 | 雙源原則 | script 定節拍，article 定畫面密度（信息池） |

### 2.4 音頻合成（TTS）

內建兩個 provider，provider-agnostic 設計：
- **MiniMax（`mmx-cli`）**：默認，中文音色穩
- **OpenAI TTS（`curl + OPENAI_API_KEY`）**：大多數用戶已有 key
- 擴充接口：ElevenLabs / edge-tts（免費）/ macOS say（離線）/ Azure / Google Cloud

### 2.5 `narrations.ts` 唯一真相源

每章的 narrations.ts 是 step 數和音頻合成的唯一真相。
章節 .tsx 裡 `if (step === N)` 的最大 N + 1 必須等於 `narrations.length`。
確保 5 個地方永遠同步：script / outline / 章節代碼 / chapters.ts / 音頻文件。

### 2.6 主題系統（23 個內建主題）

動態讀取 `themes/*/theme.json`（不硬編碼清單），每個 theme 有：
- `nameZh`（中文名）
- `descriptionZh`（一句話描述）
- `bestFor`（適合場景）
- `mood`（氣質）

AI 根據腳本的內容類型/關鍵詞/語氣，主動推薦 2-3 個最匹配的主題。

---

## 三、kb-retriever ★★ 有知識庫時才裝

> 核心定位：從本地知識庫精準檢索，不把整份文件塞進 context

### 3.1 核心設計：漸進式分層檢索

不一次把所有文件讀進來，而是靠層次化的 `data_structure.md` 索引文件導航，逐步縮小範圍再讀具體內容。

```
knowledge/
├── data_structure.md        ← 根目錄索引
├── domain-A/
│   ├── data_structure.md   ← 子目錄索引
│   └── files...
└── domain-B/
    └── ...
```

### 3.2 強制流程：先學習，再處理

遇到 PDF 或 Excel 前：
- **PDF**：必須先讀 `references/pdf_reading.md`（pdftotext / pdfplumber 用法）
- **Excel**：必須先讀 `references/excel_reading.md` + `references/excel_analysis.md`（pandas 方法）

禁止行為：
- ❌ 未讀參考文件就直接處理 PDF
- ❌ 未讀參考文件就直接處理 Excel
- ❌ 用 Glob 判斷目錄是否存在（要用 `test -d`）

### 3.3 迭代控制（最多 5 輪）

每輪：關鍵詞 → 選文件 → 執行檢索 → 分析 → 判斷是否足夠
→ 達上限但還沒找到 → 明確告知用戶，給最接近的資訊

### 3.4 知識庫根目錄確認規則

1. 用戶有指定路徑 → 用指定路徑
2. 默認用當前目錄下的 `knowledge/`
3. `knowledge/` 不存在 → **停下來問用戶**，不猜測

---

## 四、工程規劃建議

### 哪些機制值得採納

根據你的使用場景（製作設計作品），以下機制有直接參考價值：

**立即可用（直接安裝 Skill）**：
- `web-design-engineer`：你提到「高度吻合之後要做的類型」——這個最值得直接安裝
- 六步工作流可以作為你自己做前端工作的 SOP 模板

**值得研究的設計思路（可融入自己的規範）**：
- **四個定位問題（Step 3a）**：敘事角色/觀看距離/視覺溫度/容量——這個框架做任何視覺設計都適用
- **Anti-Cliché 邏輯鏈**：「AI 默認 = 訓練數據平均 = 品牌稀釋」——寫進你的設計規範
- **品牌資產優先順序**：資產 >> 規格（hex 碼），這是很多設計師也沒想清楚的
- **Tweaks 面板模式**：用單檔案 + 控制面板取代多個變體檔案——值得作為 HTML 原型的標準做法
- **雙源原則（web-video-presentation）**：script 定節奏，article 定畫面密度——做任何影片都適用

**架構模式（偏學習）**：
- 按需載入參考文件（不預載全部）——對 Skill/Agent 設計有參考意義
- 硬性 Checkpoint 機制——保證 AI 不會跳步直接開工

### 安裝決策

| Skill | 建議 | 理由 |
|-------|------|------|
| `web-design-engineer` | ✅ 現在就裝 | 直接解決「AI 設計輸出太 generic」的問題 |
| `web-video-presentation` | ✅ 有影片需求就裝 | Harness 自動化影片製作的基礎設施已完整 |
| `kb-retriever` | ⏳ 有知識庫需求再裝 | 需要本地 `knowledge/` 目錄才有效，目前不急 |
| `gpt-image-2` | ⏳ 有圖片生成需求再裝 | 需要 GPT-Image-2 API 才有意義 |

---

## 五、Reference 文件展開版（正文只提指針，這裡是原文精華）

### 5.1 advanced-patterns.md — 代碼模板庫

#### Responsive Slide Engine（固定尺寸簡報自動縮放）

關鍵約定：
- 內部陣列 0-indexed，**顯示給使用者的永遠 1-indexed**
- 每個 slide 加 `data-screen-label="01 Title"` 方便索引
- 控制按鈕放在 `.stage` **之外**，避免小螢幕失效

#### Device Simulation Frames（設備模擬框架）

`IPhoneFrame`：狀態欄（時間 + 電量）+ 內容區 + 底部返回條  
`BrowserFrame`：標題欄（三個點 + URL）+ 內容區

#### Animation Timeline Engine（動效時間軸引擎）

```jsx
// 0-1 的時間軸驅動，自動循環
const useTime = (duration = 5000) => { ... };

// Easing 函數庫
const Easing = {
  linear, easeInOut, easeOut, easeIn, spring
};

// 用法
const { time } = useTime(3000);
const opacity = interpolate(time, 0, 1);
const x = interpolate(time, -100, 0, Easing.spring);
```

#### oklch 色彩系統最佳實踐

```css
:root {
  --primary-h: 250;
  --primary: oklch(0.55 0.25 var(--primary-h));
  --primary-light: oklch(0.75 0.15 var(--primary-h));
  --primary-dark: oklch(0.35 0.2 var(--primary-h));

  /* 灰階：L 值感知均勻 */
  --gray-50: oklch(0.98 0.002 250);
  --gray-900: oklch(0.21 0.014 250);
}
```

> ⚠️ 字型推薦表：Plus Jakarta Sans / Outfit / Space Grotesk / Sora / Newsreader / Caveat / JetBrains Mono——避免 Inter / Roboto / Arial / Fraunces（AI 默認指紋）

---

### 5.2 design-directions.md — 六大學派完整分類（Advisor 擴充版）

> 使用時機：需求模糊（「做個好看的」「我不知道要什麼風格」）

**規則：3 個方向必須來自不同行（不同學派），避免使用者看不出差異**

| 學派 | 定位 | 推薦錨點（樣本台詞） |
|------|------|-------------------|
| **Information Architecture** | 理性/B2B/資料驅動 | 「Pentagram 式資訊架構——儀表板成為排版關係的系統，標題做重視覺工作，其他都退場。最適合機構公信力 + 數據是主角」 |
| **Editorial / Minimalist** | 留白/高端/靜謐奢華 | 「Kenya Hara 式編輯極簡——頁面 80% 留白，一個 serif 標題帶情感重量，產品錨定在暖白底色。最適合頂級定位比功能密度更重要的場景」 |
| **Modern Tool / Builder SaaS** | 開發工具/B2B SaaS | 「Linear 式現代工具美學——暖黑底色，1px 細邊框，單色強調少於 5% 像素，等寬快捷鍵提示。最適合技術受眾，「嚴肅但有設計感」比「趣味易親近」更重要。這個食譜是防 AI 默認輸出最直接的武器」 |
| **Motion / Experimental** | 動態/品牌時刻 | 「Field.io 式動態主導——頁面靠 scroll 驅動序列自我生成。最適合發布時刻，觀眾會分享片段。⚠️ 這是最耗工的選擇，預算要充足」 |
| **Brutalist / Raw** | 反設計/強烈個性 | 「Are.na / Bloomberg 式粗野主義——系統字體 on purpose，無圓角，無陰影，排版暴力。⚠️ 半套粗野主義 = 看起來壞了，要麼 all-in 要麼換別的」 |
| **Warm Humanist** | 親近/教育/B2C | 「Stripe Press / 早期 Mailchimp 溫暖感——人文 serif，奶油色系，插圖有手工觸感。語氣是「剛好是專家的朋友」，不是「向客戶陳述的專家」」 |

**使用者選擇後**：
- 直接確認 → 寫入 `brand-spec.md`，走主流程
- 混搭（「A 的顏色 + C 的佈局」）→ 書面確認再執行
- 「都不對」→ 問一個縮窄問題，再提 3 個新方向
- 「你選」→ 選最保守的（通常是 Editorial/Minimalist），說明理由，先做 5 分鐘 v0

---

### 5.3 style-recipes/INDEX.md — 三個交叉索引

> 使用模式：按需載入。知道錨點 → 直接讀那一個 `.md`；不知道 → 看下表

**Index 2 — 按場景**

| 場景 | 首選食譜 |
|------|---------|
| B2B SaaS / 開發工具 | `linear` · `vercel-mesh` · `raycast` · `pentagram` |
| 頂級消費 / 生活方式 | `aesop` · `muji-kenya-hara` · `stripe-press` · `monocle-magazine` |
| 資料產品 / 儀表板 | `bloomberg-terminal` · `tufte-dataink` · `vignelli-swiss-helvetica` |
| 編輯 / 長文 | `nyt-the-daily` · `monocle-magazine` · `stripe-press` |
| 發布時刻 / awwwards | `field-io` · `active-theory` · `resn-storytelling` · `vercel-mesh` |
| 差異化 / 反主流 | `are-na` · `bloomberg-businessweek-turley` · `balenciaga-post-2017` |
| 親民 B2C / 社群 | `mailchimp-freddie` · `headspace-meditation` · `notion-pre-ai` |
| 復古 / 年代感 | `y2k-retrofuturism` · `mid-century-modern` |

**Index 3 — 按深色/淺色**

| 模式 | 食譜 |
|------|------|
| 淺色優先 | `apple-hig` · `muji-kenya-hara` · `aesop` · `dieter-rams-braun` · `monocle-magazine` · `pentagram` · `nyt-the-daily` · `stripe-press` · `headspace-meditation` · `mailchimp-freddie` · `mid-century-modern` |
| 深色優先 | `linear` · `vercel-mesh` · `raycast` · `bloomberg-terminal` · `field-io` · `active-theory` · `resn-storytelling` · `y2k-retrofuturism` |
| 兩者皆可 | `vignelli-swiss-helvetica` · `tufte-dataink` · `notion-pre-ai` · `are-na` · `bloomberg-businessweek-turley` · `balenciaga-post-2017` |

**共通反模式（25 個食譜全部適用）**

| 反模式 | 後果 |
|--------|------|
| 同一頁面混兩個食譜 | 看起來困惑，不是創意 |
| 半套粗野主義 / Y2K | 看起來壞掉，不是大膽 |
| 把食譜字體換成 Inter | 抹掉排版 DNA，退回 AI 默認 |
| 自己加「平衡色」 | 食譜的限制色板 IS 食譜，多加就壞 |
| 默默偏離食譜「讓畫面有活力」 | 每個 AI 默認添加都讓食譜向均值靠近 |
| 用 CSS 假造食譜的攝影風格 | 說明缺素材，給 placeholder，不要用形狀代替 |

---

### 5.4 critique-guide.md — 設計評審詳細量規

#### 五維度評分說明

| 維度 | 9–10 分標準 | 常見失分點 |
|------|------------|----------|
| **哲學一致性** | 每個細節都能溯源到所選設計方向，無「外來元素」 | 選了極簡但塞滿了卡片 |
| **視覺層次** | 眯眼看還能辨認層次（Squint Test）；標題/副標/本文大小比 ≥ 2.5×（Hero 建議 4-6×） | 中層（副標題/說明文字）全部塌成一個大小 |
| **工藝品質** | 8pt 格線系統（8/16/24/32/48/64）；顏色 ≤ 4 個（主+輔+強調+中性）；字型 ≤ 2 個 | 間距隨意、顏色超過 5 種 |
| **功能性** | 刪除測試：刪掉這個元素設計是否變差？否 → 刪掉 | CTA/關鍵資訊不在最顯眼位置 |
| **原創性** | 至少一個「出乎意料但正確」的決定；通過 AI 陳腔濫調清單 | 見上方 Anti-Cliché 表 |

**按輸出類型的維度權重**

| 輸出類型 | 首要 | 其次 | 可放寬 |
|---------|------|------|--------|
| 著陸頁 / 行銷網站 | 功能性 / 視覺層次 | 原創性 | — |
| 儀表板 / 資料產品 | 功能性 / 工藝品質 | 視覺層次 | 原創性 |
| HTML 簡報 | 視覺層次 / 功能性 | 工藝品質 | 原創性 |
| 品牌發布動畫 | 原創性 / 視覺層次 | 哲學一致性 | 功能性 |
| 文件網站 | 功能性 / 視覺層次 | 工藝品質 | 原創性 |

**Top 10 常見問題（速查）**

| # | 問題 | 修法（要有具體數值） |
|---|------|-------------------|
| 1 | AI 科技陳腔（漸層光球/電路板/機器人臉） | 用抽象隱喻取代字面符號 |
| 2 | 字型大小層次不足（< 2.5×） | 標題至少 3× 本文（Hero 建議 6×） |
| 3 | 顏色超過 5 種 | 限主色 + 輔色 + 強調色 + 灰階 |
| 4 | 間距不一致，無系統 | 採 8pt 格線（8/16/24/32/48/64） |
| 5 | 留白不足，內容塞滿 | 留白應 ≥ 40%（極簡 60%+） |
| 6 | 字型超過 3 種 | 最多 2 種（展示 + 本文） |
| 7 | 對齊方式混亂 | 全局統一對齊，Hero 才置中 |
| 8 | 裝飾蓋過內容 | 刪除測試：移除後沒變差 → 刪 |
| 9 | Cyber neon 過度（GitHub Dark + 霓虹光） | 深色模式用非預設底色（帶暖調的近黑） |
| 10 | 資訊密度與媒介不符（簡報一頁滿文字） | 簡報：1 頁 1 核心；圖：1 個視覺焦點 |

**評審報告格式（複製即用）**

```markdown
## Design Critique

**Overall: X.X / 10** [Excellent (8+) / Good (6–7.9) / Needs work (4–5.9) / Failing (<4)]

**By dimension**:
- Philosophy alignment: X / 10 — [一句理由]
- Visual hierarchy: X / 10 — [一句理由]
- Craft quality: X / 10 — [一句理由]
- Functionality: X / 10 — [一句理由]
- Originality: X / 10 — [一句理由]

### Keep
- [用設計語言說，不說「顏色很好看」，說「靜謐的赭色對暖白底色讀來自信而編輯感」]

### Fix (sorted by severity)

**1. [問題名]** — ⚠️ Critical / ⚡ Important / 💡 Polish
- Current: [現在的樣子]
- Why: [錨定到原則，不說「感覺不好」]
- Fix: [具體數值，「標題從 32px 增到 56px」而不是「標題大一點」]

### Quick Wins (top 3)
- [ ] [影響最大且改起來最快的]
```

---

### 5.5 CHAPTER-CRAFT.md — web-video-presentation 章節開發鐵律

> 這份文件是每章開始開發前的**強制必讀**。

#### 三條通過標準（一眼判斷這章合不合格）

1. **不像 PPT**：無頁眉頁腳，突出主視覺元素，不是翻頁幻燈片感
2. **看起來舒服**：配色/字體/節奏讓人放鬆，不大量純文字，不出現太小字體
3. **有視覺衝擊**：畫面在「演」東西，不只是文字堆砌，元素隨進度逐步展現

#### 底線（不可違反）

> **每章至少 1~2 處 CSS/SVG/Canvas/JS 視覺演示。整章只有純文字 = 驗收不過 = 回去重做。**

視覺演示範例：數字遞增、橫條增長、排名交換、流程節點依次點亮、對比被一刀切開、粒子聚攏成形、模擬終端交互、模擬 AI 對話視窗、模擬目錄樹

#### 逐步揭示（最重要的一條）

> 清單/列表時，**禁止一個 step 把 X/Y/Z 全部 stagger 上來**

正確做法：
- 一項 = 一個 step
- 講到 Y 時，X 灰化保留做上下文，Y 亮起
- 判斷標準：「講者會一個一個念出來嗎？會 → 必須逐個揭示」

#### 雙源原則（節奏 vs 畫面密度）

- **節奏/順序/節拍** 跟 `script.md` 口播稿
- **畫面細節/數據/引用/案例** 回 `article.md` 原文章

> 如果只用口播稿內容做章節 → 畫面等於把口播打字打了一遍 → 那就是 PPT

#### 代碼層最小約束（換主題不破的底線）

**必須用 token**：
- 顏色：`--shell` / `--surface` / `--text` / `--accent` 等 → **禁硬編碼 hex / rgb**
- 字體：`--font-display-cn` / `--font-display-en` / `--font-body` / `--font-mono` → **禁硬編碼字體名**
- Primitive class：`.hero-num` / `.rule` / `.card` / `.stage-frame` → 接主題性格

**可自由硬編碼**（解鎖章節設計自由）：
- 字號（想要 80px 就寫 80px）
- 間距 / padding / margin
- 動畫時長 / 緩動 / keyframe
- grid 佈局尺寸

**其他工程紅線**：
- 不用 `setTimeout` / `setInterval` 驅動動畫 → 用 CSS keyframes
- 可交互元素加 `data-no-advance` 防誤推進 step
- 章節代碼物理隔離：獨立文件夾、獨立 CSS 前綴，不跨章 import
- `narrations.ts` 長度 = 章節中 `if (step === N)` 最大 N + 1
- **每步視覺動畫時長 ≤ 口播時長**（口播字數 ÷ 4 ≈ 秒數），超出 → 寫更長口播 / 拆 step / 調動畫速度

#### 完工自檢清單（寫完每章強制執行，不可跳過）

```
□ 每章至少 1~2 處 CSS/SVG/Canvas/JS 視覺演示
□ 不同 step 的主導動作不一樣（全章一種動畫 → 回去重做）
□ 字號大、留白舒服、配色舒服
□ 清單/列表逐個揭示，1 項 = 1 step
□ 畫面信息比口播稿多（有回原文章抽細節）
□ 沒有紫粉漸層 / 圓角彩色邊框 / emoji / 假數據 / 假 logo
□ 缺的素材用 placeholder，不是 fake
□ 顏色和字體家族全部走 token（無硬編碼 hex / 字體名）
□ hero 數字 / 卡片 / 分割線 / 舞台用 primitive class 接主題
□ npx tsc --noEmit 通過（不通過禁止回報「做完了」）
□ 章節代碼物理隔離：獨立 CSS 前綴，未跨章 import
□ narrations.ts 存在，長度正確，與 script.md 語義一致
□ 每步視覺動畫時長 ≤ 口播時長
```

---

### 5.6 gpt-image-2 — 提示詞 JSON 方法論（prompt-writing.md）

> 此份文件定義 gpt-image-2 的模板設計總規範，不是某個具體場景的模板。

#### 何時用 JSON 模板（vs 自然語言）

**適合 JSON**：畫面元素多、多功能區域、含 UI 結構（商品卡/評論區/圖例）、需多變體、需支援「使用者指定/默認/隨機」三模式  
**不用 JSON**：簡單單主體圖、無複雜佈局、使用者只想快速試方向

#### JSON 骨架

```json
{
  "type": "模板類型",
  "goal": "圖像用途",
  "subject": {},      // 主體：人物/商品/城市
  "scene": {},        // 場景/背景/氛圍
  "layout": {},       // 區域組織方式
  "style": {},        // 風格/材質/色彩/光線
  "details": {},      // 局部細節（標注/評論/圖例）
  "constraints": {}   // 必須有什麼/必須避免什麼
}
```

#### 參數三分類

| 類型 | 說明 | 範例 |
|------|------|------|
| **核心（必問）** | 缺失嚴重影響結果 | 主體是誰、商品名稱、主題 |
| **可默認** | 先用默認值，不影響正常工作 | 背景色、次級按鈕文案 |
| **可隨機** | 允許自動補全，但要在風格範圍內 | 路人暱稱、次級裝飾元素 |

#### 參數格式

```text
{argument name="host name" default="Elon Musk"}
```

#### 18 大圖像分類（索引用）

```
ui-mockups / product-visuals / infographics / poster-and-campaigns /
slides-and-visual-docs / portraits-and-characters / scenes-and-illustrations /
editing-workflows / avatars-and-profile / storyboards-and-sequences /
grids-and-collages / branding-and-packaging / typography-and-text-layout /
assets-and-props / academic-figures / technical-diagrams / maps / (其他)
```

**特殊場景的必要額外字段**：
- **Storyboard**：`continuity` 必填（聲明 N 個 panel 是連續敘事）；每鏡：「景別 + 主體動作 + 光線/情緒」三要素；遠/中/近/POV 要混搭
- **Lineup/Catalog**：每 panel 必須各自有 `theme_color` + `symbol`，否則模型畫成同一張；必須有 `legend`（等級 key）
- **Split 海報（行程地圖）**：`alignment_rule` 必填，左右兩欄編號/順序必須嚴格對齊

---

## 七、附記：Claude Design System Prompt 去哪了

README 提到原始 Claude Design 系統提示保存於 `dist/prompt/claude-design-system-prompt.md`，
但目前已 404，可能在近期更新中被移除。

若需要研究原版 prompt，可以：
1. 搜尋 GitHub 早期 commit（`git log --diff-filter=D --name-only` 可找已刪文件）
2. 搜尋「Claude Design system prompt」—— 社群應有人存檔
