# 滑動視窗（Sliding Window）

- 分類：解題思維框架（雙指標的一種應用）
- 對應 C#：無直接語法對應，是思考套路

> 複習時先看 Q，自己講一遍答案，再點開 `<details>` 對答案。答錯或講不出來的，去下面「完整筆記」補。
> 跟 [`order_vs_value.md`](order_vs_value.md) 的「順序重要」家族同一脈絡：不重新排列元素，用兩個索引框住一段連續範圍往前推進。

## 自我測驗

<details>
<summary>Q1. 什麼時候該直覺想到滑動視窗？</summary>

A1. 題目要求「找出一段**連續**的子字串/子陣列，滿足某個條件（不重複、總和等於/小於某值、包含某些字元…），求最長/最短/數量」時，是強烈候選。核心精神：用兩個索引（`left`、`right` 或迴圈變數 `idx`）框住目前正在檢查的一段連續範圍，`right` 往右擴張、`left` 在需要時往右收縮，全程不用重新排列或複製資料，也不用對每個起點都重新算一次。

</details>

<details>
<summary>Q2. 核心結構長什麼樣？以「找最長不重複子字串」為例</summary>

A2.
```cpp
int left = 0;
unordered_map<char,int> lastSeen;   // 記錄每個字元「最後」出現的位置
int maxLen = 0;

for (int idx = 0; idx < s.size(); idx++) {
    if (lastSeen.count(s[idx]) && lastSeen[s[idx]] >= left) {
        // 上次出現的位置還在目前視窗範圍內，真的重複了，收縮視窗
        left = lastSeen[s[idx]] + 1;
    }
    lastSeen[s[idx]] = idx;          // 永遠更新成最新位置，不需要刪除舊 entry
    maxLen = max(maxLen, idx - left + 1);
}
```
`left` 只會往右移動，不會後退。`idx - left + 1` 是目前視窗（`[left, idx]`）的長度（索引差要 `+1` 才是元素個數）。

</details>

<details>
<summary>Q3. `left` 到底代表什麼？容易誤解成什麼？</summary>

A3. `left` 是「**目前這段合法視窗的起始索引**」，不是「曾經發生過重複的那段範圍」。`left` 左邊的字元已經被排除在目前視窗之外——有些是真的造成過重複才被排除，有些只是因為 `left` 一次跳過一整段而被連帶排除（不代表它們自己也重複過）。判斷視窗長度、更新視窗邊界，永遠是看 `left` 跟 `idx`（或 `right`）這兩個索引的相對位置，不是去回憶「哪裡發生過什麼」。

</details>

<details>
<summary>Q4. `lastSeen[c] >= left` 這個檢查為什麼一定要加，不能只看「這個字元有沒有出現過」？</summary>

A4. 因為 `lastSeen`（或任何記錄「上次出現位置」的 map）裡的 entry **不會被刪除**，只會被覆蓋。如果某個字元很久以前出現過，但那個位置早就已經被 `left` 甩在後面（不在目前視窗範圍內了），這筆紀錄就是「過期的」——這時候不該把它當成「重複」來處理，否則會誤觸發 `left` 往回移動（或至少誤判成不必要的收縮），導致視窗變得比實際應該的還小，算出偏小的錯誤答案。用 `s="abba"` 具體驗證：`idx=3` 讀到的 `a` 上次出現在位置 `0`，但這時候 `left` 已經是 `2` 了（`0` 這個位置早就不在視窗內），必須用 `lastSeen['a'](0) >= left(2)`？不成立，來判斷這筆紀錄是過期的，`left` 不該被改動。

</details>

<details>
<summary>Q5. 為什麼不需要真的把過期的 entry 從 map 裡刪除？</summary>

A5. 因為每次查詢時都會先做 `>= left` 這個過濾，過期的 entry 天然就會被忽略，不需要另外花力氣清掉。硬要清除（例如遍歷整個 map、刪掉所有位置小於某個門檻的 entry）不只複雜、容易踩到「一邊迭代一邊 erase」的坑（見 [`unordered_map.md`](unordered_map.md) Q5），效率也更差（每次重複都要掃一次整個 map，最壞情況退化成 O(n²)）；用 `left` 索引 + 隨時覆蓋成最新位置，才是 O(n) 的正確做法。

</details>

<details>
<summary>Q6. 用 `unordered_map<char,int>` 記錄位置，還有其他寫法嗎？</summary>

A6. 兩種常見的替代寫法，都比 `unordered_map` 更快（利用「字元集合固定且小」的性質，見 [`container_selection.md`](container_selection.md)）：

**用固定大小陣列取代 hash map**（字元直接當索引，涵蓋整個 ASCII 用 128）：
```cpp
array<int, 128> lastSeen;
lastSeen.fill(-1);
```
比 `unordered_map` 少了 hash 運算、記憶體連續、常數因子更小。

**用「頻率計數」取代「記錄位置」，搭配 `while` 一步步收縮視窗**：
```cpp
vector<int> freq(128, 0);
int l = 0;
for (int i = 0; i < s.size(); i++) {
    while (freq[s[i]] > 0) {      // 這個字元已經在視窗裡
        freq[s[l]]--;              // 踢出視窗最左邊的字元
        l++;
    }
    ans = max(ans, i - l + 1);
    freq[s[i]]++;
}
```
`l` 全程只會往前移動、不會後退，`while` 迴圈裡的 `l++` 加總起來最多跑 `n` 次，攤還下來整體還是 O(n)，不是巢狀迴圈看起來的 O(n²)——這叫**攤還分析（amortized analysis）**：迴圈裡有 `while`，但某個指標單調遞增時，真實複雜度要看這個指標總共能移動幾次，不是看迴圈巢狀層數。

**用 `max()` 直接消除「是否出現過」的分支**：
```cpp
idx = max(idx, lastSeenIdx[c]);   // lastSeenIdx 初始值全部是 -1，idx 也從 -1 開始
```
「沒出現過」（`-1`）、「出現過但已過期」（比目前 `idx` 小）這兩種情況，`max()` 自然不會更新 `idx`，不需要額外寫 `if` 判斷「有沒有出現過」。這跟 [`dynamic_programming.md`](dynamic_programming.md) 用 `INT_MIN` 消除特殊分支、[`digit_carry_addition.md`](digit_carry_addition.md) 用 `%2`/`/2` 取代兩條規則，是同一種「用算式取代分支判斷」的精神。

</details>

## 完整筆記

滑動視窗本質上是雙指標的一種：`right`（或迴圈的 `idx`）負責擴張視窗、檢查新元素；`left` 負責在條件被打破時收縮視窗。整個過程每個元素最多被 `left`、`right` 各碰過一次，所以是 O(n)，比「對每個起點都重新掃一次」的 O(n²) 做法好很多。

## 出現過的題目

| 題號 | 用法情境 |
|------|---------|
| 3 | Longest Substring Without Repeating Characters：`left` + `unordered_map<char,int>` 記錄最後出現位置，`lastSeen[c] >= left` 判斷是否在視窗內真的重複，`idx-left+1` 算視窗長度 |
