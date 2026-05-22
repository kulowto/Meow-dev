---
文件類型: Reference  版本: v0.1  建立: 2026-05-22
---

# .canvas 格式參考（Obsidian Canvas）

## 檔案結構

`.canvas` 是純 JSON 文字檔，直接存於 Obsidian Vault 目錄下。

```json
{
  "nodes": [ ... ],
  "edges": [ ... ]
}
```

## nodes 節點格式

### 文字節點（最常用）

```json
{
  "id": "node-unique-id",
  "type": "text",
  "text": "節點顯示內容（支援 Markdown）",
  "x": -200,
  "y": -100,
  "width": 250,
  "height": 60,
  "color": "1"
}
```

### 檔案節點（連結 Obsidian 筆記）

```json
{
  "id": "node-unique-id",
  "type": "file",
  "file": "path/to/note.md",
  "x": 0,
  "y": 0,
  "width": 400,
  "height": 200
}
```

## edges 連線格式

```json
{
  "id": "edge-unique-id",
  "fromNode": "source-node-id",
  "fromSide": "right",
  "toNode": "target-node-id",
  "toSide": "left",
  "label": "選填：連線標籤"
}
```

### fromSide / toSide 可選值

`"top"` / `"bottom"` / `"left"` / `"right"`

## color 顏色對照

| 值 | 顏色 |
|----|------|
| `"1"` | 紅 |
| `"2"` | 橘 |
| `"3"` | 黃 |
| `"4"` | 綠 |
| `"5"` | 藍 |
| `"6"` | 紫 |
| 不填 | 預設（白 / 深色） |

## 轉換注意事項

- **座標原點**：Canvas 以 `(0, 0)` 為中心，正 X 往右，正 Y 往下
- **節點大小**：`width` 預設 250、`height` 依文字長度調整（最小 60）
- **AI 寫回限制**：Canvas 無自動排版，轉換腳本必須自行計算合理的 X/Y 座標
- **建議用途**：唯讀瀏覽 / 輸出給他人，不作為主力編輯格式

## 樹狀排版演算法（轉換用）

```
根節點 → (0, 0)
第一層子節點 → x = 300, y 依數量等距分佈
第二層子節點 → x = 600, y 繼承父節點區間再細分
...以此類推，每層 x 加 300
```

> 完整實作見 `tools/xmind_to_canvas.py`（待實作）
