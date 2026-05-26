# Meow-Dev 工作上下文
更新時間：2026-05-27 00:00

---

## ▌作業區塊 A：PS 工具開發 Pipeline（影片轉工具）
> 流程：影片 → MEMO.AI 轉錄 → 步驟萃取 → 工具規格草稿 → 實機驗證 → 實作

### 各影片 Phase 進度

- **Video 1（路面積水效果）**：Phase 3 完成，等使用者實機驗證後進行 Phase 4 確認
  規格草稿：`架構Wiki.../04_工具開發流程/(AI_Read) 工具規格草稿_Video1_路面积水效果.md`
- **Video 3（素描效果）**：Phase 3 完成，步驟 3「減淡工具」辨識存疑待確認，等 Phase 4
  規格草稿：`架構Wiki.../04_工具開發流程/(AI_Read) 工具規格草稿_Video3_素描效果.md`
- **Video 4（絲網印刷效果）**：Phase 4 完成，待 Phase 5 實作
- **Video 5（矩形漸變構圖）**：Phase 4 完成
- **Video 6（AI 凌亂線條字）**：Phase 4 完成，軟體為 Illustrator，實作暫時跳過
- **Video 7（雙氛圍感光效）**：Phase 4 完成（2026-05-21）
- **Video 8（透明玻璃字）**：Phase 4 完成（2026-05-21）

### 下一步優先順序（A 區塊）
1. 使用者實機測試 Video 1 / 3（PS）→ 回報 Phase 4 修正
2. Video 4 進 Phase 5 實作
3. 修正 `ps_auto.py:86` 的 `chr_halfTone` 毒性操作（`chr_layer.duplicate()` → `_duplicate_active_layer()`）

### A 區塊：障礙 / 注意事項

**規範文件體系（2026-05-21 建立）**

| 文件 | 層次 | 用途 |
|------|------|------|
| 開發理念_流程設計與資訊濾網模型 | 元層次 | 濾網概念、上下游雙向規範，給未來 AI 讀的 |
| 影片轉工具開發流程規範（v0.3） | 粗濾網 | Phase 1-5 流程規則，新增步驟 0 / 最後步驟 / 可調參數格式規範 |
| 語音辨識錯誤紀錄_Debug | 細濾網 | V1-V8 已知語音辨識錯誤分類紀錄，Phase 3 二次優化用 |
| PS工具架構設計規範（v0.2） | 下游 | 補入上游對接說明 + 規格草稿欄位對程式碼的對應表 |

- 規範文件路徑：`架構Wiki與AI的協作環境/04_工具開發流程/`
- 粗濾網（流程規範）與細濾網（Debug 紀錄）不並用，先粗後細

**MEMO.AI 自動化操作方式**
- 用 CDP Python 腳本（WebSocket 連 `localhost:9222`）控制 MEMO.AI 桌面應用
- 關鍵腳本：`C:/Users/AkatsukiNeko/AppData/Local/Temp/memo_batch_v2.py`
- ⚠️ 確認轉錄前必須設定：模型選「高品質-Medium」、GPU 加速開啟、自動斷句開啟

**工具開發現況**
- `ps_auto.py` v0.6：Phase 1（去背）+ Phase 2（圖層結構）+ Phase 3（四個特效）全部跑通
- `chr_halfTone` 尚未封裝，且 `ps_auto.py:86` 仍用 `chr_layer.duplicate()` 毒性操作（TODO 標記存在）
- 已封裝工具：`source_separation.py` / `contour_line.py` / `outline_border.py`

**關鍵文件路徑**
- 流程規範：`架構Wiki.../04_工具開發流程/(AI_Read) 影片轉工具開發流程規範.md`
- 工具架構規範：`架構Wiki.../04_工具開發流程/(AI_Read) PS工具架構設計規範（通用版）.md`
- 工具文件骨架：`Meow-Toolbox/_schema/(Template) PS工具文件骨架.md`

---

## ▌作業區塊 B：心智圖輔助工具（影片製作腳本化）
> 流程：心智圖（Xmind）→ AI 爬現有檔案 → 填入對應區塊 → 整理文案邏輯 → 輸出影片腳本草稿

