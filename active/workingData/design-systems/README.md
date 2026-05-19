---
type: index
last-updated: 2026-05-12
---

# Design Systems 索引

> 這個資料夾儲存所有設計系統。每個子資料夾對應一個品牌或客戶。
> AI 執行視覺相關任務時，先查此索引找到對應的設計系統，再讀取規則。

---

## 查找規則

1. 確認任務對應的品牌或客戶名稱
2. 進入對應資料夾，讀取 `MASTER.md`
3. 若有 `pages/<scene>.md`，該場景的規則優先於 MASTER

```
design-systems/
├── README.md              ← 你在這裡
├── _template/             ← 建立新設計系統時複製此資料夾
├── personal-brand/        ← 個人品牌（遊戲內容 / 社群視覺）
│   ├── MASTER.md
│   └── pages/
└── <client-name>/         ← 未來客戶專案
    ├── MASTER.md
    └── pages/
```

---

## 現有設計系統

| 品牌 / 客戶 | 資料夾 | 用途 | 狀態 |
|------------|-------|------|------|
| 個人品牌 | `personal-brand/` | 遊戲內容封面、社群貼文、影片縮圖 | ✅ v1.0 |

---

## 新增設計系統流程

1. 複製 `_template/` 資料夾，改名為客戶名稱
2. 用 ui-ux-pro-max skill 跑 `--design-system`，關鍵字帶入該客戶的風格定位
3. 依照產出填寫 `MASTER.md`
4. 視需要在 `pages/` 建立場景覆蓋檔案
