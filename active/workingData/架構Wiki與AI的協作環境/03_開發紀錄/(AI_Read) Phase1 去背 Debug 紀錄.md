---
type: dev-progress
scope: Photoshop / Phase 1（PART A / B / C）
version: v4.0
updated: 2026-05-14
status: ✅ PART A / B / C 全部通過
usage: 接手 Phase 1 開發的 AI 必讀。說明各 PART 設計規範、已知 PS 27.6 陷阱與正確解法。
---

# Phase 1 開發進度與設計規範

> **目前任務**：PART A / B / C 已全部通過 Playground 測試，下一步整合進 `ps_auto.py`。

完整流程說明：`(AI_Read) Photoshop 自動化腳本開發.md`

---

## 各 PART 輸入輸出定義

| PART | 輸入 | 輸出 | 說明 |
|------|------|------|------|
| A | 原始 PNG（唯一頂層圖層） | `src_img` | 改名備份，後續 PART 的資料來源 |
| B | `src_img` | `src_main` + Layer Mask | 複製 → autoCutout → 建立 Mask（主體可見） |
| C | `src_img` | `src_background` + Layer Mask | 複製 → autoCutout → 反向選取 → 建立 Mask（背景可見） |

> B 和 C 各自獨立執行 autoCutout，不互相推導，確保各 PART 可單獨運作。

---

## 測試腳本狀態

| 腳本 | 狀態 | 說明 |
|------|------|------|
| `playground/test_part_a.py` | ✅ 全部通過 | A0 IndexedColor→RGB、S1 確認 1 個圖層、A1/A2 改名 |
| `playground/test_part_b.py` | ✅ 全部通過 | B1 duplicate、B2 改名、B3 autoCutout+Mask、B4 驗證 mask |
| `playground/test_part_c.py` | ✅ 全部通過 | C1 duplicate、C2 改名、C3 autoCutout+inverse+Mask、C4/C5 驗證 mask 存在且方向正確（主體中心 brightness=0） |
| 執行方式 | — | `cd ps_tools && python -X utf8 playground/test_xxx.py` |

---

## ⚠️ PS 27.6 Scripting 已知陷阱（本次 debug 實際驗證）

### 陷阱 1：`executeAction("Dplc")` 與 `layer.duplicate()` 在 PS 27.6 全部靜默失敗

**症狀**：
- Python `app.executeAction(charIDToTypeID("Dplc"), desc)` → 不報錯，但 layers 數量不增加
- Python `layer.duplicate()` → 不報錯，但 layers 數量不增加，且**污染 PS 狀態**（後續 doJavaScript 全部 -2147212704）
- JS 內 `app.activeDocument.activeLayer.duplicate(doc, ElementPlacement.PLACEATBEGINNING)` → 同上，靜默失敗且污染狀態

**正確解法**：使用 `stringIDToTypeID("duplicate") + version:5 + ID:[layerID]`，**必須放在 doJavaScript IIFE 內**：

```javascript
(function() {
    var s2t = function(s) { return stringIDToTypeID(s); };
    var c2t = function(s) { return charIDToTypeID(s); };
    try {
        var srcId = app.activeDocument.activeLayer.id;
        var desc = new ActionDescriptor();
        var ref = new ActionReference();
        ref.putEnumerated(s2t("layer"), s2t("ordinal"), s2t("targetEnum"));
        desc.putReference(c2t("null"), ref);
        var idList = new ActionList();
        idList.putInteger(srcId);
        desc.putList(s2t("ID"), idList);
        desc.putString(s2t("name"), "新圖層名稱");
        desc.putInteger(s2t("version"), 5);   // ← 這個是關鍵，少了就靜默失敗
        executeAction(s2t("duplicate"), desc, DialogModes.NO);
        return "OK:" + app.activeDocument.activeLayer.id;
    } catch(e) {
        return "ERR:" + e.number + "|" + e.message;
    }
})();
```