### 目前狀態
- 工具一（`xmind_reader.py`）：✅ 完成
- 工具二（`xmind_to_canvas.py`）：✅ 完成，有已知 BUG 待修（見障礙區）
- 工具三（`xmind_organizer.py`）：✅ 完成，AI 語意整理，可抽換 LLM provider
- 工具四（`xmind_writer.py`）：✅ 完成，標準化 JSON → .xmind，支援 boundaries
- 工具五（`xmind_to_md.py`）：✅ 完成，Xmind / JSON → MD，含 boundaries 彙整表
- CLI（`xmind_organize_run.py`）：✅ 完成
- ＢＤ２ 整理：產出 `BD2_organized.md`（桌面），暫存 `bd2_organized.json`（桌面）

### 下一步優先順序（B 區塊）
1. 使用者閱讀 `BD2_organized.md`，討論如何進一步調整格式 / 補充比對資訊
2. 修 boundary 第一子節點 BUG（詳見障礙區）
3. 設計「AI 填入心智圖」workflow

### B 區塊：排版參數現況（xmind_to_canvas.py）

| 參數 | 值 | 說明 |
|------|----|------|
| NODE_W_MIN | 260 | 節點最小寬度 |
| NODE_H | 60 | 節點最小高度 |
| CHARS_PER_LINE | 15 | 每行估算字數（CJK） |
| CHAR_W | 14 | CJK 字元估算寬度（px） |
| LINE_H | 22 | 每行文字高度（px） |
| H_GAP_WIDE | 240 | boundary 層以上水平間距（parent 右邊到 child 左邊） |
| H_GAP_NARROW | 140 | 深層或無 boundary 水平間距 |
| V_GAP | 40 | 同層節點垂直間距 |
| SECTION_GAP | 192 | L1 區塊間額外間距 |
| GROUP_PAD_X | 16 | group box 水平內縮 |
| GROUP_PAD_Y | 8 | group box 垂直內縮 |
| GROUP_MARGIN | 120 | group box 外部間距（baked 進排版） |
| NEST_PAD | 14 | 巢狀 group 最小超出距離 |

### B 區塊：障礙 / 注意事項
- **GROUP_MARGIN 實作重點**：加在 `_children_span` 的首尾 + `_layout` 的 cur_y 起點，才能往上傳給 grandparent 的 subtree height，空間真正留出來
- boundary range `(0, n-1)` 覆蓋全部子節點時，舊做法（只加中間間隔）無效，需首尾都加
- **⚠️ 已知 BUG（待修）**：boundary 群組最上方的子節點若有自己的子節點，子節點內容可能與群組框標籤或上方節點重疊。
  - 已嘗試：在 `_children_span` 和 `_layout` 的 GROUP_MARGIN 之後額外加 V_GAP（當 `children[0]` 有子節點時），但效果不足，問題尚未完全解決。
  - 根本原因：當 span > nh 時，第一個子節點的子節點從 `cur_y`（allocation 頂端）開始，group box 上緣僅 GROUP_PAD_Y=8 的間距，群組標籤與內容重疊。
  - 下次修法方向：考慮增大 GROUP_PAD_Y，或在 `_build_groups` 的 `min_y` 計算時額外減去 V_GAP。
