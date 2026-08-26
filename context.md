# Meow-Dev 工作上下文
更新時間：2026-08-27 07:02

## 當前任務
陪使用者用 `/leetcode-tutor` Skill 刷 LeetCode（C++），一題一題走「確認題意→虛擬碼→語法→收尾」四階段流程，每題記錄進 `active/workingData/専案/轉職程式設計師_三個月計畫/`。目前累積 17 題，因對話 context 用量已到 68%，先做一次存檔記錄，等等清 context。

## 已完成
- `刷題詳細記錄/` 已累積 17 題（1_TwoSum ~ 17_LongestPalindrome），每題都有完整的解題過程、三維度審查（語法/複雜度/演算法盲點）
- `語法概念卡/` 已建立 14 張卡：`unordered_map`、`map`、`red_black_tree`、`binary_search`、`linked_list`、`stack`、`order_vs_value`、`grid_traversal`、`recursion`、`floyd_cycle`、`class_basics`、`dynamic_programming`、`container_selection`，全部用 `<details>` 自問自答格式，互相有交叉連結
- `跨題目盲點彙總.md` 持續追蹤反覆出現的弱點，目前最主要的兩個：
  1. **迴圈/遞迴狀態變數管理**（該更新沒更新、該固定卻重算、該共用卻宣告成會重置的區域變數）——已出現 5 次，是目前排名第一的弱點
  2. **二分法 `mid` 忘記加 `head` 偏移量**——已出現 2 次（Binary Search、First Bad Version）
  3. **`pair` 跟「多筆資料容器」搞混**——已出現 2 次（Ransom Note、Climbing Stairs）
  4. **指標跟參考混淆**——已出現 2 次
  5. **跨語言命名習慣打字錯誤**（C#/JS 習慣帶進 C++）——反覆出現
- 已建立並迭代 `leetcode-tutor` Skill（`MA/skills/CodeTutor/leetcode-tutor/`，目前 v1.3，已安裝至 `~/.claude/commands/leetcode-tutor.md`）：四階段流程、A/B/C 教學分類（邏輯類引導不給答案／語法類直接教／打字錯誤直接指出）、收尾檢查清單、每 3 題確認是否結束、每 5 題批次自我更新（已執行 2 次，都判定不需調整，維持 v1.3）
- 2026-08-11：Meow-Dev、Meow-agent 兩個 repo 都已 commit + push 過一次（12 題記錄 + Skill v1.3），之後新增的 5～17 題記錄跟概念卡**尚未 push**

## 待續事項
- 繼續刷題：下次開新 session，先呼叫 `/leetcode-tutor`，Skill 會自動讀取 `(AI_Read) 刷題詳細記錄使用規範.md` 跟跨題目盲點彙總，接續原本流程
- 累積題數滿 22 題時，Skill 會主動提出下一次批次更新確認
- **有未推送的變更**：`刷題詳細記錄/13~17` 五題、`語法概念卡/class_basics.md`、`dynamic_programming.md`、`container_selection.md`（新增）+ 其他卡片的更新內容，以及 `跨題目盲點彙總.md` 的更新，都還沒 commit/push 到 GitHub（`kulowto/Meow-dev`）——下次使用者要求「更新上 GitHub」時記得處理這批
- 使用者目前最需要加強的兩個盲點：迴圈/遞迴狀態變數管理、二分法 mid 偏移量計算，未來出現類似情境時可以主動點出「這是你反覆卡住的地方」

## 本次參考的文件
（暫態，下次更新清空）

## 嘗試過的路徑（含錯誤與結論）
（暫態，下次更新清空）

## 障礙 / 注意事項
- 使用者的「過」判定標準很嚴格：只要過程中有靠 AI 討論/提示才想出思路或抓出 bug，就不算「限時內完成」，AI 要主動提醒、但最終尊重使用者自己的判斷（曾出現使用者堅持記為「限時內完成」的情況，AI 提醒後仍尊重其決定）
- 專案裡的完整流程規範在 `active/workingData/専案/轉職程式設計師_三個月計畫/(AI_Read) 刷題詳細記錄使用規範.md`，記錄格式、盲點登記標準都在那份文件，不要憑印象自己假設
- Skill 本身的教學行為邏輯在 `skill.md`（package 在 Meow-agent 那邊，不是 Meow-Dev），兩邊要分清楚：**記錄內容**在 Meow-Dev，**教學怎麼進行**在 Meow-agent 的 Skill
