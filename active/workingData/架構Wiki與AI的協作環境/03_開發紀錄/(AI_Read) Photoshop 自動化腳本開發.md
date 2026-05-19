---
type: dev-overview
scope: Photoshop / Meow-Toolbox Module 01
version: v0.9
updated: 2026-05-14
status: ✅ Phase 1 封裝完成，tools/source_separation.py 已建立；main() 整合待處理
usage: 接手 PS 自動化開發任務時先讀此文。說明整體目標、流程架構、封裝狀態、已知技術問題。
---

# Photoshop 自動化腳本開發

## 專案背景

Python（photoshop-python-api）透過 Windows COM 控制本機 PS，自動化遊戲角色美術後製。  
**前提**：PS 必須在執行中。主腳本：`ps_tools/ps_auto.py`，工具庫：`ps_tools/ps_utils.py`

---

## 目標圖層結構

```
PSD
├── [群組] chr_effects
│   ├── chr_contourLine  ← 輪廓線稿（Multiply）
│   ├── chr_halfTone     ← 網點陰影（Multiply）
│   ├── chr_outLine      ← 白色外輪廓（Normal）
│   └── chr_outerLine    ← 黑色外輪廓線（Multiply）
└── [群組] original（🔒）
    ├── src_main         ← 去背主體（Layer Mask：主體可見）
    ├── src_background   ← 去背背景（Layer Mask：背景可見）
    └── src_img 🔒       ← 原始完整圖片（鎖定備份）
```

> 圖層命名為**暫定固定名稱**，開發穩定後改為抽象識別層（依格式或標記判斷圖層角色，不寫死字串）。

---

## 處理流程（四個 PART，各自獨立封裝）

> PART 之間有資料依賴：**PART A 的輸出是 B / C 的輸入源**。A 若失敗，B / C 必然失敗。

### PART A — 原始圖層保留（所有功能的必經入口）

| 步驟 | 操作 |
|------|------|
| 1 | 辨識唯一頂層圖層 |
| 2 | 改名為 `src_img` |

- **輸出**：`src_img`（未來鎖定備份）
- **封裝狀態**：✅ `_setup_src_img()` in `tools/source_separation.py`

---

### PART B — 去背，保留主體

| 步驟 | 操作 |
|------|------|
| 1 | 複製 `src_img` → 改名 `src_main` |
| 2 | 選取 `src_main` 為 active |
| 3 | 「選取 > 主體」（確認選取範圍出現才繼續） |
| 4 | 製作圖層遮色片（Reveal Selection） |

- **輸出**：`src_main`，Layer Mask，主體可見、背景透明
- **未來擴充**：「髮絲去背，保留主體」—步驟 3 改為開啟 Select and Mask 讓使用者手動處理髮絲，其餘相同
- **封裝狀態**：✅ `_create_src_main()` in `tools/source_separation.py`，test_part_b.py 通過

---

### PART C — 去背，保留背景

| 步驟 | 操作 |
|------|------|
| 1 | 複製 `src_img` → 改名 `src_background` |
| 2 | 選取 `src_background` 為 active |
| 3 | 「選取 > 主體」（確認選取範圍出現才繼續） |
| 4 | 反向選取 |
| 5 | 製作圖層遮色片（Reveal Selection） |

- **輸出**：`src_background`，Layer Mask，背景可見、主體透明
- **注意**：B 和 C 各自獨立執行「選取 > 主體」，不從 B 的 Mask 推導 C，確保各 PART 可獨立運作
- **封裝狀態**：✅ `_create_src_background()` in `tools/source_separation.py`，test_part_c.py 通過

---

### PART D — 歸檔與命名

依圖層規範整理群組、順序、鎖定。封裝狀態：⏸ 待規劃

---

## Phase 3：特效圖層（已完成）

| 工具 | 狀態 |
|------|------|
| `contour_line` | ✅ 完成，實機驗證通過 |
| `outline_border` | ✅ 完成，import 測試通過 |
| `halftone_shadow` | ⏸ 待封裝（Phase 1 完成後處理） |

---

## 已知技術問題（PS 27.6）⚠️ 實際驗證結果

> 詳細陷阱說明與完整程式碼：`(AI_Read) Phase1 去背 Debug 紀錄.md`