**關鍵差異**：
- `charIDToTypeID("Dplc")` 對應的舊路徑在 PS 27.6 被封鎖
- `stringIDToTypeID("duplicate")` 對應新路徑，但必須帶 `version: 5` 才能觸發
- `version: 5` 由 Adobe 官方「Copy As JavaScript」工具從 Actions 面板生成的 descriptor 揭露

---

### 陷阱 2：「毒性操作」——呼叫後永久污染 COM 橋接狀態

以下操作**呼叫後會讓後續所有 doJavaScript 回傳 -2147212704**，不報錯但狀態損壞：

| 操作 | 說明 |
|------|------|
| `doc.selection.selectAll()` | Python COM 呼叫全選 → 觸發 AI 選取，鎖住 COM 橋接 |
| `layer.duplicate()` | Python COM 複製圖層 → 靜默失敗且污染狀態 |
| `layer.copy()` | Python COM 複製 → 同上 |
| Python `executeAction(slct Lyr Trgt)` 在 autoCutout 後呼叫 | 成功執行但讓後續 doJavaScript 失敗（原因未明） |

**規則**：凡是涉及複製、貼上、選取的操作，**不要用 Python COM 直接呼叫**，一律包進 IIFE 用 JS 執行。

---

### 陷阱 3：`autoCutout` 只建立選取範圍，不建立 Layer Mask

**症狀**：`autoCutout` 執行後回傳 OK，但 `userMaskEnabled` 為 `false`，`hasMaskKey` 也是 `false`。

**根本原因**：`autoCutout` 等同「選取主體」，產生選取範圍（selection）但不自動建立 Mask。

**正確做法**（兩步驟，全放在同一 IIFE 內）：

```javascript
// Step 1：autoCutout（建立選取範圍）
var cutoutDesc = new ActionDescriptor();
cutoutDesc.putBoolean(s2t("sampleAllLayers"), false);
executeAction(s2t("autoCutout"), cutoutDesc, DialogModes.NO);

// Step 2：從選取範圍建立 Layer Mask（revealSelection = 主體白色可見）
var makeDesc = new ActionDescriptor();
var atRef = new ActionReference();
atRef.putEnumerated(s2t("channel"), s2t("channel"), s2t("mask"));
makeDesc.putReference(s2t("at"), atRef);
makeDesc.putClass(s2t("new"), s2t("channel"));
makeDesc.putEnumerated(s2t("using"), s2t("userMaskEnabled"), s2t("revealSelection"));
executeAction(s2t("make"), makeDesc, DialogModes.NO);
```

這兩步都來自 Adobe 官方「Copy As JavaScript」從 Actions 面板生成的 batchPlay descriptor 翻譯而來。

---

### 陷阱 4：Mask 建立後 PS 進入 mask 通道模式，後續 doJavaScript 全部失敗

**症狀**：`make channel mask` 執行後，任何新的 `doJavaScript` 呼叫都回傳 -2147212704。

**錯誤修法（無效）**：
```python
# 從 Python executeAction 切 composite channel → 雖然不報錯，但後續 doJavaScript 還是失敗
app.executeAction(app.charIDToTypeID("slct"), desc, DialogModes.DisplayNoDialogs)
```

**正確修法**：mask 退出動作必須放在**同一個 IIFE 裡、在 `make mask` 之後立即執行**：

```javascript
// make mask 之後，在同一 JS context 內立即切回 composite channel
try {
    var chDesc = new ActionDescriptor();
    var chRef = new ActionReference();
    chRef.putEnumerated(c2t("Chnl"), c2t("Chnl"), c2t("Cmps"));
    chDesc.putReference(c2t("null"), chRef);
    executeAction(c2t("slct"), chDesc, DialogModes.NO);
} catch(chErr) {
    // fallback：若 slct Chnl Cmps 失敗，改選回圖層本體
    var lyrDesc = new ActionDescriptor();
    var lyrRef = new ActionReference();
    lyrRef.putEnumerated(c2t("Lyr "), c2t("Ordn"), c2t("Trgt"));
    lyrDesc.putReference(c2t("null"), lyrRef);
    lyrDesc.putBoolean(c2t("MkVs"), false);
    executeAction(c2t("slct"), lyrDesc, DialogModes.NO);
}
```

