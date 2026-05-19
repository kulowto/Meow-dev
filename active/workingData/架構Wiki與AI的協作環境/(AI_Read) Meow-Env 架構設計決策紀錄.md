---
文件類型: AI_Read
版本: v0.9（客戶部署 SOP + 來源標記慣例確認）
建立: 2026-05-19
最後更新: 2026-05-19
狀態: 草稿，架構方向已定，細節待實作時補充
---

# Meow-Env 架構設計決策紀錄

> **本文件的目的**
> 記錄 Meow-Env 系統的設計思路、關鍵決策與取捨理由。
> 未來的 AI（包含本系統的 AI 與衍生的客戶系統）讀這份文件，可以理解「為什麼這樣設計」，以及「要擴充或維護時應該遵守什麼原則」。

---

## 一、系統定義

### Meow-Env 是什麼
個人 AI 協作環境，由五個子系統組成：一個通用框架、三個個人實例、一個開發暫存區。

### 五個子系統的職責

| 系統 | 縮寫 | 角色定位 | 比喻 |
|------|------|---------|------|
| Meow-Framework | MF | 通用框架（客戶可 fork） | 建築藍圖 |
| Meow-Agent | MA | 指揮官 / 個人秘書 | 大腦 + 指揮中心 |
| Meow-Wiki | MW | 個人知識庫 | 長期記憶 / 圖書館 |
| Meow-Tools | MT | 個人工具箱 | 工作台 |
| Meow-Dev | MD | 開發暫存區 / Playground | 實驗室草稿桌 |

### 為什麼需要 Meow-Dev 獨立出來
- workingData 的「不屬於任何區，但可調用任何區」的性質，與它住在 MT 裡產生語義衝突
- 需要 git 版控（跨裝置同步，Mac + Windows）
- 是真正的中立區，不被任何系統擁有

---

## 二、核心設計原則

### 已確認的設計決策

#### 決策 1：MA 為 God Object，屬刻意設計
- **結論**：MA 扮演秘書/指揮官角色，具備最高調用權限，可指派任務給其他 AI 角色
- **理由**：這是個人 AI 系統的核心設計意圖，MA 知道所有資源並統籌調度
- **注意**：MA 的「高權限」是刻意的，不是耦合問題，但 MA 的 CLAUDE.md 不應 hardcode 其他系統的內部路徑（這才是要解決的問題）

#### 決策 2：workingData = Playground（開發暫存區）
- **結論**：workingData 是系統性的開發暫存區，類似程式開發的 Sandbox 概念
- **規則**：
  - 不屬於任何特定系統，但可調用任意系統的資源
  - 所有未完成、未歸類的開發材料統一在此暫存
  - 確認定位後，依性質遷移至對應系統的正確位置
- **畢業流程**：workingData → 確認性質 → 遷移至 Framework / MA / MW / MT 的正確層

#### 決策 3：全域治理文件需要拆分
- **問題**：目前 workingData 裡的 `架構Wiki與AI的協作環境/` 同時包含「通用框架規則」和「個人設定」，混在一起
- **結論**：需拆分為兩層
  - **Framework 層**（通用，客戶可 fork）：角色骨架模板、通用協作規則、Prompt 框架
  - **個人層**（留在各 repo）：Meow 特有設定、個人偏好、具體專案決策

#### 決策 6：Meow-Dev 為第五個獨立 Repo（開發暫存區）
- **結論**：建立獨立的 `Meow-Dev/` repo，不隸屬於任何系統
- **理由**：
  - 需要 git 版控跨裝置同步（Mac + Windows）
  - 語義上是中立區，不應被 MT「擁有」
  - 可調用所有系統的資源，但不屬於任何系統
- **結構**：`active/`（開發中）+ `_done/`（完成待蒸餾）+ `_done/archive/`（蒸餾後的歷史快照）

### 決策 7：歸檔機制採用「內容蒸餾管線」
- **問題**：一份開發文件可能同時包含多個系統的材料（工具規格 + 設計思維 + 可推廣模式）
- **結論**：歸檔 Agent 讀取 `_done/` 中的文件，依各系統的「接受準則」，萃取並產生多份衍生品分別送入對應系統；原始文件保留至 `_done/archive/`
- **關鍵原則**：
  - 衍生品進入目的地後即獨立演化，不與原始文件同步
  - 各系統的 INDEX.md 需包含「我接受哪類內容 / 我不接受哪類內容」
  - 歸檔 Agent 透過 REGISTRY → 各系統 INDEX.md 取得接受準則後再判斷路由
