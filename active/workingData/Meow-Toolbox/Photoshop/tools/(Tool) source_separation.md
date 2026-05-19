---
type: tool
tool_id: source_separation
scope: Photoshop
version: v1.0
created: 2026-05-14
blueprint: N/A（來源圖層，不參與 chr_effects Zone 排序）
script: D:\Meow-Env\Meow-agent\ps_tools\tools\source_separation.py
---

# source_separation：來源圖層分離

---

## 描述

將原始 PNG 分離為三個帶 Layer Mask 的來源圖層（`src_img` / `src_main` / `src_background`），建立後製流程的圖層基礎結構。

此工具是所有角色美術後製效果的**必要前置步驟**——effect 工具（contour_line、outline_border 等）需要 `src_main` 的 Layer Mask 作為選取來源，因此在任何效果工具執行前，必須先執行此工具完成分層。

**適合調用的情境：**
- 開始處理一張新的角色圖，需要初始化 PSD 圖層結構
- 需要取得「去背主體」或「去背背景」各自獨立的遮色片
- 為後續的 chr_effects 特效工具（contour_line、halftone_shadow、outline_border）建立所需的圖層基礎

---

## 前置條件

調用此工具前，文件必須滿足以下條件：

- [ ] Photoshop 已開啟且執行中
- [ ] `activeDocument` 為原始 PNG，頂層只有 1 個圖層（未處理狀態）
- [ ] 文件為 RGB 或 IndexedColor 模式（非 RGB 時工具會自動轉換）

---

## 輸入 / 輸出定義

### 輸入

| 參數名稱 | 類型 | 必填 | 說明 |
|---------|------|------|------|
| `app` | PS Application | ✅ | Photoshop 應用程式物件 |
| `doc` | PS Document | ✅ | 目標文件物件 |

### 輸出

執行完畢後，文件頂層建立三個圖層（堆疊順序由上到下）：

| 圖層名稱 | Layer Mask | 說明 |
|---------|-----------|------|
| `src_background` | ✅（背景可見，主體透明） | 去背背景，供背景獨立編輯或後置使用 |
| `src_main` | ✅（主體可見，背景透明） | 去背主體，所有效果工具的來源圖層 |
| `src_img` | 無 | 原始完整圖片，供 Phase 2 鎖定後備份 |

回傳值：`tuple(src_img_id, src_main_id, src_background_id)`，三個圖層的整數 id

---

## 步驟

1. 確認文件只有 1 個頂層圖層（`_validate_fresh_document`）
2. 若文件非 RGB 模式，自動轉換（`_ensure_rgb_mode`）；IndexedColor 為 PNG 常見格式，會自動處理
3. 將唯一頂層圖層改名為 `src_img`
4. 複製 `src_img`，命名為 `src_main`（`_duplicate_active_layer`）
5. 對 `src_main` 執行 autoCutout，建立主體選取範圍，再建立 Layer Mask（主體可見，`invert_mask=False`）
6. 切回 `src_img` 為 activeLayer，確保下一步複製來源正確
7. 複製 `src_img`，命名為 `src_background`（`_duplicate_active_layer`）
8. 對 `src_background` 執行 autoCutout，反向選取（背景範圍），再建立 Layer Mask（背景可見，`invert_mask=True`）

---

## 工具（函式清單）

| 函式名稱 | 所在檔案 | 用途 |
|---------|---------|------|
| `apply_source_separation()` | `ps_tools/tools/source_separation.py` | 主入口，依序執行三個圖層建立步驟 |
| `_setup_src_img()` | `ps_tools/tools/source_separation.py` | 確認文件、轉換 RGB、命名 src_img |
| `_create_src_main()` | `ps_tools/tools/source_separation.py` | 建立 src_main（主體可見 Layer Mask） |
| `_create_src_background()` | `ps_tools/tools/source_separation.py` | 建立 src_background（背景可見 Layer Mask） |
| `_validate_fresh_document()` | `ps_tools/ps_utils.py` | 確認文件狀態（頂層只有 1 個圖層） |
| `_ensure_rgb_mode()` | `ps_tools/ps_utils.py` | 確認並轉換 RGB 模式（2=RGB，非 2 自動轉換） |
| `_get_active_layer_id()` | `ps_tools/ps_utils.py` | 透過 JS 取得 activeLayer 的可靠 id |
| `_duplicate_active_layer()` | `ps_tools/ps_utils.py` | 複製圖層並命名（PS 27.6 安全版，帶 version:5） |
| `_auto_cutout()` | `ps_tools/ps_utils.py` | autoCutout 建立選取範圍 → Layer Mask（支援反向） |
| `_select_layer_by_id()` | `ps_tools/ps_utils.py` | 選取指定 id 的圖層（by id，避免 COM proxy 問題） |