**核心原則**：任何會改變 PS 通道/模式狀態的操作，恢復動作必須在**同一個 IIFE 內完成**，不能依賴後續的 Python 呼叫。

---

### 陷阱 5：`selectSubject` 在 PS 27.6 scripting 完全無法使用

**症狀**：所有已知的 selectSubject 呼叫方式均回傳 -2147212704 或被忽略。

**解法**：改用 `autoCutout`（需搭配 Step 2 建立 Mask，見陷阱 3）。

---

### 陷阱 6：`executeAction(Cpy)` 在 PS 27.6 回傳 -25920

**症狀**：`executeAction(charIDToTypeID("Cpy "))` 或 `executeAction(stringIDToTypeID("copy"))` 均回傳 -25920「此指令目前無法使用」。

**解法**：不需要 Copy/Paste 路線，改用陷阱 1 的 `duplicate + version:5` 方案。

---

### 陷阱 7：ExtendScript 在某些 PS 狀態下沒有 `JSON` 物件

**症狀**：在某些 PS 操作後的 doJavaScript 呼叫中，`JSON.stringify()` 拋 `ReferenceError: JSON 未定義`（ERR:2）。

**解法**：不依賴 `JSON.stringify`，改用字串拼接：
```javascript
return "name=" + layer.name + "|id=" + layer.id + "|userMaskEnabled=" + maskEnabled;
```

---

### 陷阱 8：裸 doJavaScript（非 IIFE）存取可能不存在的屬性會拋 COM 錯誤

**症狀**：`app.doJavaScript("layer.userMaskEnabled")` 若 layer 沒有 mask，拋 JS 例外，Python 端收到 -2147212704。

**解法**：所有 doJavaScript 呼叫一律包 IIFE + try/catch，JS 例外在 JS 內處理，不讓它穿透 COM 橋接：
```javascript
(function() {
    try {
        var val = app.activeDocument.activeLayer.userMaskEnabled;
        return val ? "true" : "false";
    } catch(e) {
        return "ERR:" + e.number + "|" + e.message;
    }
})();
```

---

### 陷阱 9：`_ensure_rgb_mode` 的 `doc.mode` 值與 `changeMode` 對照完全相反（PS COM 實際值）

**症狀**：呼叫 `_ensure_rgb_mode(doc)` 後，文件被轉成 CMYK 而非 RGB，導致 `autoCutout` 拋 -25920「選取主體目前無法使用」。

**根本原因**：PS COM 的 `doc.mode` 與 `ChangeMode` enum 整數值對照如下：

| `doc.mode` 回傳值 | 意義 | `ChangeMode` 轉換值 |
|---|---|---|
| 2 | **RGB**（正確） | `ConvertToRGB = 2` |
| 3 | **CMYK** | `ConvertToCMYK = 3` |

舊版 `_ensure_rgb_mode` 誤以為 `3 = RGB`，導致 `doc.changeMode(3)` 把任何非 CMYK 文件（包含 RGB 本身）全部轉成 CMYK。

**正確寫法**：
```python
def _ensure_rgb_mode(doc):
    if doc.mode != 2:   # 2 = RGB
        doc.changeMode(2)   # ChangeMode.ConvertToRGB = 2
```

**驗證方式**：`app.doJavaScript("String(app.activeDocument.mode)")` 回傳 `"DocumentMode.RGB"` 或 `"DocumentMode.CMYK"`，比 Python `doc.mode` 更直觀可讀。

---

### 陷阱 10：反向選取（Select > Inverse）vs 反色（Image > Adjustments > Invert）

