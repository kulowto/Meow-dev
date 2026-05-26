# ConardLi 開源工具調查報告

> 整理日期：2026-05-26 17:25
> 調查目的：安裝前的安全性審查 + 項目全覽

---

## 作者資訊

| 項目 | 內容 |
|------|------|
| GitHub | [ConardLi](https://github.com/ConardLi) |
| YouTube 頻道 | [code秘密花園](https://www.youtube.com/@garden-conard) |
| 背景 | 中國大陸開發者，專注 Claude Code / AI Agent 工具開發 |
| 主要語言 | TypeScript，提供中英文文件 |

---

## 影片摘要

### 影片一：把 Claude Design 做成 Skill，人人都能用
- **上傳日期**：2026-04-22
- **長度**：12:58 ／ **觀看數**：約 9,400
- **核心內容**：介紹如何把 Anthropic 的 Claude Design 系統提示做成 `web-design-engineer` Skill，讓 Cursor、Codex、Claude Code 等 AI 工具都能生成高品質網頁，而不只是廉價的漸層發光效果
- **對應資源**：`garden-skills` 的 `web-design-engineer` Skill

### 影片二：Harness 實踐 — 讓 Agent 全自動製作知識講解視頻
- **上傳日期**：2026-05-08
- **長度**：23:21 ／ **觀看數**：約 31,800（點讚 1,289）
- **核心內容**：展示如何用 Claude Code 的 Harness 機制（Hooks + 流程自動化）搭配 `web-video-presentation` Skill + MiniMax CLI 語音合成，讓 Agent 從腳本到影片全程自動化
- **工具清單**：
  - `garden-skills`（Skill）
  - [MiniMax CLI](https://github.com/MiniMax-AI/cli)（TTS 語音合成）
  - [CC Switch](https://github.com/farion1231/cc-switch)（Claude 帳號切換工具）

---

## Repo ① garden-skills

> **這是你最可能想安裝的核心 Repo**

- **連結**：https://github.com/ConardLi/garden-skills
- **Stars**：⭐ 6,100 ／ Forks：865
- **License**：MIT
- **定位**：為 Claude Code、Cursor、Codex、Gemini CLI 等 AI 工具提供的 Skill 套件集合

### 包含的 4 個 Skill

| Skill 名稱 | 類型 | 最適合用來做 |
|-----------|------|------------|
| `web-video-presentation` | 網頁影片 / 簡報 | 把文章、教程、講稿轉成 1920×1080 可螢幕錄製的 Vite+React+TS 簡報，含 23 套內建主題，支援 TTS 語音合成 |
| `web-design-engineer` | 設計 / 前端 | 生成有設計感的網頁（Landing page、Dashboard、互動原型），包含 6 個設計流派 + 25 種風格配方，避開 AI 常見的廉價 UI 模板 |
| `gpt-image-2` | 圖片生成 | 使用 GPT-Image-2 生成海報、UI 原型、資訊圖表，內建 80+ 提示模板 |
| `kb-retriever` | 知識庫檢索 | 從本地 `knowledge/` 目錄精準搜尋 Markdown / PDF / Excel，不一次把整個文件塞進 context |

### 安裝方式（Claude Code 最簡單）

```bash
# 安裝全部 4 個
/plugin marketplace add ConardLi/garden-skills
/plugin install web-design-skills@garden-skills
/plugin install presentation-skills@garden-skills
/plugin install knowledge-base-skills@garden-skills
/plugin install image-generation-skills@garden-skills

# 或用 npx 挑選
npx skills add ConardLi/garden-skills -s web-design-engineer
```

---

## Repo ② easy-agent

- **連結**：https://github.com/ConardLi/easy-agent
- **Stars**：⭐ 726 ／ Forks：96
- **License**：MIT
- **定位**：**不是 Skill，是整個系統** — 從零用 TypeScript 重建 Claude Code 完整架構的開源教育專案

### 這是什麼

不是拿來「安裝使用」，而是拿來「學習 Claude Code 如何運作」的教學 Repo。
用 31 個階段（Step file）逐步還原 Claude Code 的核心機制，目前完成 Stage 21。

### 已實作的功能

| Phase | 功能 |
|-------|------|
| 1–5 | LLM 通訊層、Terminal UI、工具介面、核心 Agent 迴圈、完整工具集 |
| 6–10 | System Prompt、權限控制、多輪 Orchestration、Session 持久化、記憶系統 |
| 11–15 | Context 壓縮、Token 預算管理、計畫模式、任務追蹤 |
| 16–21 | MCP 協定、Skills 系統、Sandbox、Sub-Agent、背景代理 + Git Worktree 隔離、Agent Teams |
| 22–31 | Hooks 生命週期（下一步）、管道模式、多 Provider 支援（規劃中）|

### 使用情境

- 想深入理解 Claude Code 底層架構 → 讀 `step/` 下的里程碑檔案
- 想自己做一個 AI Coding Agent → 可以作為參考架構

---

## Repo ③ claude-code-source-code

- **連結**：https://github.com/ConardLi/claude-code-source-code
- **Stars**：⭐ 7 ／ Forks：10
- **定位**：Claude Code v2.1.88 反編譯源碼 + 深度分析報告
- **Fork 自**：`sanbuphy/learn-coding-agent`（上游更活躍）

### 這是什麼

從 npm 套件 `@anthropic-ai/claude-code 2.1.88` 提取反編譯的 TypeScript 源碼，加上 5 份分析報告（四語言版本）。

### 分析報告主題

| # | 主題 | 重要發現 |
|---|------|---------|
| 01 | 遙測與隱私 | 有兩個分析後端（Anthropic + Datadog），無法從 UI 關閉第一方日誌；`OTEL_LOG_TOOL_DETAILS=1` 會捕捉完整工具輸入 |
| 02 | 隱藏功能與代號 | 動物代號系統（Capybara / Tengu / Fennec / **Numbat**），Feature flag 用隨機詞對混淆用途 |
| 03 | Undercover 模式 | Anthropic 員工在公開 repo 貢獻時自動進入潛伏模式，AI 被指示「不要暴露身份」，以人類開發者身份 commit |
| 04 | 遠端控制 | 每小時 polling `API/claude_code/settings`，6 個以上 killswitch，GrowthBook flag 可遠端改變用戶行為；拒絕某些危險變更會導致 App 強制退出 |
| 05 | 未來路線圖 | **KAIROS** 全自動代理模式（帶 `<tick>` 心跳）、語音模式（push-to-talk 已就緒但被 gate 住）、17 個未上線工具 |

### ⚠️ 法律注意

- 源碼版權屬 Anthropic，Repo 有明確免責聲明「僅供技術研究和教育目的，嚴格禁止商業使用」
- 屬於逆向工程的灰色地帶，不建議在商業專案中使用
- 這個 Repo 適合**閱讀學習**，不適合「安裝使用」

---

## 安全性總結

### garden-skills
| 項目 | 狀態 |
|------|------|
| 授權 | ✅ MIT |
| 社群認可 | ✅ 6.1k stars，865 forks |
| 來源透明 | ✅ 引用 Anthropic 官方 Agent Skills spec，致謝說明清楚 |
| 程式碼類型 | ✅ 純 SKILL.md 文件（Markdown + YAML frontmatter），不是可執行程式碼 |
| 完整性驗證 | ✅ 提供 SHA-256 checksum 供驗證 |
| 相容性 | ✅ Claude Code / Cursor / Codex / Gemini CLI 均已測試 |
| 更新頻率 | ✅ 非常活躍（5 hours ago 仍有更新） |
| 風險提醒 | ⚠️ Repo 建立只有一個月（2026-04），相對新 |

**結論：可以安裝，風險低。**

### easy-agent
| 項目 | 狀態 |
|------|------|
| 授權 | ✅ MIT |
| 程式碼類型 | ✅ TypeScript，可審查 |
| 目的 | ✅ 教育性質明確 |
| API 使用 | ⚠️ 需要自己提供 Anthropic API key |
| 完成度 | ⚠️ 正在開發中，不是成品 |

**結論：適合學習研究，不需要「安裝」。**

### claude-code-source-code
| 項目 | 狀態 |
|------|------|
| 授權 | ❌ 使用 Anthropic 版權材料（灰色地帶） |
| 目的 | ⚠️ 純研究閱讀 |
| stars | ⚠️ 只有 7 stars，小眾 |

**結論：僅供閱讀學習，不安裝。**

---

## 給你的建議

根據你的使用需求（「實用層面基本都會用到」），以下優先度排序：

| 優先度 | Skill | 理由 |
|-------|-------|------|
| ⭐⭐⭐ | `web-design-engineer` | 直接提升 AI 生成網頁的視覺品質，使用頻率高 |
| ⭐⭐⭐ | `web-video-presentation` | 如果有製作影片或簡報需求，這個整合度很高 |
| ⭐⭐ | `kb-retriever` | 有本地知識庫查詢需求時再裝，避免 context 膨脹 |
| ⭐ | `gpt-image-2` | 需要用 GPT-Image-2 才有意義，依使用習慣決定 |
