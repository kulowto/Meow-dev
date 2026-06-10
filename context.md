# Meow-Dev 工作上下文
更新時間：2026-06-10 (更新：新增作業區塊 F)

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

## ▌作業區塊 E：oral-script Skill 開發

> 文字 → 口播稿轉換 Skill 群，三支 Skill 解耦合架構

### 架構決策（2026-06-08 確認）

採解耦合設計，拆為三支 Skill：

| Skill | 職責 | 指令 |
|-------|------|------|
| `oral-script-plan` | 內容 → 章節結構（Skill A） | `/oral-script-plan` |
| `oral-script-write` | 結構 + 補充資料 → 口播稿（Skill B） | `/oral-script-write` |
| `oral-script` | 快速模式，依序執行 A + B | `/oral-script` |

兩個 Skill 之間透過 **session.md** 傳遞狀態（interface contract）。

### Session 狀態檔格式（A → B 的介面契約）

```
D:/Meow-Env/Meow-Dev/active/oral-script/YYYYMMDD-[名稱]-session.md
```

內容：風格選擇 + 原始輸入內容 + 已確認章節架構 + 補充資料路徑（選填）

### 文件路徑

| 文件 | 路徑 |
|------|------|
| oral-script（快速模式） | `MA/skills/oral-script/` |
| oral-script-plan（Skill A） | `MA/skills/oral-script-plan/` |
| oral-script-write（Skill B） | `MA/skills/oral-script-write/` |
| 共用使用者偏好記憶 | `MA/skills/oral-script/user-prefs.md` |
| Session 輸出目錄 | `D:/Meow-Env/Meow-Dev/active/oral-script/` |

### 目前狀態（2026-06-08）

- ✅ 三支 Skill 全部實作完成（2026-06-08）
  - `oral-script-plan`：`MA/skills/oral-script-plan/` + `~/.claude/commands/`
  - `oral-script-write`：`MA/skills/oral-script-write/` + `~/.claude/commands/`
  - `oral-script`（快速模式）：`MA/skills/oral-script/` + `~/.claude/commands/` (v2.0)
- ✅ `skills-registry.md` 補錄三筆
- ✅ session.md 介面契約定義完成
- ⏳ **下一步**：用真實內容跑 `/oral-script-plan` 試跑，驗證流程與 session.md 格式

### 實作規格（給下個 AI）

**oral-script-plan/skill.md 職責**：
- Step 0：讀 `MA/skills/oral-script/user-prefs.md`
- Step 1：確認輸入（$ARGUMENTS 或詢問）
- Step 2：用 AskUserQuestion 問風格（四選一）
- Step 3：分析內容，輸出章節架構表，等確認
- Step 4：確認後儲存 session.md 至 `MD/active/oral-script/YYYYMMDD-[名]-session.md`
  - session.md 包含：風格、語速基準、原始輸入、確認架構、補充資料路徑（選填）
- 完成後告知使用者：「結構已儲存，執行 /oral-script-write 繼續生成口播稿」

**oral-script-write/skill.md 職責**：
- Step 0：讀最新 session.md（或請使用者指定）+ 讀 user-prefs.md
- Step 1：生成第一章節（含開場 Hook）→ 等確認（可多輪修改）
- Step 2：確認後 → 儲存 style-ref.md + 更新 user-prefs.md
- Step 3：一次生成所有後續章節（參照 style-ref + user-prefs）
- Step 4：驗證一致性 → 輸出完整稿 + 驗證報告
- 風格規則、TTS 標記、輸出格式從現有 oral-script/skill.md 複製

**oral-script/skill.md（快速模式）**：
- 直接執行 oral-script-plan 全部步驟（不停頓）
- 緊接執行 oral-script-write 全部步驟
- 唯一暫停點：Step 3 架構確認 + Step 4 第一章確認（與拆開版一致）

### E 區塊：障礙 / 注意事項
- TTS 標記格式：TTS 通用標記（平台無關），轉 MiniMax 或其他時另寫 converter
- session.md 是 A → B 的唯一介面，格式不能隨意改動，需要先改 spec 再改實作
- oral-script-write 讀 session.md 時，預設讀目錄內最新的一份（依日期排序），若有多份則詢問使用者

---

## ▌作業區塊 F：_pipeline_ComposeAssetsToVideo 系統規劃

> 影片內容製作流水線系統，把獨立能力模組串接成可驗證的影片產出流程

### 目前狀態（2026-06-10 更新）

- ✅ 工作目錄建立：`MD/workingData/専案/_pipeline_ComposeAssetsToVideo/`
- ✅ 討論記錄更新至 v0.2（含圖層驗證結論 + 群組問題記錄）
- ✅ HTML vs After Effects 分工邊界確認
- ✅ AI 圖層能力實作驗證完成（4 張參考圖）
- ⏳ **下一步**：研究如何串接 Figma API，讓 AI 能直接在 Figma 建立版型

### 核心架構決策（已確認）

1. **模組解耦**：各能力模組獨立存在，此專案只做索引 + 驗證
2. **半自動化**：關鍵節點人工審核，不全自動
3. **確認工作流**：圖片 → AI 分析圖層 → Figma 建立版型 → 使用者審核調整 → HTML 輸出
4. **HTML 先行**：現階段優先做 HTML 影片樣本，AE 後續階段

### HTML vs AE 分工（已確認）

| | HTML | After Effects |
|---|---|---|
| 適用類型 | 教學、資訊說明（PPT 式效果） | 精緻動畫、品牌影片 |
| 前置資訊 | 少（Figma 模板 + 口播稿） | 多（三視圖、分鏡、腳本） |
| 現階段 | ✅ 優先 | 後續階段 |

### AI 圖層能力驗證結論

- 圖層分離理解**基本正確**（除複雜照片合成外）
- **已知限制**：群組問題——AI 傾向把多行文字拆成獨立元素，而非單一文字框含換行
- 這是人工審核節點的主要工作項目之一
- 詳細記錄：`MD/workingData/専案/_pipeline_ComposeAssetsToVideo/討論記錄_v0.1.md`

### 下一步優先順序（F 區塊）

1. **研究 Figma API 串接**：AI 如何讀取圖片後在 Figma 建立正確的圖層與群組結構
2. 定義 HTML 影片樣板規格（第一個樣本）
3. 確認各功能模組的 home（`MA/skills/` vs `Meow-Tools/`）

### F 區塊：障礙 / 注意事項

- 群組問題：AI 輸出 Figma 時需要明確指定文字框結構，避免每行獨立
- 去背素材（透明 PNG）是上游步驟，Figma/PS 負責，HTML 只負責排版
- 各功能模組 home 尚未確定，建第一個模組時要先決定

