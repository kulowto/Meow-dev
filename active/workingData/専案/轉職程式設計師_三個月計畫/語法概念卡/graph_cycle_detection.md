# 有向圖環偵測（DFS + 路徑集合 + 記憶化）

- 分類：解題思維框架（圖論、DFS 的延伸應用）
- 對應 C#：無直接語法對應，概念直接套用

> 複習時先看 Q，自己講一遍答案，再點開 `<details>` 對答案。答錯或講不出來的，去下面「完整筆記」補。
> 跟 [`recursion.md`](recursion.md)、[`unordered_map.md`](unordered_map.md)（`Node*→Node*` 的 Clone Graph 用法）同一脈絡：圖/樹的遞迴走訪 + hash 容器記錄狀態。

## 自我測驗

<details>
<summary>Q1. 判斷有向圖有沒有環，核心結構長什麼樣？</summary>

A1. 先把邊的關係轉成鄰接表 `unordered_map<int, vector<int>>`（節點 → 它指向的所有節點），再對每個節點做 DFS，用一個集合記錄「目前這條路徑正在走的節點」：

```cpp
unordered_map<int, vector<int>> mp;      // 建圖：對每筆 [a,b] 做 mp[a].push_back(b)
unordered_set<int> cur;                   // 目前這條路徑正在探索的節點

bool hasCycle(int i){
    cur.insert(i);

    for (int next : mp[i]){
        if (cur.find(next) != cur.end()) return true;      // 繞回目前路徑上的節點 = 找到環
        if (hasCycle(next)) return true;                     // 子路徑找到環，往上傳
    }

    cur.erase(i);       // 這個節點所有分支都探索完、確認安全，退出前移除
    return false;
}
```

對每個節點都呼叫一次 `hasCycle`（外層跑 `0` 到 `n-1`），只要有一次回傳 `true` 就代表有環。

</details>

<details>
<summary>Q2. 為什麼一個節點探索完自己「所有」子節點之後，才能把自己從 `cur` 移除？中途移除會怎樣？</summary>

A2. 一個節點可能有**多個**子節點（多筆先修/多條邊），要分別探索每一條分支（樹狀分岔，不是單一線性鏈）。如果某個節點在只探索完**第一條**分支後就被提早從 `cur` 移除，會發生兩種錯誤：
1. 還沒探索的其他分支，如果繞回這個提早被移除的節點，就偵測不到真正的環（該報 `true` 卻報 `false`）
2. 反過來，如果 `cur` 從頭到尾都不移除任何東西（只加不減），會把「兩條分支共用同一個安全節點」（菱形依賴，例如 `A→B`、`A→C`、`B→D`、`C→D`，`D` 被兩邊共用但沒有環）誤判成環——因為 `D` 在探索 `B` 那條分支時被加進 `cur`、卻沒被移除，探索 `C` 那條分支繞到 `D` 時，`cur` 裡還殘留著它

正確時機：**這個節點的 `for` 迴圈（所有子節點）全部跑完、確認沒有任何一條分支找到環之後**，才把自己從 `cur` 移除，且只移除自己（`i`），不是移除子節點。

</details>

<details>
<summary>Q3. 只有 `cur` 沒有記憶化，為什麼會 Time Limit Exceeded？怎麼優化？</summary>

A3. 沒有記憶化時，同一個節點會在**不同的外層起點**之間被重複完整探索。例如 `A→B→C`、`A→D→C`，`C` 會在探索 `B` 那條路時被完整驗證一次，探索 `D` 那條路時又被重新驗證一次——如果圖很密集，這種重複會讓複雜度遠超過 O(V+E)，導致超時。

優化：再加一個 `unordered_set<int> checkSafe`，一個節點**所有分支都探索完、確認安全**時（跟 `cur.erase(i)` 同一個時間點），順便 `checkSafe.insert(i)`。`hasCycle` 一開始先檢查：如果這個節點已經在 `checkSafe` 裡，直接 `return false`，不用重新展開整棵子樹：

```cpp
bool hasCycle(int i){
    if (checkSafe.count(i)) return false;   // 已確認安全，直接跳過

    cur.insert(i);
    for (int next : mp[i]){
        if (cur.find(next) != cur.end()) return true;
        if (hasCycle(next)) return true;
    }
    checkSafe.insert(i);   // 全部探索完才標記安全
    cur.erase(i);
    return false;
}
```

這樣每個節點最多被完整探索一次，複雜度回到 O(V+E)。這正是經典的「白/灰/黑三色標記」DFS 環偵測法的簡化版：`cur` 對應「灰色（目前路徑上）」，`checkSafe` 對應「黑色（已確認安全）」，不在任何集合裡的對應「白色（還沒走過）」。

</details>

<details>
<summary>Q4. 迴圈裡遇到「這個子節點沒問題，繼續看下一個」的情況，該怎麼寫？常見的坑是什麼？</summary>

A4. `for` 迴圈裡「這個子節點沒有環」的分支，**什麼都不用做，讓迴圈自然跑下一輪**，不要在這個分支裡提早 `return false`——一旦提早 `return`，迴圈裡還沒檢查的其他子節點會被整個跳過，如果那些沒檢查的子節點裡藏著環，會被漏掉。只有「找到環」（`true`）的情況才需要提早 `return true`；「沒找到環」的情況要等**整個迴圈跑完**才能下結論、才能 `return false`。

</details>

## 完整筆記

這個套路本質上是樹/圖遞迴的延伸：一個節點有多個子節點時（不是單一線性鏈），要用 `for` 迴圈個別遞迴每個子節點，不能假設只有一個要跟著走下去——跟 Clone Graph 的 `for (Node* nb : node->neighbors)` 是同一種「多分支遞迴」的處理方式。

## 出現過的題目

| 題號 | 用法情境 |
|------|---------|
| 207 | Course Schedule：`cur`（目前路徑）+ `checkSafe`（已確認安全）雙集合 DFS，判斷先修關係圖有沒有環 |
