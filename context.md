# Meow-Dev 工作上下文
更新時間：2026-05-22 16:30

---

## ▌作業區塊 A：PS 工具開發 Pipeline（影片轉工具）
> 流程：影片 → MEMO.AI 轉錄 → 步驟萃取 → 工具規格草稿 → 實機驗證 → 實作

### 各影片 Phase 進度

- **Video 1（路面積水效果）**：Phase 3 完成，等使用者實機驗證後進行 Phase 4 確認
  規格草稿：`架構Wiki.../04_工具開發流程/(AI_Read) 工具規格草稿_Video1_路面积水效果.md`
- **Video 3（素描效果）**：Phase 3 完成，步驟 3「減淡工具」辨識存疑待確認，等 Phase 4
  規格草稿：`架構Wiki.../04_工具開發流程/(AI_Read) 工具規格草稿_Video3_素描效果.md`
- **Video 4（絲網印刷效果）**：Phase 4 完成，待 Phase 5 實作
- **Video 5（矩形漸變構圖）**：Phase 4 完成
- **Video 6（AI 凌亂線條字）**：Phase 4 完成，軟體為 Illustrator，實作暫時跳過
- **Video 7（雙氛圍感光效）**：Phase 4 完成（2026-05-21）
- **Video 8（透明玻璃字）**：Phase 4 完成（2026-05-21）

### 下一步優先順序（A 區塊）
1. 使用者實機測試 Video 1 / 3（PS）→ 回報 Phase 4 修正
2. Video 4 進 Phase 5 實作
3. 修正 `ps_auto.py:86` 的 `chr_halfTone` 毒性操作（`chr_layer.duplicate()` → `_duplicate_active_layer()`）

### A 區塊：障礙 / 注意事項

**規範文件體系（2026-05-21 建立）**

| 文件 | 層次 | 用途 |
|------|------|------|
| 開發理念_流程設計與資訊濾網模型 | 元層次 | 濾網概念、上下游雙向規範，給未來 AI 讀的 |
| 影片轉工具開發流程規範（v0.3） | 粗濾網 | Phase 1-5 流程規則，新增步驟 0 / 最後步驟 / 可調參數格式規範 |
| 語音辨識錯誤紀錄_Debug | 細濾網 | V1-V8 已知語音辨識錯誤分類紀錄，Phase 3 二次優化用 |
| PS工具架構設計規範（v0.2） | 下游 | 補入上游對接說明 + 規格草稿欄位對程式碼的對應表 |

- 規範文件路徑：`架構Wiki與AI的協作環境/04_工具開發流程/`
- 粗濾網（流程規範）與細濾網（Debug 紀錄）不並用，先粗後細

**MEMO.AI 自動化操作方式**
- 用 CDP Python 腳本（WebSocket 連 `localhost:9222`）控制 MEMO.AI 桌面應用
- 關鍵腳本：`C:/Users/AkatsukiNeko/AppData/Local/Temp/memo_batch_v2.py`
- ⚠️ 確認轉錄前必須設定：模型選「高品質-Medium」、GPU 加速開啟、自動斷句開啟

**工具開發現況**
- `ps_auto.py` v0.6：Phase 1（去背）+ Phase 2（圖層結構）+ Phase 3（四個特效）全部跑通
- `chr_halfTone` 尚未封裝，且 `ps_auto.py:86` 仍用 `chr_layer.duplicate()` 毒性操作（TODO 標記存在）
- 已封裝工具：`source_separation.py` / `contour_line.py` / `outline_border.py`

**關鍵文件路徑**
- 流程規範：`架構Wiki.../04_工具開發流程/(AI_Read) 影片轉工具開發流程規範.md`
- 工具架構規範：`架構Wiki.../04_工具開發流程/(AI_Read) PS工具架構設計規範（通用版）.md`
- 工具文件骨架：`Meow-Toolbox/_schema/(Template) PS工具文件骨架.md`

---

## ▌作業區塊 B：心智圖輔助工具（影片製作腳本化）
> 流程：心智圖（Xmind）→ AI 爬現有檔案 → 填入對應區塊 → 整理文案邏輯 → 輸出影片腳本草稿

### 目前狀態
- 工具一（`xmind_reader.py`）：完成，讀寫 / 搜尋 / 修改 / 樹狀顯示全部就緒
- 工具二（`xmind_to_canvas.py`）：主體完成，投資方法測試中，有已知 BUG 待修
- 測試進度：尤里教 ✓、金字塔原理 ✓、筆記類型 ✓、**投資方法（進行中）**、ＢＤ２（待）

### 下一步優先順序（B 區塊）
1. 跑 `ＢＤ２.xmind`（桌面）
2. 全部 OK 後 → 設計「AI 填入心智圖」workflow，以 BD2 資料為測試素材
3. 修 boundary 第一子節點 BUG（詳見障礙區）

### B 區塊：排版參數現況（xmind_to_canvas.py）

| 參數 | 值 | 說明 |
|------|----|------|
| NODE_W_MIN | 260 | 節點最小寬度 |
| NODE_H | 60 | 節點最小高度 |
| CHARS_PER_LINE | 15 | 每行估算字數（CJK） |
| CHAR_W | 14 | CJK 字元估算寬度（px） |
| LINE_H | 22 | 每行文字高度（px） |
| H_GAP_WIDE | 240 | boundary 層以上水平間距（parent 右邊到 child 左邊） |
| H_GAP_NARROW | 140 | 深層或無 boundary 水平間距 |
| V_GAP | 40 | 同層節點垂直間距 |
| SECTION_GAP | 192 | L1 區塊間額外間距 |
| GROUP_PAD_X | 16 | group box 水平內縮 |
| GROUP_PAD_Y | 8 | group box 垂直內縮 |
| GROUP_MARGIN | 120 | group box 外部間距（baked 進排版） |
| NEST_PAD | 14 | 巢狀 group 最小超出距離 |

### B 區塊：障礙 / 注意事項
- **GROUP_MARGIN 實作重點**：加在 `_children_span` 的首尾 + `_layout` 的 cur_y 起點，才能往上傳給 grandparent 的 subtree height，空間真正留出來
- boundary range `(0, n-1)` 覆蓋全部子節點時，舊做法（只加中間間隔）無效，需首尾都加
- **⚠️ 已知 BUG（待修）**：boundary 群組最上方的子節點若有自己的子節點，子節點內容可能與群組框標籤或上方節點重疊。
  - 已嘗試：在 `_children_span` 和 `_layout` 的 GROUP_MARGIN 之後額外加 V_GAP（當 `children[0]` 有子節點時），但效果不足，問題尚未完全解決。
  - 根本原因：當 span > nh 時，第一個子節點的子節點從 `cur_y`（allocation 頂端）開始，group box 上緣僅 GROUP_PAD_Y=8 的間距，群組標籤與內容重疊。
  - 下次修法方向：考慮增大 GROUP_PAD_Y，或在 `_build_groups` 的 `min_y` 計算時額外減去 V_GAP。
- **投資方法.xmind 正確路徑**：`I:\Obsidian Note\Obsidan-Notes-Merge-Version\_Storing Books\_Investment\_How to investment\投資方法.xmind`（不在 Fleeting Note 目錄）
- 工具腳本路徑：`active/workingData/Meow-Toolbox/Xmind/tools/`
- 測試輸出路徑：桌面（`C:\Users\AkatsukiNeko\Desktop\`）
- 尤里教聯合體系 xmind 路徑有**雙空格**：`尤里教聯合體系  (Yuri United).xmind`
