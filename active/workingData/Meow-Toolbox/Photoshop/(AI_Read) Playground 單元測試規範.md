---
type: protocol
scope: Photoshop / PS 工具開發
version: v1.0
created: 2026-05-14
usage: 開發或 debug 任何 PS 工具函式時，必須先在 Playground 跑單元測試，確認通過後再整合進主流程。
---

# (AI_Read) Playground 單元測試規範

> 本文件記錄 PS 工具開發的 Playground 測試格式與執行規範。
> 此格式來自實際 debug 過程的有效案例，讓未來的 AI 有標準可依循。

---

## 為什麼需要 Playground 測試

PS 自動化的 API 在 PS 27.6 極不穩定：
- 同一個操作，Python 直呼 vs JavaScript 呼叫，行為可能完全不同
- COM proxy 物件的屬性（如 `.id`）可能不可靠
- 操作完成後 PS 的內部狀態（如 Mask 通道 active）會影響後續所有操作

沒有單元測試，多個步驟串在一起出錯時，很難確定是哪一個環節的問題，反覆除錯浪費大量時間。

**每個新函式或不確定是否可行的操作，都必須先在 Playground 獨立驗證。**

---

## 測試檔案位置與命名

```
ps_tools/
└── playground/
    ├── test_phase1_funcs.py   ← Phase 1 去背流程測試（實際案例）
    ├── test_[功能名稱].py      ← 命名格式
    └── ...
```

- 一個測試檔案對應一個功能或一組相關函式
- 命名格式：`test_[功能名稱].py`
- 從 `ps_tools/` 目錄執行：`python playground/test_xxx.py`

---

## 測試腳本結構

### 必要元素

```python
"""
檔案頂部 docstring：
  - 說明測試目標
  - 執行前提（PS 開啟、文件狀態等）
  - 測試步驟清單
"""

# 1. sys.path 設定（確保可以 import ps_utils）
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 2. import 被測試的函式（從 ps_utils 或 tools/xxx.py）
from ps_utils import _function_to_test

# 3. 連線 PS
app = ps.Application()
doc = app.activeDocument

# 4. 逐步測試，每步驟都有：操作 + 驗證 + 輸出
```

### `check()` 工具函式（每個測試腳本都要包含）

```python
def check(label, passed, detail=""):
    status = "✓ 通過" if passed else "✗ 失敗"
    msg = f"  [{status}] {label}"
    if detail:
        msg += f"\n         → {detail}"
    print(msg)
    return passed
```

---

## 步驟格式

每個測試步驟固定格式：

```python
print("─── [步驟代號] 步驟說明 ──────")
try:
    # 1. 執行操作
    some_function(app)
    results["X1"] = check("操作完成（無例外）", True)
except Exception as e:
    results["X1"] = check("操作完成（無例外）", False, str(e))
print()

print("─── [步驟代號] 驗證結果 ───────")
try:
    # 2. 驗證 PS 狀態（透過 doJavaScript 或 Python API）
    info = app.doJavaScript("JSON.stringify({ ... })")
    data = json.loads(info)
    results["X2"] = check("預期條件", data["key"] == expected, str(data))
except Exception as e:
    results["X2"] = check("預期條件", False, str(e))
print()
```

**步驟代號規則**：
- `S` 開頭：Setup（前置確認）
- `A` 開頭：第一個主要操作的子步驟
- `B` 開頭：第二個主要操作的子步驟
- 以此類推

**將「執行」和「驗證」分開為獨立步驟**，這樣可以區分：
- 函式本身執行失敗（有例外）
- 函式執行成功但結果不對（驗證失敗）

---

## 驗證方式

### 優先用 JavaScript 驗證（不信任 Python COM proxy）

```python
# ✅ 推薦：用 doJavaScript 取得 PS 狀態
info = app.doJavaScript("""
JSON.stringify({
    name: app.activeDocument.activeLayer.name,
    id: app.activeDocument.activeLayer.id,
    userMaskEnabled: app.activeDocument.activeLayer.userMaskEnabled
});
""")
data = json.loads(info)
```

```python
# ⚠️ 謹慎：Python COM proxy 的屬性可能不可靠
layer.id        # 可能是舊值，使用 _get_active_layer_id(app) 替代
layer.name      # 相對可靠
```

### 已知驗證技巧

| 驗證項目 | 推薦做法 |
|---------|---------|
| activeLayer 名稱 | `app.doJavaScript("app.activeDocument.activeLayer.name")` |
| activeLayer id | `_get_active_layer_id(app)` → `int(app.doJavaScript("app.activeDocument.activeLayer.id"))` |
| Layer Mask 是否存在 | `doJavaScript` 取 `layer.userMaskEnabled` |
| 選取範圍 bounds | `doJavaScript` 取 `selection.bounds`，用 try/catch 包住 |

---

## PS Actions 錄製 + Copy as JavaScript：取得正確 Descriptor 的方法

> 當 Python 呼叫某操作失敗（-2147212704 / -25920 等），但手動在 PS 操作正常時，
> 最快的方式是讓 PS 自己告訴你正確的 ActionDescriptor 格式。

### 什麼時候需要用這個方法

- 不確定某個操作的 `charID` / `stringID` 或 descriptor 結構
- Python / JS 執行失敗，但手動 PS 操作完全正常
- PS 版本更新後 API 行為改變，舊代碼失效
- 需要新功能但找不到文件（例如 PS 27.x 新增的操作）

---

### 前置：開啟開發者模式（只需做一次）

**Copy as JavaScript** 必須在開發者模式啟用後才會出現在 Actions 面板選單。