- **投資方法.xmind 正確路徑**：`I:\Obsidian Note\Obsidan-Notes-Merge-Version\_Storing Books\_Investment\_How to investment\投資方法.xmind`（不在 Fleeting Note 目錄）
- 工具腳本路徑：`active/workingData/Meow-Toolbox/Xmind/tools/`
- 測試輸出路徑：桌面（`C:\Users\AkatsukiNeko\Desktop\`）
- 尤里教聯合體系 xmind 路徑有**雙空格**：`尤里教聯合體系  (Yuri United).xmind`

---

## ▌作業區塊 C：inquiry_model 結構化詢問工具

> 工具定位：金字塔原理 × 分而治之 × 問題追蹤器，用於釐清方向、探索問題、沉澱洞見

### 目前狀態：✅ v0.2 完成 + 解耦合重構完成（2026-05-26）

**核心工具**
- Python CLI：`D:\Meow-Env\Meow-Dev\active\inquiry_model\`，執行 `python run.py`
- Demo 腳本：`_demo_run.py`（傳入 `input_fn=_mock_input` 跑完整流程，不再 monkey-patch）

**Sessions 存放位置（已解耦）**
- `D:\Meow-Env\Meow-Dev\active\inquiry_sessions\`（工具搬至 Meow-Tools 後 sessions 仍留在 Meow-Dev）

**Claude Code 快速觸發**
- `/inquiry [主題]`：自訂指令，位於 `~/.claude/commands/inquiry.md`
- 不帶主題直接 `/inquiry` 也可，Claude 會先問主題

**主動觸發規則**
- 已加入 Meow-Agent CLAUDE.md：偵測到釐清問題 / 學習 / 決策 / 工作流程等意圖，主動建議使用 `/inquiry`

**workingData 思維框架文件（`active/workingData/思維框架/`）**
- 工具版（AI_Read）：9 份，供 inquiry_model 讀取
- Wiki 備份：7 份 `ref-*.md` 已存入 `Meow-Wiki/wiki/concepts/`，`reviewed: false` 待人工確認

**架構（解耦合後）**
```
inquiry_model/
  run.py / _test_pipeline.py / _demo_run.py
  core/
    llm.py            # API 層（換 provider 只改這裡）
    decomposer.py     # 主題拆解
    questioner.py     # 支柱詢問（input_fn 注入，I/O 與邏輯分離）
    synthesizer.py    # 彙整輸出（含 session→prompt 轉換，不再依賴 pyramid）
    reality_checker.py # Reality Check LLM 呼叫（從 run.py 抽出）
    recorder.py       # session 結構與存檔
    json_utils.py     # 穩健 JSON 解析
  frameworks/
    pyramid.py        # 純 prompt 字串（不含任何業務邏輯）
  .env  (GROQ_API_KEY)
```

### 下一步優先順序（C 區塊）
1. 用真實主題跑 `/inquiry` 或 `python run.py`
2. 工具穩定後搬至 `Meow-Tools`（只需改 `recorder.py` 的 sessions 絕對路徑）
3. MW 那 7 份思維框架文件，有空時人工補充確認（`reviewed: true`）

### C 區塊：障礙 / 注意事項
- sessions 使用絕對路徑（`D:/Meow-Env/Meow-Dev/active/inquiry_sessions`），工具搬家時須同步修改 `recorder.py`
- API：Groq（llama-3.3-70b-versatile），14,400 req/day 免費
- LLM 回應常包在 ```json...``` 內 → `json_utils.py` 多重 fallback 解決

---

## ▌作業區塊 D：外部工具研究 — ConardLi / garden-skills（2026-05-27）

> 本次完成了 ConardLi 的 garden-skills repo 全面調查 + 深度技術拆解

### 已完成

- 建立調查報告（安全性 + 項目全覽）：
  `active/workingData/外部工具研究/ConardLi_garden-skills 調查報告.md`
- 建立深度拆解文件（工程規劃用，含所有 reference 文件展開版）：
  `active/workingData/外部工具研究/ConardLi_garden-skills_深度拆解.md`
- 更新 `active/workingData/MENU.md`，補登兩份文件

### ⭐ 下次請先閱讀

1. **調查報告**（決定是否安裝、裝哪幾個）：
   `active/workingData/外部工具研究/ConardLi_garden-skills 調查報告.md`

2. **深度拆解**（工程規劃 + 可採納機制參考）：
   `active/workingData/外部工具研究/ConardLi_garden-skills_深度拆解.md`
   - Section 1：web-design-engineer（七步流程 / 六大學派 / 25 個食譜 / Anti-Cliché / oklch / 代碼規範）
   - Section 2：web-video-presentation（章節鐵律 / CHAPTER-CRAFT / TTS / 23 主題）
   - Section 3：kb-retriever
   - Section 5：Reference 展開版（advanced-patterns / critique-guide / gpt-image-2 模板方法論）

### D 區塊：障礙 / 注意事項
- `dist/prompt/claude-design-system-prompt.md` 目前 404（已從 repo 移除），需要原版 prompt 時另外搜尋
- 安裝決策建議：`web-design-engineer` 現在就裝、`web-video-presentation` 有影片需求就裝、其他兩個暫緩
