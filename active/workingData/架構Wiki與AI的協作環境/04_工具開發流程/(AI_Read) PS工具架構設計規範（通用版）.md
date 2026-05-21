---
reviewed: false
版本: v0.2
建立: 2026-05-18
最後更新: 2026-05-21
---

# PS 工具架構設計規範（通用版）

適用範圍：所有 `ps_tools/tools/` 下的工具，無論來源為影片教學、手動設計或實驗性效果
不適用：`ps_auto.py`（流程協調層）和 `ps_utils.py`（積木層），這兩個有各自的規範

> **上游對接**：本規範的開發輸入來自「工具規格草稿」（影片轉工具流程的 Phase 4 定稿輸出）。
> 上游流程規範：`(AI_Read) 影片轉工具開發流程規範.md`
> 設計理念說明：`(AI_Read) 開發理念_流程設計與資訊濾網模型.md`

---

## 零、從規格草稿到程式碼的對應關係

本規範的輸入來自 Phase 4 定稿的工具規格草稿。對應關係如下：

| 規格草稿欄位 | 對應程式碼決策 |
|------------|-------------|
| 整體評估（Level A/B/C） | 選用 Version A 或 Version B 骨架 |
| 工具類型（Type 1/2/3） | 決定主入口函式的參數（是否有 source_layer） |
| 可調參數（固定/可調） | 固定 → 寫死常數；可調 → 成為 `**params` 或具名參數 |
| 可調參數（作用說明） | 寫入 docstring 的 Args 說明 |
| 手動介入步驟（⏸） | 對應 `resume_fn` 前後的分段點 |
| 自動化可行性評估 | 逐步決定哪些用 Python COM、哪些用 JS |

**雙向維護**：若本規範的需求格式有異動，需同步更新上游的「輸出文件格式規範」。

---

## 一、工具分層架構

```
ps_auto.py          ← 流程協調層（決定執行順序、串接工具）
    ↓ 呼叫
tools/[tool].py     ← 工具層（本文件規範的範圍，每個效果一個檔案）
    ↓ 呼叫
ps_utils.py         ← 積木層（低階 API 封裝，不含業務邏輯）
    ↓ 呼叫
Photoshop COM / doJavaScript  ← PS 本體
```

工具層的職責：**把一個視覺效果從頭到尾走完**，不跨效果、不管流程順序。

---

## 二、工具類型分類

依照「輸入來源」和「輸出結構」分為三類：

### Type 1｜前置工具（Preparation Tool）
> 整理工作環境，讓後續工具能正確執行

- 輸入：原始 Document 狀態（通常只有一個頂層圖層）
- 輸出：整理好的圖層群組結構（多個命名圖層）
- 特徵：不依賴其他工具的輸出；通常是任何工作流的第一步
- 現有範例：`source_separation.py`（去背 → src_img / src_main / src_background）

### Type 2｜單源效果工具（Single-Source Effect Tool）
> 接受一個圖層，輸出一個（或多個）衍生效果圖層

- 輸入：一個指定的來源圖層（LayerSet 或 ArtLayer）
- 輸出：1-N 個新效果圖層（可指定輸出位置）
- 特徵：無副作用（不修改輸入圖層）；效果獨立可重現
- 現有範例：`contour_line.py`（輸入 chr_main → 輸出 chr_contourLine）
- 影片範例：Video 3 素描效果（輸入任意圖片圖層 → 輸出素描輪廓圖層）

### Type 3｜多源合成工具（Multi-Source Composite Tool）
> 組合多個輸入圖層，產生依賴彼此關係的合成效果

- 輸入：多個指定圖層（有明確的主體層、遮罩層、效果層等角色）
- 輸出：一個完整的效果群組（包含結構化的子圖層）
- 特徵：圖層間的相對位置和剪貼關係是效果的一部分
- 影片範例：Video 1 路面積水（需要背景圖層 + 動態生成的雲彩圖層合成）

---

## 三、自動化程度分級

每個工具在規格書中必須標明自動化等級：

| 等級 | 名稱 | 定義 | 代碼標記 |
|------|------|------|---------|
| A | 全自動 | 0 使用者介入，參數給定後一路跑完 | `# AUTO_LEVEL: A` |
| B | 半自動 | 在定義好的節點暫停，等使用者操作後繼續 | `# AUTO_LEVEL: B` |
| C | 引導式 | AI 說明步驟，使用者手動執行，AI 不操作 PS | `# AUTO_LEVEL: C` |

