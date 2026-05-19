---
type: tool
tool_id: contour_line
scope: Photoshop
version: v1.0
created: 2026-05-13
blueprint: Meow-Toolbox/Photoshop/(AI_Read) PSD Master Blueprint.md
script: D:\Meow-Env\Meow-agent\ps_tools\tools\contour_line.py
---

# contour_line：輪廓線工具

---

## 描述

使用 **Color Dodge 邊緣提取技法**，從角色圖層自動生成白底黑線的輪廓線稿（`chr_contourLine`）。

此技法不依賴原圖的描邊顏色，而是透過數學計算邊緣，對任何角色圖均有效——包括描邊偏淺、或填色區有暗色漸層的圖片。

**適合調用的情境：**
- 角色去背完成後，需要提取輪廓線稿進行後製疊加
- 製作遊戲封面、社群貼文、影片縮圖，需要線稿層次感
- 搭配 `chr_halfTone`、`chr_outLine`、`chr_outerLine` 組成完整的角色特效堆疊

**技法原理詳見：**
`Meow-Toolbox/Photoshop/(AI_Read) 線稿提取技法：Color Dodge 邊緣提取.md`

---

## 前置條件

調用此工具前，文件必須滿足以下條件：

- [ ] PART B 完成：`src_main` 圖層存在且含 Layer Mask（去背完成）
- [ ] `chr_effects` 群組已建立
- [ ] `original` 群組**尚未鎖定**（鎖定後 duplicate 會失敗）

---

## 輸入 / 輸出定義

### 輸入

| 參數名稱 | 類型 | 必填 | 說明 |
|---------|------|------|------|
| `app` | PS Application | ✅ | Photoshop 應用程式物件 |
| `doc` | PS Document | ✅ | 目標文件物件 |
| `chr_layer` | PS Layer | ✅ | `src_main` 圖層 reference |
| `effects_group` | PS LayerSet | ✅ | `chr_effects` 群組 reference |
| `minimum_radius` | int | 否（預設 3） | 最小值濾鏡半徑，影響線條粗細 |
| `black_in` | int | 否（預設 150） | Levels 黑場，影響線條清晰度 |
| `white_in` | int | 否（預設 240） | Levels 白場，影響亮部清理程度 |
| `gamma` | float | 否（預設 0.7） | Levels Gamma，影響中間調濃淡 |

### 輸出

執行完畢後，`chr_effects` 群組內新增一個圖層：

| 圖層名稱 | 位置 | 混合模式 | Layer Mask |
|---------|------|---------|-----------|
| `chr_contourLine` | chr_effects 內最上層 | Multiply | 繼承自 src_main |

---

## 步驟

1. 複製 `src_main`，命名為 `chr_desaturate`，移至文件頂層
2. 對 `chr_desaturate` 執行去色（Desaturate）
3. 複製 `chr_desaturate`，命名為 `chr_desaturate_invert`
4. 對 `chr_desaturate_invert` 執行：反色（Invert）→ Color Dodge 混合模式 → 最小值濾鏡（`minimum_radius`px）
5. Merge Down：將 Color Dodge 視覺效果烘焙為真實像素，結果圖層命名為 `chr_contourLine`
6. Levels 清理（黑場 `black_in` / 白場 `white_in` / Gamma `gamma`）
7. Blend If This Layer 白場 245（best-effort，失敗時由 Step 8 兜底）
8. 設定混合模式為 Multiply
9. 移入 `chr_effects` 群組（PlaceAtEnd，成為群組最上層）

---

## 工具（函式清單）

| 函式名稱 | 所在檔案 | 用途 |
|---------|---------|------|
| `apply_contour_line()` | `ps_tools/tools/contour_line.py` | 主入口，執行完整七步驟流程 |
| `_desaturate()` | `ps_tools/ps_utils.py` | 去色 |
| `_invert()` | `ps_tools/ps_utils.py` | 反色 |
| `_set_blend_mode()` | `ps_tools/ps_utils.py` | 設定混合模式（Color Dodge / Multiply） |
| `_minimum_filter()` | `ps_tools/ps_utils.py` | 最小值濾鏡，擴張線條 |
| `_merge_down()` | `ps_tools/ps_utils.py` | 向下合併，烘焙 Color Dodge 效果 |
| `_levels()` | `ps_tools/ps_utils.py` | Levels 調整，清理雜訊強化線條 |
| `_set_blend_if_this_white()` | `ps_tools/ps_utils.py` | Blend If 白場（best-effort，回傳 True/False） |

---

## 圖層區域與優先級

> 排列最終圖層順序時，查閱：`Meow-Toolbox/Photoshop/(AI_Read) PSD Master Blueprint.md`