- **蒸餾流程**：
  1. 開發者把完成的工作從 `active/` 移至 `_done/`
  2. 歸檔 Agent 讀 REGISTRY，找到所有系統的 INDEX.md
  3. 歸檔 Agent 讀 `Meow-Dev/classification-logic.md`（取得分類原則與案例樣本）
  4. AI 分析文件內容，比對各系統接受準則，判斷哪些段落去哪裡
  5. 產生蒸餾預覽清單（**半自動**：等待人工確認；**全自動**：直接執行）
  6. 確認後，為每個系統產生衍生品（重新格式化，符合目標系統慣例）
  7. 原始文件移入 `_done/archive/`；本次決策記錄進 `classification-logic.md`

### 決策 8：歸檔 Agent 採用半自動模式，搭配分類邏輯文件累積訓練樣本
- **結論**：初期半自動（人工審核），搭配 `classification-logic.md` 累積決策案例與抽象規則
- **理由**：目前沒有足夠的分類樣本，全自動會導致路由錯誤；需要人工標記建立樣本庫
- **切換條件**（任一達到即可切換全自動）：
  - 累積 20 個以上案例，且最近 10 個案例無人工修改
  - 人工手動在 `classification-logic.md` 更新狀態
- **分類邏輯文件結構**：
  - 第一層：分類原則（從案例中抽象出的通用規則，初期為空，隨案例累積補充）
  - 第二層：案例庫（具體決策記錄，含 AI 提案 + 人工審核結果 + 學到的規則）
  - 第三層：邊緣案例（容易判斷錯的特殊情境）
  - 第四層：自動化狀態（目前模式 + 切換條件 + 達成進度）

#### 決策 10：Meow-Framework 內部資料夾結構定案
- **結論**：`governance/` 下分四個子目錄，依文件性質分類
- **目錄用途**：

| 子目錄 | 放什麼 | 適用客戶 |
|--------|--------|---------|
| `collaboration/` | AI 行為規則（四條強制規則、Karpathy 原則、資料傳遞格式） | 所有客戶 |
| `roles/` | 角色 & 領域骨架模板 | 需要多角色系統的客戶 |
| `prompts/` | 通用 Prompt（學習框架、壓縮格式、架構圖規範） | 所有客戶 |
| `knowledge/` | 知識管理架構概念（LLM-Wiki.md：三層知識庫結構說明） | **有 Wiki 子系統的客戶才需讀** |

- **注意**：`knowledge/` 不是所有客戶都強制讀，Framework INDEX.md 應標明使用條件
- **目標結構**：
  ```
  Meow-Framework/
  ├── CLAUDE.md
  ├── governance/
  │   ├── collaboration/
  │   ├── roles/
  │   ├── prompts/
  │   └── knowledge/
  │       └── LLM-Wiki.md
  └── INDEX.md
  ```

#### 決策 11：文件繼承模型採「分而治之」設計
- **結論**：三層繼承結構，AI 在執行任何任務前依序讀取，逐層修正精度
- **核心思路（使用者原話）**：
  > 通用的是最上層，6~8 成都可以參考這個架構執行，但一定會有因為專業領域不同，導致細節處理上的缺失。
  > 要處理的問題，就是要仰賴這個專業領域下的歷史決策文件，來矯正或補上這個缺口。
  > 這些文件是基於通用架構上、在這專業領域裡的疏漏，用做修正用途，提供細節要如何改進、有什麼常見錯誤要避免。
- **三層結構**：

| 層級 | 文件位置 | 覆蓋率 | 用途 |
|------|---------|--------|------|
| **通用層** | Meow-Framework | 60–80% | 任何領域都適用的通用架構方法論 |
| **領域修正層** | MT（或對應系統）| 補剩餘 20–40% | 該領域的細節修正、常見錯誤、邊緣案例 |
| **知識資產層** | Meow-Wiki | — | 以上兩層的精華提煉，供未來「從零重建」時快速還原精度 |

- **適用範圍**：工具開發 / 系統設計 / 角色分配 / 任何需要 AI 「執行好」的任務，都依此繼承順序讀文件
- **MW 存在理由**：「知識財產」的永久庫。有了 MW 的文件，即使 MT 或 MF 的內容重做，也能用較精準的方式重建同樣的成果

