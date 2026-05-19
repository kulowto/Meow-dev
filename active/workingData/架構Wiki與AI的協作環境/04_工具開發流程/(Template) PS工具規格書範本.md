---
reviewed: false
版本: v0.1
建立: 2026-05-18
---

# PS 工具規格書範本

使用方法：複製整份文件 → 依影片填入 → 走 Phase 3 → Phase 4 → Phase 5

範例參考：
- Video 1（路面積水）：`(AI_Read) 工具規格草稿_Video1_路面积水效果.md`
- Video 3（素描效果）：`(AI_Read) 工具規格草稿_Video3_素描效果.md`

---

## 一、工具規格草稿格式（Phase 3 輸出）

```markdown
---
reviewed: false
版本: v0.1
建立: YYYY-MM-DD
Phase3狀態: 完成（待使用者 Phase 4 確認）
---

# 工具規格草稿：PS [效果名稱]

## 來源

| 項目 | 內容 |
|------|------|
| 影片 URL | [YouTube URL] |
| 影片標題 | [標題] |
| 軟體 | Photoshop |
| 時長 | 約 X 秒 |
| 逐字稿段數 | X 段 |
| 逐字稿檔案 | [.txt 路徑] |

---

## 效果描述

[一句話描述效果] + [適用情境]

---

## Phase 3：語音辨識修正

| 原始辨識 | 修正為 | 備註 |
|---------|--------|------|
| [錯誤] | [修正] | [說明] |

---

## 操作步驟（結構化）

步驟 1：[操作動詞] [目標] [參數或方向（若有）]
原文：[對應原始辨識文字]

步驟 2：...

---

## 可調參數

| 參數名稱 | 建議預設值 | 可調範圍 | 說明 |
|---------|-----------|---------|------|

---

## 效果原理

[技術說明，例如「減藍 = 加黃」、各步驟背後的 PS 原理]

---

## 自動化可行性評估

| 步驟 | 可自動化 | 說明 |
|------|---------|------|
| X [步驟名] | ✅ 全自動 / ⚠️ 半自動 / ❌ 手動 | [說明] |

整體評估：✅ 高度可自動化 / ⚠️ 半自動化 / ❌ 不適合自動化

---

## 開發狀態

- [ ] Phase 3 完成（步驟草稿 + 語音修正）
- [ ] Phase 4 完成（使用者確認定稿）
- [ ] Phase 5 完成（實作 + 實機測試）
```

---

## 二、Python 工具函式骨架（Phase 5 用）

參照 `ps_tools/tools/contour_line.py` 的結構，每個效果工具都是一個 `apply_XXX()` 函式，由 `ps_auto.py` 統一呼叫。

```python
"""
[Windows Only] [效果名稱]工具（[tool_name]）
工具文件：[對應規格書路徑]

效果說明：[一句話]
前置條件：[輸入圖層說明]
平台限制：依賴 photoshop-python-api（Windows COM），Mac / Linux 無法執行
"""

from photoshop.api.enumerations import ElementPlacement
from ps_utils import (
    _select_layer,
    _duplicate_active_layer,
    _levels,
    _fill_color,
    _delete_selection,
    # 根據需要添加其他工具函式
)


def apply_[tool_name](app, doc, source_layer,
                      param_1=預設值, param_2=預設值):
    """
    [效果名稱]主入口。
    [一句話說明效果]

    Args:
        app:          Photoshop Application 物件
        doc:          目標 Document 物件
        source_layer: 來源圖層 reference（通常是原始圖片圖層）
        param_1:      [參數說明]（預設 X）
        param_2:      [參數說明]（預設 X）
    """
    print(f"\n[[tool_name]] 開始執行[效果名稱]...")

    # Step 1：[步驟說明]
    # 對應影片步驟 1
    _select_layer(app, source_layer)
    # ... PS 操作 ...
    print("[[tool_name]] Step 1 完成")

    # Step 2：[步驟說明]
    # 對應影片步驟 2-3（合併）
    result = app.doJavaScript("""
    (function() {
        // ExtendScript 操作
        return "OK";
    })();
    """)
    if result != "OK":
        raise RuntimeError(f"[[tool_name]] Step 2 失敗：{result}")
    print("[[tool_name]] Step 2 完成")

    # ... 依此類推 ...

    print("[[tool_name]] [效果名稱]完成")
```

---

## 三、常用 PS 操作 → Python API 對照表

這些操作在各效果工具中頻繁出現，皆已封裝在 `ps_utils.py` 或可用 `app.doJavaScript` 觸發：

### 已封裝（直接呼叫 ps_utils 函式）

