# Meow-Dev 工作上下文
更新時間：2026-10-28 00:00

## 當前任務
遊戲腳本開發 — 星塔旅人台服適配。已完成 MaaStellaSora v1.8.0 安裝，準備逐一測試台服（台港澳）各功能，確認哪些 pipeline 需要補修。

## 已完成
- 【遊戲腳本環境建立】建立目錄 `D:\Meow-Env\Meow-Dev\遊戲腳本\星塔旅人\`，安裝 MaaStellaSora v1.8.0（Windows x86_64），並建立 `SOURCE.md`（含 GitHub 連結、版本紀錄、台服已知問題追蹤表）
- 【技術調查】確認 tw 包覆蓋模式：載入順序為 `base（簡中）` → 疊加 `tw（台服）`；tw 包已覆蓋 login/friend/shop/quest/task/grant/talk，但缺少 `mail.json`（領取郵件）與 `tyrants_tower.json`（魔王之塔）的繁中覆蓋
- 【LeetCode 刷題 — 累積進度】共 34 題（1_TwoSum ～ 34_CourseSchedule），含完整解題記錄與語法概念卡；26 題起全部推送至 GitHub，1～25 題、概念卡等早期內容與 Skill v1.3 均已在 2026-08-11 前後推送完畢

## 待續事項
- **【優先】** 開啟 `MaaStellaSora\MFAAvalonia.exe`（管理員執行），選「台服」+「桌面端」，逐一測試各功能並回報結果，依 `SOURCE.md` 追蹤表更新狀態
- 測試後若有功能卡住，從 tw 包 pipeline 定點修補（已知高風險：`mail.json`、`tyrants_tower.json`）
- LeetCode 刷題：下次繼續時直接呼叫 `/leetcode-tutor`，Skill 會自動讀取規範文件並接續流程（目前 34 題，無未推送變更）

## 本次參考的文件
（暫態，下次更新清空）

## 嘗試過的路徑（含錯誤與結論）
（暫態，下次更新清空）

## 障礙 / 注意事項
- MaaStellaSora 台服注意：安裝路徑 `D:\Meow-Env\Meow-Dev\遊戲腳本\星塔旅人\MaaStellaSora\`，需以**管理員權限**執行 `MFAAvalonia.exe`
- tw 包技術細節：OCR 辨識文字需繁體中文，App 套件名台服為 `com.Stargazer.StellaSora`（與官服 `com.RoamingStar.StellaSora` 不同）
- 灾变防線功能明確標示「只支援官服 Windows 前台」，台服不需測試此功能
- LeetCode 使用者「過」判定標準嚴格，規範在 `active/workingData/専案/轉職程式設計師_三個月計畫/(AI_Read) 刷題詳細記錄使用規範.md`
