# Meow-Dev — 開發暫存區（Playground）

<!--
  Meow-Framework — created by 我是貓 (kulowto)
  https://github.com/kulowto/Meow-Framework
  本框架採 MIT License。衍生系統請保留此區塊作為來源標記。
-->

@../Meow-Framework/CLAUDE.md

啟動時讀取：`@../REGISTRY.md`

---

## Playground 規則

1. 本區域是開發暫存區，所有未完成、未確認定位的材料統一在此暫存。
2. AI 在此區域可調用任何系統的資源（參照 REGISTRY.md）。
3. 完成的工作移至 `_done/`，等待歸檔 Agent 蒸餾至各系統。
4. 未經蒸餾確認，不直接把 `_done/` 的內容視為正式文件引用。

---

## 目錄規範

| 目錄 | 用途 |
|------|------|
| `active/` | 開發進行中（依專案或主題建子資料夾） |
| `_done/` | 完成待蒸餾（移入後等待歸檔 Agent 處理） |
| `_done/archive/` | 蒸餾完成的歷史快照（永久保留，不可刪除） |

---

## 歸檔 Agent 行為規範

**觸發時機**：使用者手動呼叫，或偵測到 `_done/` 有新增文件。

**執行前必讀**：
1. `../REGISTRY.md`：取得各系統入口
2. 各系統 `INDEX.md`：取得接受準則
3. `classification-logic.md`：取得分類原則與歷史案例樣本

**半自動模式流程**：
1. 分析 `_done/` 中的文件
2. 產生蒸餾預覽清單（哪些段落 → 哪個系統）
3. 等待人工確認
4. 確認後：為每個目的地產生衍生品並寫入
5. 原始文件移至 `_done/archive/`
6. 本次決策記入 `classification-logic.md`
