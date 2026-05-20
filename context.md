# Meow-Dev 工作上下文
更新時間：2026-05-20 21:29

## 當前任務
影片轉 PS 工具開發流程（影片 → MEMO.AI 轉錄 → 步驟萃取 → 工具規格草稿 → 實機驗證 → 實作）

## 待續事項

### 影片轉工具 Pipeline（Phase 進度）

- **Video 1（路面積水效果）**：Phase 3 完成，等使用者實機驗證後進行 Phase 4 確認
  規格草稿：`架構Wiki.../04_工具開發流程/(AI_Read) 工具規格草稿_Video1_路面积水效果.md`
- **Video 3（素描效果）**：Phase 3 完成，步驟 3 有「减淡工具」辨識存疑待確認，等 Phase 4
  規格草稿：`架構Wiki.../04_工具開發流程/(AI_Read) 工具規格草稿_Video3_素描效果.md`
- **Video 4（絲網印刷效果）**：Phase 4 完成，待 Phase 5 實作
  規格草稿：`架構Wiki.../04_工具開發流程/(AI_Read) 工具規格草稿_Video4_絲網印刷效果.md`
- **Video 5（矩形漸變構圖）**：Phase 4 完成（2026-05-20）
  確認項：漸變色為手動介入、位移邏輯=物件寬度、重複變換改條件迴圈（超出畫面為止）、步驟 6 改為提示使用者輸入文案
  規格草稿：`架構Wiki.../04_工具開發流程/(AI_Read) 工具規格草稿_Video5_矩形漸變構圖.md`
- **Video 6（AI 凌亂線條字）**：Phase 4 完成（2026-05-20），軟體為 Illustrator，實作暫時跳過
  確認項：步驟 3 Shift+X、效果為鋸齒化（Zig Zag）、步驟 4 移動拷貝補入、字型相依性機制建立、已驗證字型清單待累積
  規格草稿：`架構Wiki.../04_工具開發流程/(AI_Read) 工具規格草稿_Video6_AI凌亂線條字.md`
- **Video 7（雙氛圍感光效）**：Phase 3 完成，待確認「Ctrl+2」是否為 Ctrl+Shift+I，等 Phase 4
  規格草稿：`架構Wiki.../04_工具開發流程/(AI_Read) 工具規格草稿_Video7_雙氛圍感光效.md`
- **Video 8（透明玻璃字）**：Phase 3 完成，圖層樣式數值全部「看影片」，需實機記錄，等 Phase 4
  規格草稿：`架構Wiki.../04_工具開發流程/(AI_Read) 工具規格草稿_Video8_透明玻璃字.md`

### 下一步優先順序
1. 使用者實機測試 Video 7 / 8（PS）→ 回報 Phase 4 修正
2. 使用者實機測試 Video 1 / 3（PS）→ 回報 Phase 4 修正
3. 累積足夠樣本後，進行「向上抽象化」→ 產出通用規範檔案
4. Video 4 進 Phase 5 實作
5. 修正 `ps_auto.py:86` 的 `chr_halfTone` 毒性操作（`chr_layer.duplicate()` → `_duplicate_active_layer()`）

## 障礙 / 注意事項

### MEMO.AI 自動化操作方式
- 用 CDP Python 腳本（WebSocket 連 `localhost:9222`）控制 MEMO.AI 桌面應用
- 關鍵腳本：`C:/Users/AkatsukiNeko/AppData/Local/Temp/memo_batch_v2.py`（批次版，含舊逐字稿清除等待修正）
- ⚠️ 確認轉錄前必須設定：模型選「高品質-Medium」、GPU 加速開啟、自動斷句開啟
- 逐字稿存放：`C:/Users/AkatsukiNeko/AppData/Local/Temp/memo_transcript_[VideoN].txt`

### 工具開發現況
- `ps_auto.py` v0.6：Phase 1（去背）+ Phase 2（圖層結構）+ Phase 3（四個特效）全部跑通
- `chr_halfTone` 尚未封裝，且 `ps_auto.py:86` 仍用 `chr_layer.duplicate()` 毒性操作（TODO 標記存在）
- 已封裝工具：`source_separation.py` / `contour_line.py` / `outline_border.py`

### 流程分工
- AI 負責：MEMO.AI 操作（輸入 URL、等待、提取文字）+ Phase 3 步驟萃取 + 工具規格草稿
- 使用者負責：實機 PS / AI 操作驗證步驟 + Phase 4 確認定稿

### 關鍵文件路徑
- 流程規範：`架構Wiki.../04_工具開發流程/(AI_Read) 影片轉工具開發流程規範.md`
- 工具架構規範：`架構Wiki.../04_工具開發流程/(AI_Read) PS工具架構設計規範（通用版）.md`
- 工具文件骨架：`Meow-Toolbox/_schema/(Template) PS工具文件骨架.md`
- PSD 圖層規範：`Meow-Toolbox/Photoshop/(AI_Read) PSD Master Blueprint.md`