| 圖層 | Zone | Priority |
|------|------|----------|
| `chr_contourLine` | A - EFFECT_OVERLAY | 10 |

---

## 參數

| 參數名稱 | 預設值 | 說明 |
|---------|--------|------|
| `minimum_radius` | `3` | 最小值濾鏡半徑。值越大，線條越粗；值越小，線條越細但可能斷裂 |
| `black_in` | `150` | Levels 黑場。亮度低於此值的像素全推成純黑，值越高線條越清晰但細節越少 |
| `white_in` | `240` | Levels 白場。亮度高於此值的才算純白，影響亮部殘留程度 |
| `gamma` | `0.7` | Levels Gamma。小於 1.0 壓暗中間調使線條更濃；大於 1.0 提亮使線條更淡 |

---

## 副檔（條件性參考）

| 文件 | 觸發條件 | 說明 |
|------|---------|------|
| `(AI_Read) 線稿提取技法：Color Dodge 邊緣提取.md` | 修改任何步驟或參數前 | 記錄每個步驟的設計意圖與參數調整指南 |

---

## 驗證標準

執行完畢後，確認以下條件全部通過：

- [ ] `chr_contourLine` 存在於 `chr_effects` 群組內
- [ ] `chr_contourLine` 為 `chr_effects` 群組的**最上層**圖層
- [ ] 混合模式為 **Multiply**
- [ ] 角色邊緣有清晰的黑色線條，填色平坦區域接近白色（Multiply 下透明）
- [ ] 中間工作圖層（`chr_desaturate`、`chr_desaturate_invert`）已消失（Merge Down 後）

---

## 常見錯誤記錄

| 錯誤描述 | 原因 | 解法 |
|---------|------|------|
| Blend If 兩種方法均失敗（`-2147212704`） | PS 27.6 的 `blendRange` action descriptor API 不穩定 | 已知問題，由 Multiply 混合模式兜底，視覺效果等同；Blend If 修復後自動生效 |
| 線條之外有大量灰色殘留 | 黑場（`black_in`）太低，雜訊沒被清掉 | 把 `black_in` 從 150 往上調（試 170–200） |
| 線條斷裂或太細 | 黑場太高，把線條邊緣也推掉 | `black_in` 往下調（試 120–140）；或 `minimum_radius` 從 3 調到 4 |
| 整體線條太淡 | Gamma 太高 | `gamma` 從 0.7 往下調（試 0.5–0.6） |
| 線條太濃，角色細節消失 | Gamma 太低或黑場太高 | `gamma` 往上調（試 0.8–1.0），同時降低 `black_in` |
| duplicate 失敗 | `original` 群組已鎖定 | 確認 original 群組在所有 Phase 3 完成前不鎖定 |

---

## 告知訊息（使用者說明）

### 使用前說明

此工具使用 Color Dodge 邊緣提取技法，自動從角色圖生成輪廓線稿，不需要原圖有明顯黑色描邊。
生成的 `chr_contourLine` 以 Multiply 混合模式疊加在角色上方，白色區域透明、黑色線條保留，呈現線稿疊加效果。

Levels 參數可依圖片品質微調，每次只調一個參數，確認效果後再動下一個。

### 參數選擇提示

**`minimum_radius`（最小值濾鏡半徑）**：控制線條的粗細與連續性

| 選項 | 數值 | 效果說明 |
|------|------|---------|
| 細 | `2` | 線條細緻，適合精細插畫風格；複雜細節處可能斷線 |
| 中（預設）| `3` | 標準線條，適合多數遊戲角色美術 |
| 粗 | `4` | 線條較粗紮實，適合輪廓不夠清晰的圖片 |
| 自訂 | 使用者輸入 | 直接輸入數值 |

**`black_in`（Levels 黑場）**：控制線條清晰程度與雜訊殘留

| 選項 | 數值 | 效果說明 |
|------|------|---------|
| 低 | `120` | 保留更多線條細節，但背景灰色雜訊較多 |
| 中（預設）| `150` | 標準清理，適合多數遊戲角色美術 |
| 高 | `180` | 線條最乾淨，但可能犧牲部分細線條 |
| 自訂 | 使用者輸入 | 建議範圍 100–220 |

**`gamma`（Levels Gamma）**：控制中間調濃淡

| 選項 | 數值 | 效果說明 |
|------|------|---------|
| 濃 | `0.5` | 中間調整體壓暗，線條最濃最清晰 |
| 中（預設）| `0.7` | 標準，線條清晰且保留部分灰階過渡 |
| 淡 | `1.0` | 中間調保持原樣，線條較淡，灰色過渡保留較多 |
| 自訂 | 使用者輸入 | 建議範圍 0.4–1.2 |