#### 決策 12：各系統 INDEX.md 接受準則（依三層繼承模型定義）

**Meow-Framework（通用層）**
- 接受：普遍適用的 AI 協作規則、角色骨架模板、任何領域通用的 Prompt 框架、知識管理架構概念
- 不接受：特定系統的路徑 / 個人偏好 / 單一工具的操作步驟

**Meow-Tools（領域修正層）**
- 接受：工具規格書（spec doc）、可執行程式碼、操作 SOP、**工具開發歷史決策**（為什麼這樣設計、踩過的坑、領域內的修正補丁）
- 不接受：純概念定義（沒有對應到 MT 工具的）、跨領域的通用洞察

**Meow-Wiki（知識資產層）**
- 接受：**由 MT 或 MF 提煉出的洞察**（設計原則、教訓、跨專案共通發現）、「讓未來 AI 重建同樣成果所需的最精要知識」
- 不接受：可執行程式碼、操作步驟細節、尚未驗證的想法

**雙重歸檔規則**：
- MT 的「工具開發歷史決策」同時在 MW 留一份，但兩份獨立演化
  - MT 版本：操作層，隨工具更新同步修改
  - MW 版本：知識層，專注於「從這件事學到什麼可以泛化」，由蒸餾管線定期從 MT 提煉更新
- **未來維護方向（現階段不實作）**：MT 領域文件與 MW 對應知識點做雙向整合——MW 知識點若有獨立演化，也可以反向更新 MT 的操作文件。目前先維持單向（MT → MW），等雙方內容都穩定後再評估雙向同步機制

### 決策 4：新增 Meow-Framework 作為第四個 Repo
- **結論**：建立獨立的 `Meow-Framework/` repo
- **理由**：
  - 客戶可 fork 此 repo 取得通用框架，再填入自己的內容（獨立演化）
  - Framework 需要獨立的版本控制
  - 個人的 Meow-Agent / Meow-Wiki / Meow-Tools 是 Meow-Framework 的「個人實例」
- **客戶部署模式**：客戶 fork Meow-Framework → 建立自己的 Agent/Wiki/Tools → 獨立演化

#### 決策 9：Framework CLAUDE.md 採明確繼承設計（`@` include 語法）
- **結論**：客戶的 Agent CLAUDE.md 用 Claude Code 原生的 `@path/to/file` 語法 include Framework CLAUDE.md，個人覆蓋層寫在 include 之後
- **理由**：Claude Code 原生支援此語法（AI 讀到 `@` 行時自動展開），無需自行實作 import 機制
- **Framework CLAUDE.md 應包含（通用，客戶直接繼承）**：
  - AI 開發協作行為規範（查閱再實作 / 跳過留紀錄 / 先單元測試 / 先對齊思路）
  - Karpathy 程式碼原則（先想再寫 / 最小實作 / 精準修改 / 目標驗證）
  - 安裝工具標準流程（安全性檢查 → 說明用途 → 反問需求 → 提方案比較）
  - 角色骨架結構（七個 Section 模板引用）
  - 資料傳遞格式（五種資料契約定義）
  - 文件管理規則（新建/刪除時必須更新 MENU.md）
- **個人層 CLAUDE.md 應包含（Meow 特有，不進 Framework）**：
  - 語氣 / 語言偏好（繁體中文、朋友語氣）
  - 上下文管理（cs/cc 指令行為、每 10 次壓縮規則）
  - 具體路徑引用（改為讀 REGISTRY.md 而非 hardcode）
  - Meow-Env 特有 MCP 工具清單
  - 時間：Asia/Taipei 時區
- **客戶 CLAUDE.md 骨架**：
  ```markdown
  @../Meow-Framework/CLAUDE.md   ← include 通用層
  
  # 個人覆蓋層
  - [語言 / 語氣偏好]
  - 啟動讀 @../REGISTRY.md
  - [其他個人偏好]
  ```
- **更新策略**：Framework 更新時，客戶在本機執行 `git pull`（或維護 git submodule），個人覆蓋層完全不受影響

#### 決策 5：跨系統發現機制採用 Registry 模式
- **結論**：在 Meow-Env 根目錄建立 `REGISTRY.md`，AI 每次啟動時必讀
- **理由**：MA 不應 hardcode 其他系統的內部路徑，應透過 Registry 發現能力位置
- **Registry 格式**：能力映射表（需要什麼 → 去哪個系統 → 讀哪個入口文件）

