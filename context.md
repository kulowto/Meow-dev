# Meow-Dev 工作上下文
更新時間：2026-05-21 17:28

## 當前任務
影片轉 PS 工具開發流程（影片 → MEMO.AI 轉錄 → 步驟萃取 → 工具規格草稿 → 實機驗證 → 實作）

## 待續事項

### 影片轉工具 Pipeline（Phase 進度）

- **Video 1（路面積水效果）**：Phase 3 完成，等使用者實機驗證後進行 Phase 4 確認
  規格草稿：`架構Wiki.../04_工具開發流程/(AI_Read) 工具規格草稿_Video1_路面积水效果.md`
- **Video 3（素描效果）**：Phase 3 完成，步驟 3「減淡工具」辨識存疑待確認，等 Phase 4
  規格草稿：`架構Wiki.../04_工具開發流程/(AI_Read) 工具規格草稿_Video3_素描效果.md`
- **Video 4（絲網印刷效果）**：Phase 4 完成，待 Phase 5 實作
- **Video 5（矩形漸變構圖）**：Phase 4 完成
- **Video 6（AI 凌亂線條字）**：Phase 4 完成，軟體為 Illustrator，實作暫時跳過
- **Video 7（雙氛圍感光效）**：Phase 4 完成（2026-05-21）
- **Video 8（透明玻璃字）**：Phase 4 完成（2026-05-21）

### 下一步優先順序
1. 使用者實機測試 Video 1 / 3（PS）→ 回報 Phase 4 修正
2. Video 4 進 Phase 5 實作
3. 修正 `ps_auto.py:86` 的 `chr_halfTone` 毒性操作（`chr_layer.duplicate()` → `_duplicate_active_layer()`）

## 障礙 / 注意事項

### 規範文件體系（2026-05-21 建立）

| 文件 | 層次 | 用途 |
|------|------|------|
| 開發理念_流程設計與資訊濾網模型 | 元層次 | 濾網概念、上下游雙向規範，給未來 AI 讀的 |
| 影片轉工具開發流程規範（v0.3） | 粗濾網 | Phase 1-5 流程規則，新增步驟 0 / 最後步驟 / 可調參數格式規範 |
| 語音辨識錯誤紀錄_Debug | 細濾網 | V1-V8 已知語音辨識錯誤分類紀錄，Phase 3 二次優化用 |
| PS工具架構設計規範（v0.2） | 下游 | 補入上游對接說明 + 規格草稿欄位對程式碼的對應表 |

- 規範文件路徑：`架構Wiki與AI的協作環境/04_工具開發流程/`
- 粗濾網（流程規範）與細濾網（Debug 紀錄）不並用，先粗後細

### MEMO.AI 自動化操作方式
- 用 CDP Python 腳本（WebSocket 連 `localhost:9222`）控制 MEMO.AI 桌面應用
- 關鍵腳本：`C:/Users/AkatsukiNeko/AppData/Local/Temp/memo_batch_v2.py`
- ⚠️ 確認轉錄前必須設定：模型選「高品質-Medium」、GPU 加速開啟、自動斷句開啟

### 工具開發現況
- `ps_auto.py` v0.6：Phase 1（去背）+ Phase 2（圖層結構）+ Phase 3（四個特效）全部跑通
- `chr_halfTone` 尚未封裝，且 `ps_auto.py:86` 仍用 `chr_layer.duplicate()` 毒性操作（TODO 標記存在）
- 已封裝工具：`source_separation.py` / `contour_line.py` / `outline_border.py`

### 關鍵文件路徑
- 流程規範：`架構Wiki.../04_工具開發流程/(AI_Read) 影片轉工具開發流程規範.md`
- 工具架構規範：`架構Wiki.../04_工具開發流程/(AI_Read) PS工具架構設計規範（通用版）.md`
- 工具文件骨架：`Meow-Toolbox/_schema/(Template) PS工具文件骨架.md`