| 問題 | 症狀 | ✅ 正確解法 | 狀態 |
|------|------|------|------|
| `executeAction("Dplc")` 失效 | 不報錯，但 layers 數量不增加 | `stringIDToTypeID("duplicate") + version:5 + ID:[layerID]` 在 IIFE 內執行 | ✅ 已修正 |
| `layer.duplicate()` 毒性操作 | 靜默失敗且污染 COM 橋接，後續 doJavaScript 全部 -2147212704 | **絕對不要呼叫**，改用上方 IIFE 方案 | ✅ 已修正 |
| `doc.selection.selectAll()` 毒性操作 | 觸發 AI 選取，鎖住 COM 橋接 | **絕對不要呼叫**，全選操作在 JS IIFE 內做 | ✅ 已確認 |
| `selectSubject` 完全無法使用 | 所有呼叫方式均 -2147212704 | 改用 `autoCutout`（需搭配 `make mask` 第二步） | ✅ 已確認 |
| `autoCutout` 只建選取範圍，不建 Mask | `userMaskEnabled` 為 false | 在 autoCutout 後加 `executeAction(make, channel, revealSelection)` | ✅ 已修正 |
| Mask 建立後 doJavaScript 失敗 | `make mask` 後 PS 進入 mask 通道模式 | 退出操作放在**同一 IIFE 內**立即執行（先試 slct Chnl Cmps，fallback slct Lyr Trgt） | ✅ 已修正 |
| 從 Python executeAction 退出 mask 模式無效 | 執行不報錯，但後續 doJavaScript 仍失敗 | 退出動作必須在 IIFE 內，不從 Python 做 | ✅ 已確認 |
| `JSON.stringify` 在某些 PS 狀態下未定義 | ERR:2 JSON 未定義 | 改用字串拼接回傳資料 | ✅ 已修正 |
| `executeAction("Cpy ")` 回傳 -25920 | 「此指令目前無法使用」 | 不需要複製貼上路線，改用 duplicate 方案 | ✅ 已確認 |
| PNG IndexedColor 模式 | AI 選取需要 RGB | PART A 自動轉換（A0 步驟） | ✅ 已實作 |
| `_ensure_rgb_mode` 用 `changeMode(3)` 轉 CMYK | autoCutout -25920，文件變 CMYK | `doc.mode==2` 才是 RGB，`changeMode(2)` 轉 RGB；見陷阱 9 | ✅ 已修正 |
| `c2t("Invr")` 誤用於反向選取 | mask 方向錯（反色而非反選） | 反向選取用 `s2t("inverse")`；見陷阱 10 | ✅ 已修正 |
| mask 通道無法從純 JS IIFE 選取 | -25920 slct 不可用 | 先 Python 選圖層，再 JS `c2t("Msk ")` + `MkVs=false`；見陷阱 11 | ✅ 已確認 |
| `layer.userMaskEnabled` 回傳 false 即使 mask 正常 | mask 驗證誤判 | 改用 `executeActionGet` + `getBoolean(s2t("userMaskEnabled"))` | ✅ 已確認 |
| `Blend If` API 失敗 | -2147212704 | Multiply 模式兜底，回傳 False | ✅ 已實作 |

### 核心原則（必讀）

1. **所有涉及複製、選取、mask 的操作，一律放在 IIFE 內執行，不從 Python COM 直接呼叫**
2. **狀態恢復（退出 mask 模式、退出選取）必須在同一個 IIFE 裡完成，不能依賴後續的 Python 呼叫**
3. **不確定的 descriptor 格式，用 PS Actions 面板（Alt+F9）錄製操作後，透過「Copy As JavaScript」取得正確參數提供給 AI**
   → 詳細操作步驟：`Meow-Toolbox/Photoshop/(AI_Read) Playground 單元測試規範.md`「PS Actions 錄製 + Copy as JavaScript」section
4. **doJavaScript 一律包 IIFE + try/catch，JS 例外在 JS 內處理**

---

## 相關檔案

| 用途 | 路徑 |
|------|------|
| 主腳本 | `ps_tools/ps_auto.py` |
| 工具庫 | `ps_tools/ps_utils.py` |
| 來源圖層分離工具 | `ps_tools/tools/source_separation.py` |
| 工具文件 | `Meow-Toolbox/Photoshop/tools/(Tool) source_separation.md` |
| 單元測試 | `ps_tools/playground/` |
| Phase 1 開發進度 | `架構Wiki與AI的協作環境/(AI_Read) Phase1 去背 Debug 紀錄.md` |
| Playground 規範 | `Meow-Toolbox/Photoshop/(AI_Read) Playground 單元測試規範.md` |