---

## 三、目標架構

### 目錄結構（目標狀態）

```
D:\Meow-Env\
├── REGISTRY.md                  ← AI 每次啟動必讀，能力映射表
│
├── Meow-Framework\              ← 通用框架（客戶 fork 的起點）
│   ├── CLAUDE.md                ← 框架層 AI 規則（通用，無個人路徑）
│   ├── governance\
│   │   ├── roles\               ← 角色骨架模板、領域文件骨架
│   │   ├── collaboration\       ← AI 協作規則（通用版）
│   │   └── prompts\             ← 通用 Prompt 模板（學習框架等）
│   └── INDEX.md                 ← 聲明「我提供什麼能力」
│
├── Meow-Agent\                  ← 個人實例（繼承 Framework）
│   ├── CLAUDE.md                ← 個人規則：讀 Registry + 個人偏好覆蓋
│   ├── .claude\
│   │   └── memory\              ← AI 跨對話記憶（只有 MA 擁有）
│   ├── context.md
│   └── INDEX.md
│
├── Meow-Wiki\                   ← 個人知識庫
│   ├── raw\
│   ├── wiki\
│   ├── context.md
│   └── INDEX.md                 ← 接受準則 + 查詢入口
│
├── Meow-Tools\                  ← 個人工具箱
│   ├── ps_tools\
│   ├── context.md
│   └── INDEX.md                 ← 接受準則 + 工具清單入口
│
└── Meow-Dev\                    ← 開發暫存區（跨裝置同步，Mac/Windows）
    ├── active\                  ← 開發進行中（依專案 / 主題分資料夾）
    ├── _done\                   ← 完成待蒸餾（觸發歸檔 Agent）
    │   └── archive\             ← 蒸餾完成的歷史快照（永久保留）
    ├── classification-logic.md  ← 分類邏輯文件（歸檔 Agent 必讀，半自動→全自動的橋樑）
    └── CLAUDE.md                ← Playground 規則（AI 在此可調用所有系統）
```

### INDEX.md 的雙重職責

各系統的 INDEX.md 同時服務兩個用途：

| 用途 | 內容 |
|------|------|
| 對外介面（MA 讀） | 這個系統提供什麼能力、查詢入口在哪 |
| 歸檔接受準則（歸檔 Agent 讀） | 我接受哪類內容 / 我不接受哪類內容 |

**範例格式：**
```markdown
# Meow-Wiki INDEX.md

## 我提供的能力
- 查詢個人知識，入口：wiki/index.md

## 歸檔接受準則
### 接受
- 概念解釋（什麼是 X、X 的原理）
- 設計思維（為什麼這樣做、背後邏輯）
- 跨專案的共通洞察

### 不接受
- 操作步驟、工具規格
- 尚未驗證的想法
- 程式碼（無論是否完成）
```

### REGISTRY.md 格式規範

Registry 由 AI 啟動時讀取，格式為 Markdown 表格，分兩個區塊：

```markdown
## 系統清單
| 系統 | 路徑 | 角色 | INDEX 位置 |
|------|------|------|-----------|
| Meow-Framework | ./Meow-Framework/ | 通用框架 | INDEX.md |
| Meow-Agent     | ./Meow-Agent/     | 指揮官   | INDEX.md |
| Meow-Wiki      | ./Meow-Wiki/      | 知識庫   | INDEX.md |
| Meow-Tools     | ./Meow-Tools/     | 工具箱   | INDEX.md |

## 能力映射
| 需求 | 系統 | 入口文件 |
|------|------|---------|
| 讀取通用 AI 治理規則 | Meow-Framework | governance/ |
| 角色 / 領域骨架模板 | Meow-Framework | governance/roles/ |
| 查詢個人知識        | Meow-Wiki      | wiki/index.md |
| 工具規格 / Playground | Meow-Tools   | workingData/MENU.md |
| 執行 PS 工具        | Meow-Tools     | ps_tools/ |
```

### 各系統 INDEX.md 的職責

每個系統在根目錄放一份 `INDEX.md`，是該系統的「對外公開介面」。
**MA 的 CLAUDE.md 只引用各系統的 INDEX.md，不深入其內部路徑。**