---

## 圖層區域與優先級

此工具建立的是**來源圖層**，最終移入 `original` 群組（Phase 2 處理），不在 `chr_effects` 內，不參與 Zone 排序。

| 欄位 | 值 |
|------|---|
| `layer_zone` | N/A（original 群組，非 chr_effects 效果圖層） |
| `layer_priority` | N/A |

---

## 參數

目前無可調參數（工具為全自動模式）。

| 參數名稱 | 預設值 | 說明 |
|---------|--------|------|
| — | — | 未來可擴充 `hair_mask=True` 模式，開啟 Select and Mask 手動處理髮絲去背 |

---

## 副檔（條件性參考）

| 文件 | 觸發條件 | 說明 |
|------|---------|------|
| `(AI_Read) Phase1 去背 Debug 紀錄.md` | 修改任何步驟，或遇到 PS API 回傳錯誤碼時 | 記錄 PS 27.6 的已知陷阱與每個問題的正確修法 |
| `(AI_Read) Photoshop 自動化腳本開發.md` | 需要了解整體架構或 Phase 1 背景時 | 說明分層流程的設計動機與整體模組結構 |

---

## 驗證標準

執行完畢後，確認以下條件全部通過：

- [ ] 文件頂層有 3 個圖層：`src_background`、`src_main`、`src_img`（由上到下）
- [ ] `src_main` 有 Layer Mask，主體中心像素偏白（`brightness > 128`）
- [ ] `src_background` 有 Layer Mask，主體中心像素偏黑（`brightness < 128`）
- [ ] `src_img` 無 Layer Mask，為原始像素備份
- [ ] 對應 Playground：`test_part_a.py`、`test_part_b.py`、`test_part_c.py` 全部通過

---

## 常見錯誤記錄

| 錯誤描述 | 原因 | 解法 |
|---------|------|------|
| `autoCutout` 失敗（-25920「此指令目前無法使用」） | 文件為 CMYK 模式（`doc.mode==3`，PS COM 中 2=RGB、3=CMYK） | `_ensure_rgb_mode` 已自動處理；若仍失敗，確認 `doc.mode==2` |
| `_duplicate_active_layer` 後，後續 `doJavaScript` 全部 -2147212704 | 使用了 `layer.duplicate()`（PS 27.6 毒性操作） | 絕對只用 `_duplicate_active_layer()`；禁止呼叫 `layer.duplicate()` |
| `src_background` Mask 方向錯誤（主體可見，背景反而透明） | 反色（`c2t("Invr")`）誤用於反向選取 | `_auto_cutout(invert_mask=True)` 內部使用 `s2t("inverse")`（Select > Inverse），不是 `c2t("Invr")`（Image > Invert，反色） |
| Mask 建立後 `doJavaScript` 全部失敗 | `make mask` 後 PS 停在 Mask 通道模式，封鎖後續呼叫 | 退出通道動作必須在同一 IIFE 內完成；`_auto_cutout` 已處理，不需另外操作 |
| `_validate_fresh_document` 拋出 RuntimeError | 文件頂層不止 1 個圖層，可能已被腳本處理過 | 在 Photoshop 重新開啟原始 PNG，確認文件未被處理過 |

---

## 告知訊息（使用者說明）

### 使用前說明

此工具為全自動流程。執行前只需確認 Photoshop 已開啟，且目標圖片以**原始 PNG**（單一頂層圖層）的狀態載入。

工具會自動辨識角色主體（PS 內建 AI 去背），建立兩個方向相反的去背遮色片，以及一份原始備份圖層。

> **注意：** 若圖片含有複雜髮絲、半透明披風或複雜邊緣，AI 自動去背可能有邊緣不精確的情況。此時需手動在 Photoshop 用 Select and Mask 補正。未來 `hair_mask` 模式開放後，可改為半自動流程。

### 參數選擇提示

本工具目前為全自動，無需選擇參數。
