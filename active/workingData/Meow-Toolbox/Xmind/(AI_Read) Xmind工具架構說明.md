---
文件類型: AI_Read  版本: v0.1  建立: 2026-05-22  最後更新: 2026-05-22
reviewed: false
---

# Xmind 工具架構說明

## 工具定位

心智圖輔助工具組，服務「影片製作腳本化」流程：
1. AI 讀取 / 修改 `.xmind` 檔案內容（工具一）
2. 將 `.xmind` 轉換為 Obsidian Canvas 格式供瀏覽（工具二）

## 工具清單

| 工具 | 檔案 | 狀態 | 說明 |
|------|------|------|------|
| xmind_reader | `tools/xmind_reader.py` | 待實作 | 解壓 `.xmind`、讀寫 `content.json` |
| xmind_to_canvas | `tools/xmind_to_canvas.py` | 待實作 | 轉換層次結構為 Canvas JSON，自動計算節點座標 |

## 目錄結構

```
Xmind/
├── (AI_Read) Xmind工具架構說明.md   ← 本文件
├── tools/
│   ├── xmind_reader.py              ← 工具一：讀寫 .xmind
│   └── xmind_to_canvas.py          ← 工具二：轉換 .canvas
└── schema/
    ├── (Ref) xmind-format.md        ← .xmind 格式參考
    └── (Ref) canvas-format.md       ← .canvas 格式參考
```

## 工作流程

```
使用者用 Xmind 建圖
       ↓
[工具一] xmind_reader.py
  - 解壓 .xmind（ZIP）
  - 讀取 content.json（層次樹狀結構）
  - AI 爬相關檔案 → 填入 / 修改節點內容
  - 打包回 .xmind
       ↓
使用者在 Xmind 確認內容 → 按自動排版
       ↓
[工具二] xmind_to_canvas.py（選用）
  - 讀取修改後的 .xmind
  - 用樹狀排版演算法計算 X/Y 座標
  - 輸出 .canvas（Obsidian 可開）
       ↓
AI 輸出影片腳本草稿（Markdown）
```

## 設計原則

- **Xmind 為主力編輯工具**：使用者享有快捷鍵 + 自動排版，AI 只改內容不管排版
- **Canvas 為唯讀輸出**：轉換後僅供瀏覽，不在 Canvas 裡再次編輯
- **工具一先完成**：工具二依賴工具一，開發順序固定

## 格式說明

詳見 `schema/` 下的格式參考文件：
- `.xmind` 格式 → `(Ref) xmind-format.md`
- `.canvas` 格式 → `(Ref) canvas-format.md`