**判斷規則：**
- 步驟是否需要人眼判斷位置？→ 有一個就是 B 以上
- 核心效果步驟是否完全靠手感（畫筆塗抹）？→ C 或不適合開發
- 所有步驟都有確定參數可程式化？→ A

---

## 四、標準函式介面

### 主入口函式簽名（強制規範）

```python
def apply_[tool_name](
    app,                  # ps.Application 物件（必填）
    doc,                  # doc = app.activeDocument（必填）
    source_layer,         # 主要輸入圖層（ArtLayer 或 LayerSet）
    output_target=None,   # 輸出位置（None = 根層級；LayerSet = 移入指定群組）
    **params              # 工具特定可調參數
):
```

**例外：Type 1 前置工具**（前置工具在 doc 尚未整理時執行，不接受 source_layer）

```python
def apply_[tool_name](app, doc, **params):
```

### 回傳值規範

- **Level A 工具**：回傳主要輸出圖層（ArtLayer 或 LayerSet），或 tuple（多輸出時）
- **Level B 工具**：回傳 `dict`，包含：
  ```python
  {
      "completed_layers": [...],  # 已完成的圖層
      "status": "paused",         # "ok" | "paused"
      "resume": callable,         # 使用者完成手動步驟後呼叫
  }
  ```
- 任何 PS 操作失敗時：`raise RuntimeError("[tool_name] 步驟 N 失敗：{原因}")`

### Docstring 規範（4 個必填欄位）

```python
def apply_[tool_name](app, doc, source_layer, output_target=None, param_1=預設值):
    """
    [效果一句話描述]

    Args:
        app:           Photoshop Application 物件
        doc:           目標 Document 物件
        source_layer:  [說明接受什麼狀態的圖層]
        output_target: 輸出目標群組（None = 根層級）
        param_1:       [說明]（預設 X，範圍 Y～Z）

    Returns:
        [回傳類型]：[說明]

    Raises:
        RuntimeError: [何時會失敗]
    """
```

---

## 五、圖層命名規範

### 現有 Zone 系統（角色美術流程用）

`chr_effects` 群組內按優先級排列：
```
chr_contourLine  (優先級 10, Zone A)
chr_halfTone     (優先級 20, Zone A)
chr_outLine      (優先級 30, Zone B)
chr_outerLine    (優先級 40, Zone B)
```

### 新效果工具的命名規則（影片工具 / 非角色美術用途）

| 圖層用途 | 命名格式 | 範例 |
|---------|---------|------|
| 工具最終輸出圖層 | `fx_[tool]_result` | `fx_rain_result` |
| 工具輸出群組 | `fx_[tool]` | `fx_rain` |
| 內部工作暫存圖層 | `_tmp_[step]`（操作完立即刪除） | `_tmp_clouds` |
| 中間留存圖層 | `[tool]_[purpose]` | `rain_clouds`, `rain_reflection` |

**原則：**
- `fx_` 前綴 = 最終效果圖層，使用者可見
- `_tmp_` 前綴 = 暫存，程式自動清理，不出現在最終文件裡
- 純英文小寫+底線，不用中文命名（避免 COM 編碼問題）

---

## 六、JS vs Python 操作選擇規則

PS COM Python API 在 PS 27.x 有若干不穩定操作，以下決策規則已從實際踩坑整理：

| 操作類型 | 使用方式 | 原因 |
|---------|---------|------|
| 圖層選取（by ID） | `_select_layer(app, layer)` | Python COM 最穩定 |
| 複製圖層 | `_duplicate_active_layer(app, name)` | Python COM 穩定 |
| 圖層移動位置 | `layer.move(target, placement)` | Python COM 穩定 |
| 命名圖層 | `app.doJavaScript('...layer.name = ...')` | Python COM 偶爾失效 |
| 濾鏡（模糊/銳化/雲彩等） | `app.doJavaScript(...)` | Python COM 不穩定 |
| 調整圖層（色階/曲線/閾值等） | `app.doJavaScript(...)` | Python COM 不穩定 |
| 選取範圍（色彩範圍/全選等） | `app.doJavaScript(...)` | Python COM 不穩定 |
| Layer Mask 建立 | `app.doJavaScript(...)` | Python COM 不穩定 |
| 混合模式設定 | `_set_blend_mode(app, code)` | 已封裝，Python 穩定 |
| Blend If 設定 | `app.doJavaScript(...)`（best-effort） | PS 27.6 API 不穩定，失敗時用 Multiply 兜底 |
| 剪貼蒙板 | `app.doJavaScript(...)` | Python 偶爾觸發錯誤 |

