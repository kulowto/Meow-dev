---
文件類型: menu  版本: v1.3  建立: 2026-05-19  最後更新: 2026-05-26
---

# workingData 頂層索引

> AI 進入 workingData 時先讀此文件，確認全貌後再前往子目錄。

---

## 目錄結構一覽

| 目錄 | 性質 | 說明 |
|------|------|------|
| `架構Wiki與AI的協作環境/` | 核心架構文件 | AI 協作框架、角色定義、開發紀錄；詳見子目錄 `MENU.md` |
| `Meow-Toolbox/` | 工具規格文件 | PS 工具設計文件（PSD 藍圖、各工具 spec、骨架模板） |
| `design-systems/` | 設計系統 | 品牌設計規範，依品牌分子目錄；詳見 `design-systems/README.md` |
| `思維框架/` | 個人思維框架 | 金字塔理論、問好問題、驗證資料、AI 協作思維；入口：`思維框架整合索引.md` |
| `專案/BD2/` | 專案材料 | BD2 遊戲相關的影片腳本與爬蟲工具 |
| `外部工具研究/` | 外部工具調查 | 安裝前的安全性審查與功能評估報告 |

---

## 各目錄說明

### 架構Wiki與AI的協作環境/
MD（Meow-Dev）暫存的 AI 協作文件：角色定義、架構設計思路、開發紀錄、工具開發流程規範。
通用治理文件已遷移至 `Meow-Framework/governance/`，透過 `CLAUDE.md @include` 自動繼承。
→ 詳見 `架構Wiki與AI的協作環境/MENU.md`

### Meow-Toolbox/
工具設計規格文件區，依工具類型分子目錄。

| 路徑 | 內容 |
|------|------|
| `Photoshop/` | PSD Master Blueprint、各工具 spec（contour_line、outline_border、source_separation） |
| `Photoshop/tools/` | 各工具的 `(Tool)` 規格文件 |
| `Xmind/` | 心智圖輔助工具組（工具一~五）；詳見 `(AI_Read) Xmind工具架構說明.md` 與 `(AI_Read) Xmind整理工具使用規範.md` |
| `Xmind/schema/` | 格式參考：xmind / canvas / md 三種格式規格 + AI 整理 Prompt |
| `_schema/` | 新工具文件骨架模板 |

### design-systems/
設計系統儲存庫，目前包含 `personal-brand/`。
→ 詳見 `design-systems/README.md`

### 思維框架/
個人核心思維框架，供 inquiry_model 和 AI 工具讀取參考。
已同步備份至 Meow-Wiki `wiki/concepts/`（ref-pyramid-principle-framework 等 7 份，reviewed: false 待人工確認）。

| 文件 | 使用情境 | 類型 |
|------|---------|------|
| 思維框架整合索引 | 進入此目錄時先讀 | AI讀 |
| 金字塔理論與分而治之框架 | 問題拆解、結構化思考 | AI讀 |
| 如何問好問題 | 討論前、喬哈理窗應用 | AI讀 |
| 高品質驗證資料篩選準則 | 評估論點依據 | AI讀 |
| 與AI工具協作共長思維 | 日常 AI 互動策略 | AI讀 |
| GROW_Reality前置詢問 | 詢問前確認現況/上下文（可選） | AI讀 |
| 蘇格拉底視角與後果提問 | 開放性問題的視野擴展（可選） | AI讀 |
| Powerful_Questions原則 | 一次一問 + 問題追蹤器原則 | AI讀 |
| Clean_Language潔淨語言 | 使用者限定範圍時的單線程模式 | AI讀 |

### 外部工具研究/
安裝前調查報告，包含安全性審查、功能評估與使用建議。

| 文件 | 使用情境 | 類型 |
|------|---------|------|
| `ConardLi_garden-skills 調查報告.md` | 考慮安裝 garden-skills 前的全面評估 | AI讀 |
| `ConardLi_garden-skills_深度拆解.md` | garden-skills 各 Skill 工程細節，含 reference 文件展開版 | AI讀 |

### 專案/BD2/
BD2（Blue Archive II）遊戲相關專案材料。

| 子目錄 | 內容 |
|--------|------|
| `PVP影片腳本/` | PVP 系列教學影片腳本（A / B / C / X 系列，共 13 個 MD 文件） |
| `爬蟲工具/` | BD2 圖片素材爬蟲：2DLive 素材提取 + 一般角色圖片下載 |

