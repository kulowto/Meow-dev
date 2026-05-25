# Meow-Dev 工作上下文
更新時間：2026-05-26 00:10

---

## ▌作業區塊 A：PS 工具開發 Pipeline（影片轉工具）
> 流程：影片 → MEMO.AI 轉錄 → 步驟萃取 → 工具規格草稿 → 實機驗證 → 實作

### 各影片 Phase 進度

- **Video 1（路面積水效果）**：Phase 3 完成，等使用者實機驗證後進行 Phase 4 確認
- **Video 3（素描效果）**：Phase 3 完成，步驟 3「減淡工具」辨識存疑待確認，等 Phase 4
- **Video 4（絲網印刷效果）**：Phase 4 完成，待 Phase 5 實作
- **Video 5（矩形漸變構圖）**：Phase 4 完成
- **Video 6（AI 凌亂線條字）**：Phase 4 完成，軟體為 Illustrator，實作暫時跳過
- **Video 7（雙氛圍感光效）**：Phase 4 完成
- **Video 8（透明玻璃字）**：Phase 4 完成

### 下一步優先順序（A 區塊）
1. 使用者實機測試 Video 1 / 3（PS）→ 回報 Phase 4 修正
2. Video 4 進 Phase 5 實作
3. 修正 `ps_auto.py:86` 的 `chr_halfTone` 毒性操作

### A 區塊：障礙 / 注意事項
- 規範文件路徑：`架構Wiki與AI的協作環境/04_工具開發流程/`
- MEMO.AI 腳本：`C:/Users/AkatsukiNeko/AppData/Local/Temp/memo_batch_v2.py`
- `ps_auto.py` v0.6：Phase 1-3 全部跑通；`chr_halfTone` 尚未封裝

---

## ▌作業區塊 B：心智圖輔助工具（影片製作腳本化）

### 目前狀態
- 工具一~五 + CLI（xmind_organize_run.py）：✅ 全部完成
- ＢＤ２ 整理：產出 `BD2_organized.md`（桌面）

### 下一步優先順序（B 區塊）
1. 使用者閱讀 `BD2_organized.md`，討論格式 / 補充比對資訊
2. 修 boundary 第一子節點 BUG
3. 設計「AI 填入心智圖」workflow

### B 區塊：障礙 / 注意事項
- 工具腳本路徑：`active/workingData/Meow-Toolbox/Xmind/tools/`
- ⚠️ 已知 BUG：boundary 群組最上方子節點若有子節點，可能與群組框標籤重疊

---

## ▌作業區塊 C：inquiry_model 結構化詢問工具

> 工具定位：金字塔原理 × 分而治之 × 問題追蹤器

### 目前狀態：✅ v0.2 完成 + 周邊配置完成

**核心工具**
- Python CLI：`D:\Meow-Env\Meow-Dev\active\inquiry_model\`，執行 `python run.py`
- Demo 腳本：`_demo_run.py`（模擬輸入跑完整流程）

**Sessions 存放位置（已解耦）**
- `D:\Meow-Env\Meow-Dev\active\inquiry_sessions\`（工具搬至 Meow-Tools 後 sessions 仍留在 Meow-Dev）

**Claude Code 快速觸發**
- `/inquiry [主題]`：自訂指令，位於 `~/.claude/commands/inquiry.md`
- 不帶主題直接 `/inquiry` 也可，Claude 會先問主題

**主動觸發規則**
- 已加入 Meow-Agent CLAUDE.md：偵測到釐清問題/學習/決策/工作流程等意圖，主動建議使用 `/inquiry`

**思維框架文件**
- 工具版：`active/workingData/思維框架/`（8 份 AI_Read，供工具讀取）
- Wiki 備份：`Meow-Wiki/wiki/concepts/`（7 份 ref-*.md，reviewed: false 待人工確認）

### 下一步優先順序（C 區塊）
1. 用真實主題跑 `/inquiry` 或 `python run.py` 體驗看看
2. 工具穩定後搬至 `Meow-Tools`（只需改 `recorder.py` 工具本體路徑，sessions 路徑不動）
3. MW 裡的 7 份思維框架文件，有空時人工補充確認（reviewed: true）

### C 區塊：障礙 / 注意事項
- sessions 路徑使用絕對路徑（`D:/Meow-Env/Meow-Dev/active/inquiry_sessions`），搬家時須同步修改 `recorder.py`
- API：Groq（llama-3.3-70b-versatile），14,400 req/day 免費
