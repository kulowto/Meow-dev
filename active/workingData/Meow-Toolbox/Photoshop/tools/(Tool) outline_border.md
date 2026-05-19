---
type: tool
tool_id: outline_border
scope: Photoshop
version: v1.0
created: 2026-05-13
blueprint: Meow-Toolbox/Photoshop/(AI_Read) PSD Master Blueprint.md
script: D:\Meow-Env\Meow-agent\ps_tools\tools\outline_border.py
---

# outline_border：外輪廓工具

---

## 描述

在角色輪廓外產生兩個疊加圖層——白色填色層（`chr_outLine`）與黑色線條環（`chr_outerLine`）。
讓角色在各種背景色上都能保持清晰的輪廓分離感，是角色美術後製的基礎外框效果。

**適合調用的情境：**
- 角色去背完成後，需要加上輪廓強調效果
- 製作遊戲封面、社群貼文、影片縮圖，背景為深色或複雜圖案時
- 需要角色從背景中明顯「跳出」的視覺效果

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
| `expand_px` | int | 否（預設 12） | 輪廓向外擴張的像素數 |
| `line_width` | int | 否（預設 3） | 黑色線條環的寬度（像素） |

### 輸出

執行完畢後，`chr_effects` 群組內新增兩個圖層：

| 圖層名稱 | 位置 | 混合模式 | Layer Mask |
|---------|------|---------|-----------|
| `chr_outLine` | chr_effects 內，chr_halfTone 下方 | Normal | 無 |
| `chr_outerLine` | chr_effects 內，chr_outLine 下方（最底層） | Multiply | 無 |

---

## 步驟

### chr_outLine（白色外輪廓填色）

1. 複製 `src_main`，命名為 `chr_outLine`
2. 刪除繼承的 Layer Mask（填色需延伸到角色輪廓外，Mask 會截掉）
3. 清除所有像素（使圖層完全透明）
4. 從 `src_main` 的透明通道載入選取範圍
5. Expand 選取範圍 `expand_px` 像素
6. 填入白色（RGB: 255, 255, 255）
7. 取消選取
8. 移入 `chr_effects` 群組（PlaceAtEnd）

### chr_outerLine（黑色外輪廓線條環）

1. 複製 `src_main`，命名為 `chr_outerLine`
2. 刪除繼承的 Layer Mask
3. 清除所有像素
4. 從 `src_main` 的透明通道載入選取範圍 → Expand `expand_px`px → 填黑（整體外形）
5. 再次從 `src_main` 載入選取範圍 → Expand `(expand_px - line_width)`px → 刪除內部像素
6. 結果：保留 `line_width`px 寬的黑色線條環
7. 取消選取
8. 設定混合模式為 Multiply
9. 移入 `chr_effects` 群組（PlaceAtEnd）

---

## 工具（函式清單）

| 函式名稱 | 所在檔案 | 用途 |
|---------|---------|------|
| `apply_outline_border()` | `ps_tools/tools/outline_border.py` | 主入口，依序執行下方兩個函式 |
| `_make_outLine()` | `ps_tools/tools/outline_border.py` | 建立 chr_outLine |
| `_make_outerLine()` | `ps_tools/tools/outline_border.py` | 建立 chr_outerLine |
| `_load_layer_selection()` | `ps_tools/ps_utils.py` | 從圖層透明通道載入選取 |
| `_expand_selection()` | `ps_tools/ps_utils.py` | 擴張選取範圍 |
| `_fill_color()` | `ps_tools/ps_utils.py` | 填色 |
| `_delete_selection()` | `ps_tools/ps_utils.py` | 刪除選取內像素 |
| `_delete_layer_mask()` | `ps_tools/ps_utils.py` | 刪除 Layer Mask |
| `_clear_layer_pixels()` | `ps_tools/ps_utils.py` | 清除圖層所有像素 |
| `_set_blend_mode()` | `ps_tools/ps_utils.py` | 設定混合模式 |

---

## 圖層區域與優先級

> 排列最終圖層順序時，查閱：`Meow-Toolbox/Photoshop/(AI_Read) PSD Master Blueprint.md`

| 圖層 | Zone | Priority |
|------|------|----------|
| `chr_outLine` | C - EFFECT_UNDERLAY | 10 |
| `chr_outerLine` | C - EFFECT_UNDERLAY | 20 |

---

## 參數

| 參數名稱 | 預設值 | 說明 |
|---------|--------|------|
| `expand_px` | `12` | 輪廓向外擴張的像素數。同時影響白色填色的厚度與黑色線條環的位置 |
| `line_width` | `3` | 黑色線條環的寬度（像素）。實際線條 = expand_px 外形扣掉 (expand_px - line_width) 內形 |

---

## 副檔（條件性參考）

無（目前無額外條件性文件）

---

## 驗證標準

執行完畢後，確認以下條件全部通過：

- [ ] `chr_outLine` 存在於 `chr_effects` 群組內
- [ ] `chr_outerLine` 存在於 `chr_effects` 群組內
- [ ] `chr_outLine` 的混合模式為 **Normal**
- [ ] `chr_outerLine` 的混合模式為 **Multiply**
- [ ] `chr_outLine` 在 `chr_outerLine` 的**上方**（chr_effects 群組內）
- [ ] `chr_outLine` 和 `chr_outerLine` 均**無 Layer Mask**
- [ ] 白色填色在角色輪廓外可見（不被截掉）

---

## 常見錯誤記錄

| 錯誤描述 | 原因 | 解法 |
|---------|------|------|
| 白色填色或黑色線條被截掉，只出現在角色輪廓內 | duplicate src_main 時繼承了 Layer Mask，Mask 限制了填色範圍 | 複製後立即執行 `_delete_layer_mask()` 再 `_clear_layer_pixels()`，確保 Mask 已移除 |
| `line_width` 設定值 ≥ `expand_px` 導致線條消失 | inner = expand_px - line_width ≤ 0，整個黑色區域被刪除 | `line_width` 必須小於 `expand_px`，建議 `line_width` 最大為 `expand_px / 2` |
| chr_outerLine duplicate 失敗 | original 群組已鎖定，無法 duplicate 其中的圖層 | 確認 original 群組在所有 Phase 3 完成前不鎖定，鎖定操作移至 `main()` 最末 |

---

## 告知訊息（使用者說明）

### 使用前說明

此工具會在角色輪廓外建立白色光暈底層與黑色線條環，讓角色更明顯地從背景中突出。
兩個參數可獨立調整：`expand_px` 控制整體輪廓的厚度，`line_width` 控制黑色線條的粗細。

### 參數選擇提示

**`expand_px`（輪廓擴張大小）**：決定白色填色與黑色線條環距離角色邊緣多遠

| 選項 | 數值 | 效果說明 |
|------|------|---------|
| 小 | `6` | 細緻緊貼的輪廓，適合精緻風或小圖使用 |
| 中（預設）| `12` | 標準輪廓，適合多數遊戲封面與社群貼文 |
| 大 | `20` | 粗獷顯眼的輪廓，適合強調風格或大型橫幅 |
| 自訂 | 使用者輸入 | 直接輸入像素數，不限範圍 |

**`line_width`（線條粗細）**：決定黑色外框線條的寬度

| 選項 | 數值 | 效果說明 |
|------|------|---------|
| 小 | `2` | 細線條，輪廓感精緻低調 |
| 中（預設）| `3` | 標準線條，清晰有力 |
| 大 | `6` | 粗線條，強調輪廓，漫畫感較強 |
| 自訂 | 使用者輸入 | 需小於 `expand_px` 的值 |
