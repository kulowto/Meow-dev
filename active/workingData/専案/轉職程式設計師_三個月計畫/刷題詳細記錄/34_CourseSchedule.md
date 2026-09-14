# 207 Course Schedule

- Key Cogitation：有向圖環偵測（DFS + 路徑集合 + 記憶化）
- Level：Medium
- 相關概念卡：[`語法概念卡/graph_cycle_detection.md`](../語法概念卡/graph_cycle_detection.md)、[`語法概念卡/recursion.md`](../語法概念卡/recursion.md)

> 同一題每次複習都在本檔案下方累加一段，不開新檔。用「跟上次相比」欄位追蹤盲點是否解決。

---

## 複習 #1 — 2026-09-14

- 狀態：有Bug
- 花費時間：120 分鐘

### 我的解法

```cpp
class Solution {
private:
    unordered_map<int, vector<int>> mp;
    unordered_set<int> cur;
    unordered_set<int> check_safe;

    bool hasCycle(int i){
        if(check_safe.find(i) != check_safe.end()){
            return false;
        }else{
            cur.insert(i);
        }

        for(int prq : mp[i]){
            if(cur.find(prq) != cur.end()){
                return true;
            }else{
                if(!hasCycle(prq)){
                    // 沒閉環，繼續看下一個
                }else{
                    return true;
                }
            }
        }
        check_safe.insert(i);
        cur.erase(i);
        return false;
    }

public:
    bool canFinish(int nC, vector<vector<int>>& pr) {
        for(auto p : pr){
            mp[p[0]].push_back(p[1]);
        }

        for(int i = 0; i < nC; i++){
            if(hasCycle(i)){
                return false;
            }
        }

        return true;
    }
};
```

- 時間複雜度：O(V+E)
- 空間複雜度：O(V+E)

### 解題過程

這題花費時間長，是目前記錄過除錯輪數最多的一題，過程中卡在同一個函式（`hasCycle`）連續好幾輪都冒新的結構性問題，最終改用「拆解成最小步驟」的方式才收斂。

#### 虛擬碼階段：容器選錯、狀態變數設計反覆修正

一開始想用 `unordered_map<int,int>`（一對一）記錄先修關係，經提問確認一門課可能有多個先修課，改成 `unordered_map<int,vector<int>>`。接著用單一 `int cur` 記錄「走過的值」，經提問確認需要的是「集合」不是單一數字，改成 `unordered_set<int> cur`。

邏輯設計本身也反覆修正：
1. 一開始想用兩個獨立的資料結構分開處理「建圖」跟「找環」，且 `cur` 從頭到尾只累加不清除。用菱形依賴例子（`0` 同時被 `1`、`2` 依賴，`3` 依賴 `1` 跟 `2`，沒有環）trace 出：`cur` 累加不清除會讓正常的共用依賴被誤判成環
2. 改成「處理完一個外層 `i` 才清空 `cur`」，用同一個菱形例子繼續 trace，問題還在——因為誤判發生在**同一個 `i`（`3`）的兩條分支（`1`、`2`）之間**，不是不同 `i` 之間

#### 程式碼階段：卡住多輪，改用「拆解成最小步驟」引導

`hasCycle` 這個函式的實作階段，連續好幾輪修改都是「修好上一輪指出的問題，同時在另一個地方引入新問題」（`tokens[s]` 型別誤用、`cur` 從未真正被 `insert`、`for` 迴圈裡提早 `return` 導致只檢查第一個先修課、`hasCycle` 回傳 `true` 沒有往上傳、`cur.erase()` 缺參數且位置錯、函式缺 `return false`）。主動要求換成「一步一步」引導，拆成：

1. 獨立寫「建圖」的迴圈（跟遞迴函式分開）
2. `hasCycle` 只寫「進入時的第一件事」（`cur.insert(i)`）
3. 只寫 `for` 迴圈裡「檢查 `prq` 在不在 `cur`」這一步
4. 只寫 `else` 分支（遞迴呼叫 + 判斷要不要往上傳 `true`）
5. 最後補迴圈外的 `cur.erase(i)` + `return false`

拆解後每步驟都個別確認，才寫出結構正確的版本。中途又踩到一次「迴圈裡沒問題的分支提早 `return false`」的回歸（把上一版正確的「沒問題就讓迴圈自然跑下一輪」改回「提早 return」），用同一個菱形例子再次驗證抓出來。

#### 送出後 Time Limit Exceeded，加記憶化優化

第一版邏輯正確但送出後超時——同一個節點會在不同外層 `i` 之間被重複完整探索。加上 `unordered_set<int> check_safe`，一個節點所有分支都探索完、確認安全時（跟 `cur.erase(i)` 同一時間點）標記進去，`hasCycle` 一開始先查這個集合，已確認安全就直接 `return false`，不重新展開子樹。加上這個優化後複雜度回到 O(V+E)。

### 1️⃣ 語法概念

- 型別選擇：一個節點有多個先修課時要用 `unordered_map<int, vector<int>>`（一對多），不是 `unordered_map<int,int>`
- 建圖（把輸入轉成鄰接表）應該獨立成一個迴圈，不要跟遞迴找環的邏輯混在同一個函式裡

### 2️⃣ 邏輯與複雜度

- 有 `check_safe` 記憶化：O(V+E) 時間、O(V+E) 空間；沒有的話最壞情況會嚴重超時
- **這是經典的三色標記 DFS 環偵測法的簡化版**：`cur` 對應「灰色（目前路徑上）」、`check_safe` 對應「黑色（已確認安全）」，不在任一集合對應「白色（沒走過）」。只有「灰」被重新繞到才是真正的環，「黑」被重新繞到是安全的共用依賴（菱形結構）
- `for` 迴圈裡「沒找到環」的分支不能提早 `return false`，要讓迴圈自然跑完所有子節點才能下結論；只有「找到環」才提早 `return true`

### 3️⃣ 演算法 / 資料結構盲點

- 第一次遇到「有向圖環偵測」，反覆在「該不該清除路徑集合、什麼時候清除」上卡住，核心盲點是沒有一開始就想清楚「目前路徑」跟「已確認安全」是兩個不同語意的集合，全部混在一個 `cur` 裡處理
- **多分支遞迴（一個節點有好幾個子節點要分別探索）跟「單一線性鏈」搞混**：一開始的虛擬碼描述像是「一路往下找前提值」的線性走法，沒有意識到 `vector<int>`（多個先修課）需要對每一個分別遞迴，不是一路到底的單一鏈
- 這題促成一條新的教學流程規則（`leetcode-tutor` skill v1.6 新增 4-14）：同一個方向連續 3 次以上冒新結構性問題時，改成拆解成最小步驟、一次只確認一步的引導方式，比一次給完整骨架讓使用者自己填空更有效

### 跟上次相比

（第一次複習，留空）