**症狀**：PART C 想要「反向選取（選取範圍對調）」，但程式做的是「反色（像素顏色 RGB 取補色）」，導致 mask 方向看起來是套用了顏色負片效果而非選取反轉。

| 操作 | 正確 charID/stringID | 說明 |
|---|---|---|
| **反向選取**（Select > Inverse）✅ | `s2t("inverse")` | 選取範圍互換（主體→背景） |
| 反色（Image > Adjustments > Invert）❌ | `c2t("Invr")` | 像素 RGB 取補色，與選取無關 |

**正確程式碼**（PART C 反向選取步驟）：
```javascript
executeAction(stringIDToTypeID("inverse"), new ActionDescriptor(), DialogModes.NO);
```

---

### 陷阱 11：mask 通道選取需要先從 Python 選圖層，不能全在 JS IIFE 內

**症狀**：在 JS IIFE 內直接 `slct Chnl Msk` 回傳 -25920「選取目前無法使用」，無論用 `s2t("mask")` 或 `c2t("Msk ")` 都失敗。

**正確做法**（仿照 `_invert_layer_mask`）：
```python
# Step 1：Python 先用 executeAction 選取圖層（by ID）
desc = ps.ActionDescriptor()
ref = ps.ActionReference()
ref.putIdentifier(app.charIDToTypeID("Lyr "), layer_id)
desc.putReference(app.charIDToTypeID("null"), ref)
desc.putBoolean(app.charIDToTypeID("MkVs"), False)
app.executeAction(app.charIDToTypeID("slct"), desc, DialogModes.DisplayNoDialogs)

# Step 2：JS 再選 Msk 通道（charID + MkVs=false）
app.doJavaScript("""
    var chDesc = new ActionDescriptor();
    var chRef = new ActionReference();
    chRef.putEnumerated(c2t("Chnl"), c2t("Chnl"), c2t("Msk "));
    chDesc.putReference(c2t("null"), chRef);
    chDesc.putBoolean(c2t("MkVs"), false);
    executeAction(c2t("slct"), chDesc, DialogModes.NO);
    // ... 取樣、退出 ...
""")
```

**附加說明**：`layer.userMaskEnabled` 的 Python COM 屬性讀值不可靠（即使 mask 存在且啟用也可能回傳 false）。可靠讀法是用 `executeActionGet` ActionDescriptor 的 `getBoolean(s2t("userMaskEnabled"))` 方法。

---

## 完整 `_auto_cutout` 正確實作

以下是符合上述所有規則的最終實作（已整合進 `ps_utils.py`）：

