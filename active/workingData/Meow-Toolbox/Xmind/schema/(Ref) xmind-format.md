---
文件類型: Reference  版本: v0.1  建立: 2026-05-22
---

# .xmind 格式參考

## 檔案結構

`.xmind` 是 ZIP 壓縮檔，解壓後主要包含：

```
content.json       ← 主要資料（層次樹狀結構，現代版本）
metadata.json      ← 檔案 metadata（版本、作者等）
attachments/       ← 附件（若有）
res/               ← 資源檔（圖片等，若有）
```

> **注意**：舊版 Xmind（8 以前）使用 `content.xml`，現代版（2020+）使用 `content.json`。
> 本工具以 `content.json` 為主。

## content.json 結構

```json
[
  {
    "id": "root-sheet-id",
    "class": "sheet",
    "title": "工作表名稱",
    "rootTopic": {
      "id": "root-topic-id",
      "class": "topic",
      "title": "根節點標題",
      "children": {
        "attached": [
          {
            "id": "child-id",
            "class": "topic",
            "title": "子節點標題",
            "children": {
              "attached": [
                // 遞迴巢狀結構
              ]
            }
          }
        ]
      }
    }
  }
]
```

## 關鍵欄位說明

| 欄位 | 說明 |
|------|------|
| `id` | 節點唯一 ID（UUID 格式） |
| `class` | 固定為 `"topic"` |
| `title` | 節點顯示文字 |
| `children.attached` | 子節點陣列（主要分支） |
| `children.detached` | 浮動子節點（少用） |
| `note` | 節點備註（純文字） |
| `markers` | 標籤 / 圖示（陣列） |
| `branch` | 分支樣式（`"folded"` 表示折疊） |

## Python 讀取範例

```python
import zipfile, json

def read_xmind(path):
    with zipfile.ZipFile(path, 'r') as z:
        with z.open('content.json') as f:
            return json.load(f)

def write_xmind(path, data):
    import shutil, os, tempfile
    tmp = path + '.tmp'
    shutil.copy(path, tmp)
    with zipfile.ZipFile(tmp, 'a') as z:
        z.writestr('content.json', json.dumps(data, ensure_ascii=False, indent=2))
    os.replace(tmp, path)
```

> 完整讀寫邏輯見 `tools/xmind_reader.py`（待實作）
