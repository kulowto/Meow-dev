---
文件類型: AI_Read  版本: v0.3  建立: 2026-05-22  最後更新: 2026-05-22
reviewed: false
---

# Xmind 工具架構說明

## 工具定位

心智圖輔助工具組，服務「影片製作腳本化」與「資料整理」兩條流程：
1. 讀取 / 修改 `.xmind` 內容（工具一）
2. 轉換為 Obsidian Canvas 供瀏覽（工具二）
3. AI 語意整理資料 → 輸出整理後格式（工具三 / 四 / 五）

---

## 工具清單

| 工具 | 檔案 | 狀態 | 說明 |
|------|------|------|------|
| 一：xmind_reader | `tools/xmind_reader.py` | ✅ 完成 | 讀 / 寫 / 搜尋 / 修改 .xmind |
| 二：xmind_to_canvas | `tools/xmind_to_canvas.py` | ✅ 完成 | Xmind → Obsidian Canvas（自動排版） |
| 三：xmind_organizer | `tools/xmind_organizer.py` | ✅ 完成 | Xmind → AI 語意整理 → 標準化 JSON |
| 四：xmind_writer | `tools/xmind_writer.py` | ✅ 完成 | 標準化 JSON → 寫回 .xmind |
| 五：xmind_to_md | `tools/xmind_to_md.py` | ✅ 完成 | Xmind / JSON → Markdown（可讀可編輯） |
| CLI | `tools/xmind_organize_run.py` | ✅ 完成 | 工具三 + 四 整合入口，詢問輸出格式 |

---

## 目錄結構

```
Xmind/
├── (AI_Read) Xmind工具架構說明.md      ← 本文件
├── (AI_Read) Xmind整理工具使用規範.md  ← 工具三/四/五 使用 SOP
├── tools/
│   ├── xmind_reader.py                 ← 工具一
│   ├── xmind_to_canvas.py              ← 工具二
│   ├── xmind_organizer.py              ← 工具三（AI 整理，可抽換 LLM）
│   ├── xmind_writer.py                 ← 工具四（JSON → .xmind）
│   ├── xmind_to_md.py                  ← 工具五（→ Markdown）
│   └── xmind_organize_run.py           ← CLI 整合入口
└── schema/
    ├── (Ref) xmind-format.md           ← .xmind 格式參考
    ├── (Ref) canvas-format.md          ← .canvas 格式參考
    ├── (Ref) xmind-md-format.md        ← MD 格式規格（輸出慣例）
    └── (Prompt) Xmind資訊整理Prompt規格.md  ← AI 整理用 Prompt
```

---

## 工作流程

### 流程 A：瀏覽用（Xmind → Canvas）

```
.xmind → [工具二] xmind_to_canvas.py → .canvas（Obsidian 開啟）
```

### 流程 B：整理發想中的 Xmind（主要用途）

```
.xmind
  → [工具一] 讀取原始樹狀結構 + boundaries
  → [工具三] AI 語意分類整理 → 標準化 JSON
        ↓                          ↓
  [工具五] → .md          [工具四] → .xmind
  （人工調整）             （直接使用）
        ↓
  手動調整 JSON
        ↓
  [工具四] → .xmind（整理版）
        ↓（選用）
  [工具二] → .canvas（瀏覽整理結果）
```

### 流程 C：不需 AI，直接輸出 MD

```
.xmind → [工具五] xmind_to_md.py → .md（直接閱讀 / 編輯）
```

---

## 標準化 JSON 格式（工具三/四/五 共用的 pivot 格式）

```json
{
  "title": "節點標題",
  "note": "備註（字串）",
  "boundaries": [
    { "title": "圈選框標題", "range": "(0,2)" }
  ],
  "children": [
    { "title": "子節點", "note": "...", "children": [...] }
  ],
  "_meta": { "source": "原始路徑", "root_title": "根節點標題" }
}
```

> 與 Xmind 原始格式的差異：`children` 是陣列（非 `{attached: [...]}`），`note` 是字串（非 `{content: "..."}`），`boundaries` 無 `id`/`class`（寫入時自動補）。

---

## 設計原則

- **解耦**：整理（工具三）與格式輸出（工具四 / 五）分開，可獨立替換
- **Pivot JSON**：所有工具以標準化 JSON 作為中間格式傳遞
- **LLM 可抽換**：工具三的 `LLMClient` 以 provider 參數切換，預設 Anthropic
- **Xmind 為主力編輯**：AI 只整理內容，不干預使用者在 Xmind 裡的排版
- **Canvas 為唯讀輸出**：轉換後僅供瀏覽，不在 Canvas 裡再次編輯