```javascript
(function() {
    var s2t = function(s) { return stringIDToTypeID(s); };
    var c2t = function(s) { return charIDToTypeID(s); };
    try {
        // 設定 device 模式（確保 AI 去背使用 GPU 加速）
        var setDesc = new ActionDescriptor();
        var prefsRef = new ActionReference();
        prefsRef.putProperty(s2t("property"), s2t("imageProcessingPrefs"));
        prefsRef.putEnumerated(s2t("application"), s2t("ordinal"), s2t("targetEnum"));
        setDesc.putReference(s2t("null"), prefsRef);
        var prefsDesc = new ActionDescriptor();
        prefsDesc.putEnumerated(
            s2t("imageProcessingSelectSubjectPrefs"),
            s2t("imageProcessingSelectSubjectPrefs"),
            s2t("imageProcessingModeDevice")
        );
        setDesc.putObject(s2t("to"), s2t("imageProcessingPrefs"), prefsDesc);
        executeAction(s2t("set"), setDesc, DialogModes.NO);

        // Step 1：autoCutout（建立選取範圍，不建立 Mask）
        var cutoutDesc = new ActionDescriptor();
        cutoutDesc.putBoolean(s2t("sampleAllLayers"), false);
        executeAction(s2t("autoCutout"), cutoutDesc, DialogModes.NO);

        // Step 2：從選取範圍建立 Layer Mask
        var makeDesc = new ActionDescriptor();
        var atRef = new ActionReference();
        atRef.putEnumerated(s2t("channel"), s2t("channel"), s2t("mask"));
        makeDesc.putReference(s2t("at"), atRef);
        makeDesc.putClass(s2t("new"), s2t("channel"));
        makeDesc.putEnumerated(s2t("using"), s2t("userMaskEnabled"), s2t("revealSelection"));
        executeAction(s2t("make"), makeDesc, DialogModes.NO);

        // Step 3：在同一 context 內退出 mask 通道模式（不能從 Python 做）
        try {
            var chDesc = new ActionDescriptor();
            var chRef = new ActionReference();
            chRef.putEnumerated(c2t("Chnl"), c2t("Chnl"), c2t("Cmps"));
            chDesc.putReference(c2t("null"), chRef);
            executeAction(c2t("slct"), chDesc, DialogModes.NO);
        } catch(chErr) {
            var lyrDesc = new ActionDescriptor();
            var lyrRef = new ActionReference();
            lyrRef.putEnumerated(c2t("Lyr "), c2t("Ordn"), c2t("Trgt"));
            lyrDesc.putReference(c2t("null"), lyrRef);
            lyrDesc.putBoolean(c2t("MkVs"), false);
            executeAction(c2t("slct"), lyrDesc, DialogModes.NO);
        }

        return "OK";
    } catch(e) {
        return "ERR:" + e.number + "|" + e.message;
    }
})();
```

---

## 如何確認 `version:5` 和其他正確 descriptor

使用 Adobe 官方「Copy As JavaScript」功能：

1. PS → `Edit > Preferences > Plugins` → 勾選 **Enable Developer Mode** → 重啟 PS
2. 開啟 Actions 面板，錄製你想驗證的操作
3. 選取動作步驟 → 面板右上角 ≡ 選單 → **Copy As JavaScript**（中文：「拷貝成 JavaScript」）
4. 得到的是 UXP batchPlay 格式，對照 `_obj` / `_target` / `version` 翻譯成 ExtendScript `executeAction` 語法

> batchPlay 的 `_obj` = ExtendScript 的 `stringIDToTypeID()`  
> batchPlay 的 `_target` = ExtendScript 的 `putReference(charIDToTypeID("null"), ref)`  
> batchPlay 的 `version` = ExtendScript 的 `desc.putInteger(stringIDToTypeID("version"), 5)`

---

## 各 PART 驗證項目（更新後）

### PART A（✅ 全部通過）
| 代號 | 驗證項目 |
|------|---------|
| A0 | IndexedColor → RGB 自動轉換 |
| S1 | 頂層只有 1 個圖層 |
| A1 | 改名 activeLayer → `src_img`（無例外） |
| A2 | name == "src_img" |

### PART B（✅ 全部通過）
| 代號 | 驗證項目 |
|------|---------|
| S1 | activeLayer.name == "src_img" |
| B1 | duplicate 後新圖層 id ≠ src_img id |
| B2 | name == "src_main" |
| B3a | autoCutout + make mask IIFE 回傳 "OK" |
| B3b | IIFE 後 doJavaScript 可正常呼叫（mask 模式已退出） |
| B4 | hasMaskKey == true（Layer Mask 存在） |

### PART C（⏸ 待建立）
| 代號 | 驗證項目 |
|------|---------|
| S1 | activeLayer.name == "src_img" |
| C1 | duplicate 後新圖層 id ≠ src_img id |
| C2 | name == "src_background" |
| C3a | autoCutout + make mask IIFE 回傳 "OK" |
| C3b | IIFE 後 doJavaScript 可正常呼叫 |
| C4 | hasMaskKey == true |
| C5 | （額外）驗證 Mask 是背景可見（反向）而非主體可見 |

> PART C 的 Mask 要「背景可見」：autoCutout 建立選取（主體），反向選取後再建立 mask（`revealSelection`），黑白與 B 相反。