| 系統 | INDEX.md 應包含 |
|------|----------------|
| Meow-Framework | 框架提供哪些規則模板、路徑地圖 |
| Meow-Wiki | 知識庫有哪些主題、查詢入口 |
| Meow-Tools | 工具清單、Playground 用途說明、入口文件 |

---

## 四、現有耦合問題與解決方案

### 問題清單

| 問題 | 現況 | 解法 |
|------|------|------|
| MA CLAUDE.md hardcode MT 內部路徑（20+ 條） | MA → MT 深度耦合 | MA 改讀 REGISTRY + MT INDEX.md |
| MA CLAUDE.md hardcode MW wiki/ 路徑 | MA → MW 耦合 | MA 改讀 REGISTRY + MW INDEX.md |
| 全域治理文件住在 MT，MT 承擔全域治理職責 | MT 職責越位 | 通用部分遷移至 Meow-Framework |

### workingData/架構Wiki 的拆分計劃

| 文件 | 現在位置 | 目的地 | 分類依據 |
|------|---------|--------|---------|
| 全域角色格式與規範文件 | MT workingData | MF/governance/collaboration | 通用框架 |
| AI 開發協作行為規範（通用邏輯）| MT workingData | MF/governance/collaboration | 通用框架 |
| AI 開發協作行為規範（Meow 特有）| MT workingData | MA CLAUDE.md 個人層 | 個人設定 |
| 角色創建架構（模板）| MT workingData | MF/governance/roles | 通用框架 |
| 領域文件架構（模板）| MT workingData | MF/governance/roles | 通用框架 |
| 新領域學習引導框架 | MT workingData | MF/governance/prompts | 通用框架 |
| LLM-Wiki.md | MT workingData | MT 留著 | Meow 特有知識 |
| 角色職責與背後思路 | MT workingData | MT 留著 | Meow 設計決策 |
| Meow-Toolbox 工具箱架構總覽 | MT workingData | MT 留著 | MT 專屬 |
| PS 工具開發流程規範 | MT workingData | MT 留著 | MT 專屬 |
| 開發紀錄（Debug / 設計討論）| MT workingData | MT 留著 | Meow 歷史 |

### MA CLAUDE.md 解耦目標

**現在**：CLAUDE.md 列出 20+ 條具體路徑，AI 直接讀 MT 內部結構  
**目標**：CLAUDE.md 只包含三類內容：
1. **「啟動讀 Registry」** — `../REGISTRY.md`（相對路徑）
2. **個人行為規則** — 語氣、語言、偏好、MA 的指揮官角色設定
3. **MA 特有邏輯** — 上下文管理、每 10 次壓縮、工具呼叫規則等

---

## 五、設計模式說明（供未來 AI 理解架構意圖）

本系統運用了以下資料結構與軟體設計概念：

| 概念 | 在本系統的應用 |
|------|-------------|
| **分層架構（Layered Architecture）** | Framework 層（通用）→ 個人層（MA/MW/MT）→ Playground 層（開發中） |
| **Registry 模式** | REGISTRY.md 作為跨系統能力發現的中樞 |
| **介面隔離（Interface Segregation）** | 各系統對外只暴露 INDEX.md，MA 不直接讀內部路徑 |
| **關注點分離（Separation of Concerns）** | MA 管指揮、MW 管知識、MT 管工具、MF 管規則框架 |
| **Playground 模式** | Meow-Dev 作為獨立的開發暫存區，確認後透過蒸餾管線「畢業」 |
| **內容蒸餾管線（ETL）** | 一份原始文件 → AI 萃取 → 多份衍生品分送各系統 → 各自獨立演化 |
| **Queue + Consumer** | `_done/` 是待處理 Queue，歸檔 Agent 是 Consumer，`archive/` 是已處理紀錄 |
| **Template + Instance** | MF 是模板，MA/MW/MT 是個人實例；客戶 fork MF 後建自己的實例 |

---

## 六、實作路線圖（規劃中，尚未執行）

> 以下為規劃方向，不代表已實作。

