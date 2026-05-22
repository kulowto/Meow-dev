---
文件類型: AI_Read  版本: v1.0  建立: 2026-05-22
---

# Xmind 整理工具使用規範

> 適用情境：Xmind 檔案處於「發想中 / 開發中」階段，結構尚未穩定，需要 AI 協助做分類歸納。

---

## 工具全貌

| 工具 | 檔案 | 職責 |
|------|------|------|
| 工具一 | `xmind_reader.py` | 讀寫 / 搜尋 / 修改 Xmind |
| 工具二 | `xmind_to_canvas.py` | Xmind → Obsidian Canvas |
| 工具三 | `xmind_organizer.py` | Xmind → AI 整理 → JSON |
| 工具四 | `xmind_writer.py` | JSON → 寫回 .xmind |
| CLI | `xmind_organize_run.py` | 整合入口，問使用者輸出格式 |

工具三和工具四**解耦設計**：整理邏輯（工具三）與格式轉換（工具四）分開，方便個別替換或測試。

---

## 使用時機

以下情況適合用本工具：

- Xmind 是「還在想」的階段：結構混亂、有重複、層次不清
- 想讓 AI 幫你把資料重新歸類，看出哪些地方有缺漏
- 要從 Xmind 輸出一份「可讀版」給自己或別人看

以下情況**不適合**：

- Xmind 結構已經很明確，只需要轉成 Canvas 看 → 用工具二即可
- 需要做特定的資料編輯操作 → 用工具一

---

## 執行方式

```bash
python xmind_organize_run.py <input.xmind> [output_path]
```

執行後會詢問：
```
輸出格式？
  1. Canvas (.canvas)
  2. Xmind  (.xmind)
選擇 [1/2，預設 1]：
```

**Canvas**：整理後轉成 Obsidian Canvas，適合視覺化瀏覽  
**Xmind**：整理後寫成新的 .xmind 檔，適合繼續在 Xmind 編輯

---

## AI 整理規則

AI 整理時遵守 `schema/(Prompt) Xmind資訊整理Prompt規格.md`，主要行為：

- 同語意節點合併、語意過廣節點拆分
- 重新整理層次，讓父子關係更清晰
- 缺少說明的節點補充備註（note）
- 保留所有原始資訊，不刪除內容

---

## 輸出說明

### Canvas 輸出
- 排版由 `xmind_to_canvas.py` 控制，參數設定見 context.md 的 B 區塊
- 適合「整體瀏覽」，不適合繼續編輯

### Xmind 輸出
- 工作表名稱為「{原始根節點}（整理版）」
- 保留 note 備註
- 可以用 Xmind 開啟繼續編輯

---

## LLM 設定

目前預設使用 Anthropic Claude（`ANTHROPIC_API_KEY` 環境變數）。  
若需要抽換，修改 `xmind_organizer.py` 的 `LLMClient` 類別：

```python
# 目前支援
client = LLMClient(provider="anthropic")

# 未來擴充點（在 LLMClient._call_xxx 新增對應方法）
# client = LLMClient(provider="openai", model="gpt-4o")
```

---

## 迭代調整

整理結果不滿意時的調整流程：

1. 修改 `schema/(Prompt) Xmind資訊整理Prompt規格.md`（改 AI 行為）
2. 重新執行，比較新舊輸出
3. 若是特定節點結構問題，可先用工具一手動調整再送給 AI