**通則：只要有疑慮就用 JS，JS 失敗比 Python COM 失敗更容易偵測（有返回值）。**

---

## 七、JS 操作的錯誤偵測標準

所有 `app.doJavaScript(...)` 呼叫必須：
1. JS 代碼用 IIFE 包裹：`(function() { ... return "OK"; })()`
2. 例外情況 `return "ERR:" + e.number + "|" + e.message`
3. Python 端立即檢查返回值

```python
result = app.doJavaScript("""
(function() {
    try {
        // ... 操作 ...
        return "OK";
    } catch(e) {
        return "ERR:" + e.number + "|" + e.message;
    }
})();
""")
if result != "OK":
    raise RuntimeError(f"[{tool_name}] 步驟 N 失敗：{result}")
```

---

## 八、進度印出規範

每個 `apply_` 函式必須印出頭尾，中間每個重要步驟一行：

```python
print(f"\n[{TOOL_NAME}] 開始 [效果名稱]...")
# ... 步驟 ...
print(f"[{TOOL_NAME}] Step 1 完成（[可量化的結果]）")
print(f"[{TOOL_NAME}] Step 2 完成（[可量化的結果]）")
# ...
print(f"[{TOOL_NAME}] 完成，輸出圖層：{output_layer.name}")
```

格式：`[工具名稱]` 前綴（固定大小寫）+ 簡短動作描述 + 可量化的結果（px 數值、圖層名稱等）

---

## 九、通用 Python 工具骨架

以下是實作新工具時的起始範本，依工具類型選對應版本：

### Version A：Level A 全自動 / Type 2 單源效果工具

```python
"""
[Windows Only] [效果名稱]工具（[tool_name]）
工具文件：[對應規格書路徑]

AUTO_LEVEL: A
TOOL_TYPE:  2 (Single-Source Effect)

效果說明：[一句話]
輸入圖層：[說明接受什麼狀態]
輸出圖層：fx_[tool]_result（[說明）
平台限制：依賴 photoshop-python-api（Windows COM），Mac / Linux 無法執行
"""

from photoshop.api.enumerations import ElementPlacement
from ps_utils import (
    _select_layer,
    _duplicate_active_layer,
    # 根據需要加入其他工具函式
)

TOOL_NAME = "[tool_name]"


def apply_[tool_name](app, doc, source_layer, output_target=None,
                      param_1=預設值, param_2=預設值):
    """
    [效果一句話描述]

    Args:
        app:           Photoshop Application 物件
        doc:           目標 Document 物件
        source_layer:  [說明]
        output_target: 輸出目標群組（None = 根層級）
        param_1:       [說明]（預設 X，範圍 Y～Z）
        param_2:       [說明]（預設 X，範圍 Y～Z）

    Returns:
        ArtLayer：fx_[tool]_result 圖層

    Raises:
        RuntimeError: [何時失敗]
    """
    print(f"\n[{TOOL_NAME}] 開始 [效果名稱]...")

    # Step 1：[操作說明]
    _select_layer(app, source_layer)
    _duplicate_active_layer(app, "_tmp_work")
    work_layer = doc.activeLayer
    print(f"[{TOOL_NAME}] Step 1 完成（工作圖層 {work_layer.name} 建立）")

    # Step 2：[操作說明]（JS 操作）
    result = app.doJavaScript(f"""
    (function() {{
        try {{
            // ExtendScript 操作（注意：f-string 內部大括號需雙重轉義）
            return "OK";
        }} catch(e) {{
            return "ERR:" + e.number + "|" + e.message;
        }}
    }})();
    """)
    if result != "OK":
        raise RuntimeError(f"[{TOOL_NAME}] Step 2 失敗：{result}")
    print(f"[{TOOL_NAME}] Step 2 完成")

    # Step N：命名輸出圖層，移至目標位置
    output_layer = doc.activeLayer
    output_layer.name = "fx_[tool]_result"
    if output_target is not None:
        output_layer.move(output_target, ElementPlacement.PlaceAtEnd)

    print(f"[{TOOL_NAME}] 完成，輸出圖層：{output_layer.name}")
    return output_layer
```

### Version B：Level B 半自動工具（有手動介入步驟）