| 步驟 | 操作 |
|------|------|
| 1 | 開啟 PS → 選單列 `Edit > Preferences > Plug-ins`（Windows） |
| 2 | 勾選 `Enable Developer Mode`（可能標示為 Generator 或 Developer Mode） |
| 3 | 重啟 PS |
| 驗證 | 開啟 Actions 面板 → 點右上角 `≡` 選單 → 確認有「Copy as JavaScript」選項出現 |

---

### 操作流程：錄製並取得 JavaScript

**Step 1 — 開啟 Actions 面板**

```
Alt + F9（Windows）
或：Window > Actions
```

**Step 2 — 建立新 Action**

1. 點擊面板底部的資料夾圖示 → 建立新的 Action Set（例如命名為 `Debug`）
2. 點擊 `+` 圖示 → 建立新的 Action，命名（例如 `test_operation`）
3. 此時 PS 進入錄製模式（面板底部的錄製按鈕變紅）

**Step 3 — 執行目標操作**

在 PS 中手動完成你想複製的操作（例如：建立 Layer Mask、duplicate 圖層、套用濾鏡）。
操作會逐一記錄在 Action 的步驟清單裡。

**Step 4 — 停止錄製**

點擊面板底部的方形「停止」按鈕。

**Step 5 — 複製為 JavaScript**

1. 在 Actions 面板中選取剛才錄製的 Action（整個 Action 或單一步驟皆可）
2. 點擊面板右上角 `≡` 選單
3. 選擇 **「Copy as JavaScript」**
4. 把複製的程式碼貼給 AI

---

### 提供給 AI 的格式

把以下資訊一起提供，方便 AI 快速定位問題：

```
【操作說明】
我想做的操作：（例如：對 src_main 圖層建立以主體為範圍的 Layer Mask）
手動可以成功：是 / 否
程式碼錯誤訊息：（如有）

【Copy as JavaScript 輸出】
（貼上從 PS Actions 複製的 JS 程式碼）
```

---

### 注意事項

| 項目 | 說明 |
|------|------|
| 不是所有操作都能錄製 | 手動拖曳圖層順序、某些 UI 操作不會被記錄；改用選單路徑操作才能被錄製 |
| 輸出格式是 ExtendScript | Copy as JavaScript 產生的是 ExtendScript 格式（PS 內建 JS），不是直接可用的 Python 程式碼，需要 AI 轉換 |
| 每次錄製都是新鮮狀態 | 重新開啟 PNG、確認文件狀態一致，避免 PS 殘留狀態干擾錄製結果 |
| 只錄一個步驟更精確 | 如果要確認單一操作的 descriptor，每次只錄製一步，減少干擾 |

---

## 已知 PS 27.6 陷阱

接手 AI 開始 debug 前必讀這個清單：

| 陷阱 | 症狀 | 處理方式 |
|------|------|---------|
| **-2147212704 根本原因** | 手動正常，程式失敗 → 操作前未取得所需資料（id、選取範圍、active 狀態） | 每步驟確認資料已取得；不假設 PS 狀態自動延續 |
| Python COM proxy `.id` 不可靠 | `layer.duplicate()` 後 `.id` 仍是原始圖層的值 | 用 JS 一步完成 duplicate + rename + 回傳 id（`_duplicate_active_layer`） |
| autoCutout 後 mask 模式封鎖 `doJavaScript` | 後續所有 `doJavaScript` 回傳 `-2147212704` | autoCutout 後改用 Python `executeAction` 切回 composite channel |
| `selectSubject` 失敗（待確認） | 舊代碼 `-2147212704`，手動正常 | 懷疑是資料未取得問題；重構後重新 Playground 測試 |
| 選取範圍空但 `_add_mask_from_selection` 不拋例外 | 建立的是 Reveal All 空白 Mask | 先驗證選取範圍有效（bounds width > 0）再執行 Mask 建立 |

---

## 結果總覽格式

每個測試腳本結尾必須包含：

```python
print("=" * 55)
print("  測試結果總覽")
print("=" * 55)
for key, passed in results.items():
    print(f"  [{key}] {'✓' if passed else '✗'}")

all_passed = all(results.values())
if all_passed:
    print("\n✅ 全部通過——可整合進主流程。")
else:
    failed = [k for k, v in results.items() if not v]
    print(f"\n❌ 失敗步驟：{failed}")
    print("   請把上方的輸出貼給 AI 進行 debug。")
```

這樣每次跑完，只要把**完整輸出**貼給 AI，就能精確定位問題。

---

## 從 Playground 整合進主流程的條件

- 所有步驟 `✓ 通過`
- 在 PS 中視覺確認結果符合預期（不只靠程式驗證）
- 通過後才將邏輯移入 `ps_auto.py` 或對應的 `tools/xxx.py`

---

## 實際案例：Phase 1 PART A / B / C

Phase 1 拆成三個獨立測試腳本，每個 PART 各自通過後再整合：

| 腳本 | 測試對象 | 狀態 |
|------|---------|------|
| `test_part_a.py` | 辨識圖層 + 改名 src_img（對應 `_setup_src_img`） | ✅ 通過 |
| `test_part_b.py` | duplicate + autoCutout + Layer Mask（src_main，對應 `_create_src_main`） | ✅ 通過 |
| `test_part_c.py` | duplicate + autoCutout + 反向選取 + Layer Mask（src_background，對應 `_create_src_background`） | ✅ 通過（含 C5 mask 方向驗證，brightness=0）|

開發進度與技術問題詳見：`架構Wiki與AI的協作環境/(AI_Read) Phase1 去背 Debug 紀錄.md`
