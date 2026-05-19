---
project: Personal Brand
type: design-system
version: v1.0
created: 2026-05-12
generator: ui-ux-pro-max skill
usage: gaming content / social media visuals / video thumbnails
---

# Personal Brand — Design System MASTER

> 這是個人品牌的全域設計系統，適用於影片封面、社群貼文、遊戲角色視覺。
> 新增客戶或專案時，在 `design-systems/<client-name>/` 建立對應的 MASTER.md。
> 需要針對特定頁面或情境覆蓋規則，建立 `pages/<scene>.md`。

---

## 使用情境說明

- 遊戲內容封面：大主美術圖 + 文字疊加 + 輔助元素拼貼
- 社群貼文視覺：角色主視覺 + 大量後製文字資訊
- 背景處理：大色塊 或 主圖模糊做底
- 角色主色彈性：基底為無色系，Accent 隨角色主色替換（見下方說明）

---

## Pattern

- **Name:** Editorial / Hero Content
- **Layout Logic:** 大主圖佔主視覺區，文字分層疊加，背景用色塊或模糊拉開層次
- **Color Strategy:** 無色系基底（黑白灰），Accent 跟隨角色主色動態替換
- **Whitespace:** 刻意留白，為後製文字資訊預留空間

---

## Style

- **Name:** Exaggerated Minimalism
- **Mode:** Dark 優先（見 Dark Mode 色票對照）
- **Keywords:** Bold minimalism, oversized typography, high contrast, negative space, loud minimal, statement design
- **Best For:** Gaming content, editorial, portfolio, character showcase
- **Performance:** Excellent | **Accessibility:** WCAG AA

---

## Colors（基礎色票 — 無色系基底）

> ⚠️ `--color-accent` 是變數，不固定為藍色。
> 使用時替換為當下角色的主題色（紅色角色 → 換紅、藍色角色 → 換藍）。
> 基底黑白灰不變，只有 Accent 跟隨角色主色。

### Light Mode（備用）

| Role | Hex | CSS Variable |
|------|-----|--------------|
| Primary | `#18181B` | `--color-primary` |
| On Primary | `#FFFFFF` | `--color-on-primary` |
| Secondary | `#3F3F46` | `--color-secondary` |
| **Accent/CTA** | **`[角色主色]`** | `--color-accent` |
| Background | `#FAFAFA` | `--color-background` |
| Foreground | `#09090B` | `--color-foreground` |
| Muted | `#E8ECF0` | `--color-muted` |
| Border | `#E4E4E7` | `--color-border` |

### Dark Mode（主要使用）

| Role | Hex | CSS Variable |
|------|-----|--------------|
| Primary | `#FAFAFA` | `--color-primary` |
| On Primary | `#09090B` | `--color-on-primary` |
| Secondary | `#A1A1AA` | `--color-secondary` |
| **Accent/CTA** | **`[角色主色]`** | `--color-accent` |
| Background | `#09090B` | `--color-background` |
| Surface | `#18181B` | `--color-surface` |
| Foreground | `#FAFAFA` | `--color-foreground` |
| Muted | `#27272A` | `--color-muted` |
| Border | `#3F3F46` | `--color-border` |

### Accent 範例替換表

| 角色主色 | 建議 Accent Hex | 說明 |
|---------|---------------|------|
| 紅色系 | `#DC2626` | 高飽和紅，在深色底上對比強 |
| 藍色系 | `#2563EB` | 標準藍，清晰明確 |
| 金/黃色系 | `#D97706` | 溫暖金黃，適合貴族/傳說角色 |
| 綠色系 | `#16A34A` | 自然系角色 |
| 紫色系 | `#7C3AED` | 魔法/神秘類型 |

---

## Typography

- **Heading:** Playfair Display（大標題、角色名稱）
- **Body:** Source Serif 4（說明文字、資訊標籤）
- **Mono:** JetBrains Mono（數值、屬性資訊）
- **Mood:** monochrome, editorial, austere, high contrast, luxury

### Font Scale

| 層次 | 用途 | 建議大小 |
|------|------|---------|
| Display | 角色名稱 / 主標題 | clamp(3rem, 10vw, 12rem) |
| Heading | 段落標題 / 章節名 | 2rem – 3rem |
| Body | 說明文字 | 1rem – 1.125rem |
| Label | 屬性標籤 / 數值 | 0.75rem – 0.875rem |

### Google Fonts 匯入

```css
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500&family=Playfair+Display:ital,wght@0,400;0,700;0,900;1,400&family=Source+Serif+4:ital,wght@0,300;0,400;0,600;1,300&display=swap');
```

---

## Key Effects

- 大標題：`font-weight: 900`、`letter-spacing: -0.05em`
- 留白：刻意大面積 negative space，為資訊文字預留落點
- 背景：大色塊 或 `backdrop-filter: blur(20px–40px)`
- 圖像層次：主視覺圖置頂，模糊背景在底層拉開景深

---

## 文字分層規則

> 背景 → 底層資訊 → 主圖 → 強調文字 → 主標題

| 層次 | 顏色 | 說明 |
|------|------|------|
| 背景 | `--color-background` 或模糊圖 | 最底層，純色或毛玻璃 |
| 輔助資訊 | `--color-secondary`（灰） | 不搶主視覺 |
| 主體資訊 | `--color-foreground`（白/黑） | 清晰可讀 |
| 強調 / CTA | `--color-accent`（角色主色） | 唯一彩色，引導視覺焦點 |

---

## Avoid（禁止事項）

- 彩色背景（會跟角色主色衝突）
- 多種顏色並用（只允許無色系基底 + 單一 Accent）
- 密集文字不留白
- 動畫過重（此用途以靜態為主）

---

## Pages 覆蓋規則

如需針對特定場景調整，在 `pages/` 建立對應檔案：

- `pages/youtube-thumbnail.md` — 封面縮圖的特定尺寸與比例規範
- `pages/instagram-post.md` — IG 方形 / 限動格式規範
- `pages/presentation.md` — 簡報 / 一圖流特定排版

> 查找規則：先找 `pages/<scene>.md`，有則優先套用；無則回到此 MASTER.md。