```python
"""
[Windows Only] [效果名稱]工具（[tool_name]）

AUTO_LEVEL: B
TOOL_TYPE:  [1/2/3]

手動節點：步驟 N — [說明需要使用者做什麼]
...（同上略）
"""

TOOL_NAME = "[tool_name]"


def apply_[tool_name](app, doc, source_layer, output_target=None, **params):
    """..."""
    print(f"\n[{TOOL_NAME}] 開始 [效果名稱]（半自動模式）...")

    # --- 自動化前段 ---
    # Step 1-N：全自動操作
    _run_auto_steps_before_manual(app, doc, source_layer, **params)
    print(f"\n[{TOOL_NAME}] ⚠️  手動步驟：請在 Photoshop 中完成以下操作：")
    print(f"[{TOOL_NAME}]   1. [具體操作說明]")
    print(f"[{TOOL_NAME}]   2. [具體操作說明]")
    print(f"[{TOOL_NAME}]   完成後呼叫 resume_fn() 繼續")

    # 回傳暫停狀態 + resume callable
    partial_layers = [doc.activeLayer]

    def resume_fn():
        print(f"\n[{TOOL_NAME}] 繼續執行手動步驟後段...")
        output_layer = _run_auto_steps_after_manual(app, doc, **params)
        if output_target is not None:
            output_layer.move(output_target, ElementPlacement.PlaceAtEnd)
        print(f"[{TOOL_NAME}] 完成，輸出圖層：{output_layer.name}")
        return output_layer

    return {
        "completed_layers": partial_layers,
        "status": "paused",
        "resume": resume_fn,
    }


def _run_auto_steps_before_manual(app, doc, source_layer, **params):
    """手動步驟前的自動化段落"""
    pass  # 實作


def _run_auto_steps_after_manual(app, doc, **params):
    """手動步驟後的自動化段落"""
    pass  # 實作
```

---

## 十、工具整合至 ps_auto.py 的規範

新工具完成後，要加入 `ps_auto.py` 的方式：

1. **新增 import**（依字母順序）：
   ```python
   from tools.[tool_name] import apply_[tool_name]
   ```

2. **新增可調參數**（集中在頂部的 `# ── 可調參數 ──` 區塊）：
   ```python
   [TOOL_NAME]_PARAM_1 = 預設值   # [說明]
   ```

3. **在對應 Phase 函式中呼叫**：
   ```python
   result = apply_[tool_name](
       app, doc, source_layer,
       output_target=effects_group,
       param_1=TOOL_NAME_PARAM_1,
   )
   ```

4. **工具不應在 ps_auto.py 裡再做圖層整理**：輸出位置透過 `output_target` 參數傳入，由工具自己 `move`。

---

## 十一、Playground 測試規範

每個新工具在 `ps_tools/playground/test_[tool_name].py` 有獨立測試腳本。

### 測試腳本最小結構

```python
"""
[tool_name] 工具 Playground 測試
前提：Photoshop 已開啟，目標圖片已載入為 activeDocument
"""
import sys
sys.path.insert(0, "..") # 讓 ps_utils 可被 import
from ps_utils import get_app_and_doc
from tools.[tool_name] import apply_[tool_name]

app, doc = get_app_and_doc()
source_layer = doc.activeLayer  # 或依測試需要指定圖層

# 測試 1：預設參數
result = apply_[tool_name](app, doc, source_layer)
print(f"[Test 1] 輸出圖層：{result.name} ✓")

# 測試 2：邊界參數
result2 = apply_[tool_name](app, doc, source_layer, param_1=最小值)
print(f"[Test 2] 邊界參數：{result2.name} ✓")
```

### 測試的三個必過關卡

1. **功能正確**：視覺效果符合規格書描述
2. **冪等性**：連續執行兩次不會報錯（第二次在已有效果的圖層上執行）
3. **參數邊界**：最小值、最大值、預設值都能正常執行

---

## 附錄：現有工具一覽

| 工具名稱 | 類型 | 等級 | 輸入 | 輸出 | 檔案 |
|---------|------|------|------|------|------|
| source_separation | Type 1 前置 | A 全自動 | 原始 PNG doc | src_img / src_main / src_background | `tools/source_separation.py` |
| contour_line | Type 2 單源 | A 全自動 | chr_main | chr_contourLine | `tools/contour_line.py` |
| outline_border | Type 2 單源 | A 全自動 | 任意圖層 | chr_outLine / chr_outerLine | `tools/outline_border.py` |
| rain_puddle（待開發） | Type 3 多源合成 | B 半自動 | 街景照片圖層 | fx_rain（效果群組） | — |
| sketch_effect（待開發） | Type 2 單源 | B 半自動 | 任意圖層 | fx_sketch_result | — |