| PS 操作 | 函式 | 備註 |
|---------|------|------|
| 選取圖層 | `_select_layer(app, layer)` | 用 ID 選取，比直接賦值可靠 |
| 複製圖層 | `_duplicate_active_layer(app, "新名稱")` | 先 `_select_layer` 再複製 |
| 填充顏色 | `_fill_color(app, r, g, b)` | 填滿目前選取範圍或整層 |
| Delete 刪除選取 | `_delete_selection(app)` | 等同 Delete 鍵 |
| 色階調整 | `_levels(app, black_in, white_in, gamma)` | 常用參數：black_in=150, white_in=240 |
| 去色 | `_desaturate(app)` | 轉灰階但保留 RGB 模式 |
| 反色 | `_invert(app)` | Image > Adjustments > Invert |
| 設混合模式 | `_set_blend_mode(app, "Mltp")` | Mltp=Multiply, CDdg=Color Dodge, Nrml=Normal |
| 最小值濾鏡 | `_minimum_filter(app, radius=3)` | 線稿提取技法用 |
| 向下合併 | `_merge_down(app)` | 合併當前圖層到下方 |
| 清除圖層像素 | `_clear_layer_pixels(app, doc)` | 全選並清除（JS 實現） |

### 常用 JS 操作（doJavaScript 觸發）

```javascript
// 分層雲彩濾鏡
executeAction(charIDToTypeID("Dfrn"), new ActionDescriptor(), DialogModes.NO);

// 動感模糊（角度 90°，距離 30px）
var desc = new ActionDescriptor();
desc.putInteger(charIDToTypeID("Angl"), 90);
desc.putUnitDouble(charIDToTypeID("Dist"), charIDToTypeID("#Pxl"), 30);
executeAction(charIDToTypeID("MtnB"), desc, DialogModes.NO);

// 色彩範圍選取（選白色）
var desc = new ActionDescriptor();
desc.putInteger(charIDToTypeID("Fzns"), 40);  // Fuzziness
desc.putEnumerated(charIDToTypeID("Slct"), charIDToTypeID("Clrr"), charIDToTypeID("Wht "));
executeAction(charIDToTypeID("ClrR"), desc, DialogModes.NO);

// 建立 Layer Mask（以選取範圍顯示）
var desc = new ActionDescriptor();
var ref = new ActionReference();
ref.putEnumerated(charIDToTypeID("Chnl"), charIDToTypeID("Chnl"), charIDToTypeID("Msk "));
desc.putReference(charIDToTypeID("null"), ref);
desc.putClass(charIDToTypeID("Usng"), charIDToTypeID("RvlS"));  // Reveal Selection
executeAction(charIDToTypeID("Mk  "), desc, DialogModes.NO);

// 垂直翻轉（自由變換）
var desc = new ActionDescriptor();
desc.putEnumerated(charIDToTypeID("FTrs"), charIDToTypeID("Ornt"), charIDToTypeID("Vrtc"));
executeAction(charIDToTypeID("FlpD"), desc, DialogModes.NO);

// 剪貼蒙板（與下方圖層建立剪貼遮罩）
executeAction(charIDToTypeID("GrpL"), new ActionDescriptor(), DialogModes.NO);

// USM 銳化（強度 100, 半徑 1.5, 閾值 0）
var desc = new ActionDescriptor();
desc.putUnitDouble(charIDToTypeID("Amnt"), charIDToTypeID("#Prc"), 100.0);
desc.putUnitDouble(charIDToTypeID("Rds "), charIDToTypeID("#Pxl"), 1.5);
desc.putInteger(charIDToTypeID("Thsh"), 0);
executeAction(charIDToTypeID("UnsM"), desc, DialogModes.NO);
```

---

## 四、語音辨識常見錯誤累積表

（隨使用持續累積，每次 Phase 3 分析後更新此表）

| 辨識錯誤 | 正確意思 | 出現影片 |
|---------|---------|---------|
| 素质一层 | 複製一層 | Video 1 |
| 一丢丢雨画 | 一點羽化（Feather） | Video 1 |
| 预知 | 閾值（Threshold） | Video 3 |
| 简单工具 | 減淡工具（Dodge Tool） | Video 3（存疑） |
| 扛車加鉤 / 扛 J | Ctrl+J（複製圖層快捷鍵） | 通用 |
| 曲線塗層 | 曲線調整圖層（Curves Adjustment Layer）| 通用 |

---

## 五、適合 / 不適合自動化的判斷標準

（新影片 Phase 3 分析時參考）

### 適合自動化 ✅

- 步驟有固定順序，無需根據畫面即時判斷
- 參數有具體數值，或可設合理預設值
- 每個步驟的目標圖層/選取範圍明確

### 半自動化 ⚠️（需暫停讓使用者操作）

- 需要手動塗抹（畫筆類工具）
- 透視變形幅度需根據實際照片視角決定
- 「調到滿意為止」類型的步驟

### 不適合自動化 ❌（暫時跳過）

- 全程依賴手感的藝術性操作
- AI（Illustrator）影片（目前無 Python COM 支援）
- 過於依賴特定素材的步驟（無法泛化）