### Phase 0：建立 Meow-Dev repo
- 建立 `D:\Meow-Env\Meow-Dev\` 並初始化 git
- 建立 `active/`、`_done/`、`_done/archive/` 目錄結構
- 將 MT 的 workingData 內容評估後遷移至 Meow-Dev
- 建立 CLAUDE.md（Playground 規則，AI 在此可調用所有系統）

### Phase A：建立 Meow-Framework repo
- 建立 `D:\Meow-Env\Meow-Framework\` 並初始化 git
- 從 workingData/架構Wiki 拆出通用部分遷移進來
- 建立 INDEX.md

### Phase B：建立 REGISTRY.md
- 在 `D:\Meow-Env\` 根目錄建立 REGISTRY.md
- 填入四個系統的能力映射

### Phase C：各系統建立 INDEX.md
- MA / MW / MT 各自建立 INDEX.md（對外介面文件）

### Phase D：解耦 MA CLAUDE.md
- 移除 hardcode 的 MT / MW 路徑
- 改為引用 REGISTRY.md + 各系統 INDEX.md
- 個人行為規則保留，具體路徑全數移除

### Phase E：workingData 清整
- 依分類表將通用文件遷移至 Meow-Framework
- 剩餘文件依其性質留在 workingData 或其他 MT 子目錄

---

## 七、客戶部署 SOP

> 本 SOP 適用於客戶 fork Meow-Framework 後，從零建立自己的 AI 協作系統。

### 前置條件（客戶自備）
- Claude Code 已安裝，API Key 已設定
- GitHub 帳號
- 本機有 git

### 命名慣例
- 建議使用 `[YourName]-` 前綴保持一致性，例如 `Alice-Env`、`Alice-Agent`
- 不強制，客戶可自由命名

### 來源標記慣例（浮水印）
- Framework `CLAUDE.md` 頂端保留來源標記區塊，請勿刪除
- 這是明文慣例，不是技術強制；要移除需主動決定
- 標記格式：
  ```markdown
  <!--
    Meow-Framework — created by 我是貓 (kulowto)
    https://github.com/kulowto/Meow-Framework
    本框架採 MIT License。衍生系統請保留此區塊作為來源標記。
  -->
  ```

---

### Phase 1：核心部署（必要）

| 步驟 | 操作 | 產出 |
|------|------|------|
| 1 | Fork `Meow-Framework` 到自己的 GitHub，clone 到本機 | `[Name]-Framework/` |
| 2 | 在本機建立 `[Name]-Env/` 根目錄，Framework 放進去 | `[Name]-Env/` |
| 3 | 建立 `[Name]-Agent/` repo，git init + push GitHub | `[Name]-Agent/` |
| 4 | 撰寫 Agent `CLAUDE.md`（第一行 include Framework，後面填個人覆蓋） | AI 行為定義完成 |
| 5 | 在 Env 根目錄建立 `REGISTRY.md`，填入 Framework + Agent 兩個系統 | 跨系統發現機制啟動 |
| 6 | 建立 `[Name]-Agent/INDEX.md`（Agent 對外介面，初期可精簡） | Agent 公開介面 |
| 7 | 啟動 Claude Code，驗證 AI 能正常讀取 REGISTRY 與 CLAUDE.md | ✅ 最小可用系統 |

**Phase 1 完成後的目錄結構**：
```
[Name]-Env/
├── REGISTRY.md
├── [Name]-Framework/       ← fork 自 Meow-Framework
└── [Name]-Agent/
    ├── CLAUDE.md           ← @../[Name]-Framework/CLAUDE.md + 個人設定
    ├── INDEX.md
    └── context.md
```

---

### Phase 2：選配擴充（按需，任意時間添加）

每個模組的標準安裝步驟一致：
1. 建立 repo，git init + push GitHub
2. 建立 `INDEX.md`（接受準則 + 查詢入口）
3. 更新 Env 根目錄的 `REGISTRY.md`，加入新系統

| 模組 | 建議添加時機 |
|------|------------|
| `[Name]-Wiki` | 開始累積個人知識資產，需要長期知識庫時 |
| `[Name]-Tools` | 開始開發自動化工具，需要工具規格管理時 |
| `[Name]-Dev` | 需要跨裝置（多台電腦）同步開發暫存區時 |

---

## 八、待討論事項

> 本輪討論所有議題已全部確認，規劃文件進入收尾狀態。

- `専案用資料(Prompt)/剪片應用/`：Premiere Pro 資料夾結構 Prompt，開發中、待驗證，暫留 workingData；Meow-Dev 建立後遷移至 `active/影片製作/`

---

*本文件由 Meow-Agent + 使用者 2026-05-19 共同建立。*
*架構設計以「可獨立運作、可擴充、可複製給客戶」為核心原則。*
