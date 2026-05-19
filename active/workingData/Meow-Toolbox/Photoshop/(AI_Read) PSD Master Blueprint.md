---
type: blueprint
scope: Photoshop
version: v1.0
created: 2026-05-13
usage: 定義 PSD 圖層的 Zone 系統與排序規則，供 AI 在最終組合圖層順序時查閱
---

# PSD Master Blueprint

> **查閱時機**：只有在需要決定最終圖層排列順序時查閱一次。
> 單獨執行某個工具時不需要查閱此文件。
>
> **維護責任**：每新增一個工具文件（Tool），必須同步更新「已登記圖層清單」。

---

## Zone 系統

PSD 由上到下分為四個固定語義區域（Zone），Zone 之間的順序**不可更動**：

```
PSD（由上到下）
│
├── [Zone A] EFFECT_OVERLAY    ← 疊加在角色本體上的效果（Multiply 混合為主）
│                                 例：輪廓線提取、網點陰影
│
├── [Zone B] CHARACTER         ← 角色本體
│                                 例：src_main（去背主體）
│
├── [Zone C] EFFECT_UNDERLAY   ← 延伸到角色輪廓外的效果
│                                 例：白色外輪廓填色、黑色線條環
│
└── [Zone D] BACKGROUND        ← 底色與備份圖層
                                  例：background、chr_source（鎖定備份）
```

### Zone 語義說明

| Zone | 名稱 | 視覺語義 | 典型混合模式 |
|------|------|---------|------------|
| A | EFFECT_OVERLAY | 效果在角色「上方」，對角色本體進行疊加處理 | Multiply、Overlay |
| B | CHARACTER | 角色本體，去背後的主圖層 | Normal |
| C | EFFECT_UNDERLAY | 效果在角色「下方」，延伸至輪廓外 | Normal、Multiply |
| D | BACKGROUND | 底色、鎖定備份、純色背景 | Normal |

---

## 優先級規則

### 數字定義

- **數字越小 = 越靠近畫面上層（觀看者）**
- 每個 Zone 內部，各自從 `10` 起算，以 `10` 為間距遞增
- 預留間距是為了方便未來在兩個工具之間插入新工具

```
priority: 10  ← Zone 內最上層
priority: 20
priority: 30
  ...
priority: 90  ← Zone 內最下層（系統保留層如鎖定備份）
```

### 跨 Zone 排序邏輯

AI 組合多工具排序時，依序：

1. 先依 Zone（A → B → C → D）排列
2. 同一 Zone 內，依 priority 數字由小到大排列（小的在上）

---

## 已登記圖層清單

> 每新增工具文件時，必須在此表格補充對應圖層的登記資訊。

| 圖層名稱 | 所屬群組 | Zone | Priority | 混合模式 | 鎖定 | 來源工具 |
|---------|---------|------|----------|---------|------|---------|
| `chr_contourLine` | `chr_effects` | A - EFFECT_OVERLAY | 10 | Multiply | 否 | Phase 3 - contourLine |
| `chr_halfTone` | `chr_effects` | A - EFFECT_OVERLAY | 20 | Multiply | 否 | Phase 3 - halfTone |
| `src_main` | `original` | B - CHARACTER | 10 | Normal | 否 | PART B |
| `chr_outLine` | `chr_effects` | C - EFFECT_UNDERLAY | 10 | Normal | 否 | Phase 3 - outLine |
| `chr_outerLine` | `chr_effects` | C - EFFECT_UNDERLAY | 20 | Multiply | 否 | Phase 3 - outerLine |
| `src_background` | `original` | D - BACKGROUND | 10 | Normal | 否 | Phase 2 |
| `src_img` | `original` | D - BACKGROUND | 90 | Normal | ✅ | Phase 2 |

---

## 群組結構

圖層會依功能歸入對應群組，群組本身也有固定的 PSD 排列順序：

```
PSD（由上到下）
├── [群組] chr_effects      ← 所有特效圖層（Zone A + C）
└── [群組] original 🔒     ← 角色本體與備份（Zone B + D）
```

> **設計說明**：Zone A 和 Zone C 的圖層目前都放在 `chr_effects` 群組內，
> 依 Zone + priority 決定群組內部的上下順序。
> 未來若需要分開管理，可拆為 `chr_effects_overlay` 和 `chr_effects_underlay` 兩個群組。

---

## 新增工具的流程

當一個新工具需要登記時：

1. 確認工具輸出的圖層屬於哪個 Zone（依視覺語義判斷）
2. 查閱上方清單，確認該 Zone 內已有哪些 priority 數字被占用
3. 選擇一個未被占用的 priority（若需插入現有兩個工具之間，取其中間值）
4. 在工具文件的「圖層區域與優先級」欄位填入 Zone 和 priority
5. 在本文件的「已登記圖層清單」補上該圖層的登記資訊

---

## 版本記錄

| 版本 | 日期 | 變更說明 |
|------|------|---------|
| v1.0 | 2026-05-13 | 初始建立，定義四個 Zone，登記 Phase 1–3 全部圖層 |
| v1.1 | 2026-05-14 | 修正 Zone D 圖層命名：background→src_background，chr_source→src_img（對齊 v0.5 程式碼） |
| v1.2 | 2026-05-14 | Zone B 圖層命名：chr_main→src_main（對齊 PART A/B/C 新架構） |
