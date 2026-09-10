# unordered_map（含 unordered_set）

- 分類：STL 容器（Hash Table）
- 對應 C#：`unordered_map` ↔ `Dictionary<TKey,TValue>`；`unordered_set` ↔ `HashSet<T>`

> 複習時先看 Q，自己講一遍答案，再點開 `<details>` 對答案。答錯或講不出來的，去下面「完整筆記」補。
> 「依值整理」家族的代表，何時該用、何時不該用，見 [`order_vs_value.md`](order_vs_value.md)；跟其他容器的選擇對照，見 [`container_selection.md`](container_selection.md)。有序版本是 [`map`](map.md)（紅黑樹）。

## 自我測驗

<details>
<summary>Q1. 這是什麼？什麼情境下會想到用它？</summary>

A1. 底層是 hash table 的 key-value 容器，O(1) 平均查表。看到「配對/互補」類問題（例如 `target - nums[i]` 這種形式，要查某個值有沒有出現過）第一直覺就該想到它，用空間換時間。

</details>

<details>
<summary>Q2. 核心操作有哪些？怎麼寫？</summary>

A2.
```cpp
m[key] = value;              // 插入或覆蓋
m.insert({key, value});      // 只在不存在時插入
m.count(key);                // 0 或 1，判斷是否存在
m.find(key) != m.end();      // 回傳 iterator，可直接拿值
m.at(key);                   // 取值，key 不存在會丟例外
m.erase(key);
m[c]++;                       // 取代「查有沒有出現、有就累加、沒有就設 1」的 if-else（不存在自動建 value=0 再 ++）
for (auto& [k, v] : m) { }   // C++17 結構化綁定遍歷
```

</details>

<details>
<summary>Q3. 常見的坑是什麼？</summary>

A3.
1. `m[key]` 如果 key 不存在會**自動新增**一個預設值 entry（int 是 0），不會像 C# 那樣丟例外。想「檢查存在」別直接 `if (m[key] == ...)`，要用 `count` 或 `find`
2. 遍歷順序不固定，跟插入順序、key 大小都無關。要有序換 [`map`](map.md)
3. `count` 只查一次表判斷有無，`find` 可以一次拿到 iterator 直接取值——查完馬上要用值時用 `find` 比 `count` + `m[key]`（查兩次）好
4. `find` 拿到的 iterator 用 `it->first`（key）、`it->second`（value）取值
5. 對「空的」`unordered_map` 呼叫 `count`/`find` 完全安全，只回傳「找不到」——跟 `stack` 空的時候呼叫 `top()`/`pop()` 是未定義行為不一樣
6. iterator 只能用 `==`／`!=` 比較，**不支援 `<`／`>=`**（hash table 沒有「誰在誰前面」的概念）。`for (auto it = m.begin(); it != m.end(); it++)` 才對，不能 `it < m.end()`——跟 `vector` 的 random access iterator 最大的差異

</details>

<details>
<summary>Q4. 時間/空間複雜度？</summary>

A4. 平均插入/查詢/刪除都是 O(1)；最壞情況（hash 碰撞嚴重）退化成 O(n)，一般題目不會刻意設計碰撞。空間 O(n)。

</details>

<details>
<summary>Q5. 一邊走訪、一邊要 `erase` 某些 entry，正確寫法是什麼？</summary>

A5. **不能**用一般 `for` 迴圈自帶的 `iter++` 搭配迴圈內的 `erase`：

```cpp
// 錯誤：erase 之後 iter 已失效，接著 for 迴圈還會執行 iter++（對失效的 iterator 操作，未定義行為）
for (auto iter = store.begin(); iter != store.end(); iter++) {
    if (該刪除) store.erase(iter->first);
}
```

要讓迴圈自己控制何時前進：

```cpp
// 正確：erase 回傳「指向下一個元素」的 iterator，用它取代手動 ++；沒刪除時才自己 ++iter
for (auto iter = store.begin(); iter != store.end(); ) {
    if (該刪除) iter = store.erase(iter);
    else        ++iter;
}
```

**額外**：如果迴圈開始前另外拿了一個獨立 iterator（例如 `auto reg = store.find(key);`）在迴圈裡用，只要迴圈中途把 `reg` 指到的 entry 也刪掉，`reg` 一樣失效，之後讀 `reg->second` 是未定義行為。安全做法是**在迴圈開始前先把 `reg->second` 取出來存成普通變數**，迴圈裡用這個普通變數比較。

</details>

## unordered_set（沒有 value 的版本）

<details>
<summary>S1. 什麼時候用 unordered_set 而不是 unordered_map？</summary>

S1. 只存**值本身**，沒有 key-value 配對。判斷準則：**需要「值 + 對應的另一個資訊」（次數、索引、任何配對資料）→ `unordered_map`；只需要「這個值有沒有出現過」→ `unordered_set`**。用 `unordered_map<T,bool>` 硬凹也能動，但浪費一個用不到的 value 欄位，語意不精準。

```cpp
#include <unordered_set>
unordered_set<int> s;
s.insert(x);              // 已存在再 insert 不會報錯也不會變兩筆（set 天生值唯一）
s.count(x);                // 0 或 1
s.find(x) != s.end();
s.erase(x);
for (auto& x : s) { }       // 直接拿到值本身，不是 pair
```

</details>

<details>
<summary>S2. unordered_set 跟 unordered_map 比，有什麼不同要注意？</summary>

S2.
1. **沒有 `[]` 運算子**：只能用 `insert`／`count`／`find`／`erase`，不能 `s[x]`
2. 遍歷順序一樣不固定
3. 要有序（遍歷時自動排序）換 `set<T>`（紅黑樹版本）
4. 其他行為（O(1)、空容器查詢安全、iterator 限制）跟 `unordered_map` 一樣

</details>

<details>
<summary>S3. Big-O 比較好，實際跑分不一定比較快</summary>

S3. `unordered_set` 版本 O(n) 理論上比「排序 + 掃相鄰元素」的 O(n log n) 好，但 LeetCode 測資規模下，實測常常是排序版本更快——**常數因子**：hash table 每次操作要算 hash、處理碰撞、節點散落 heap（cache miss 多）；排序後的 `vector` 連續記憶體、`std::sort` 高度優化。資料量成長到非常大時，O(n) 的理論優勢才會蓋過常數因子劣勢。Big-O 只講成長趨勢，不代表小到中等資料量下誰跑分快。

</details>

## 完整筆記

`#include <unordered_map>` / `#include <unordered_set>`。

- **命名**：`map` 是「映射」（key 對應 value），不是「循跡」；`unordered` 指不保證遍歷順序（元素落在哪個 bucket 看 key 的 hash，跟插入順序、key 大小無關）——犧牲順序換 O(1) 直接定位
- **生活比喻**：健身房置物櫃／超商取貨櫃——輸入密碼/編號直接算出位置，不用一格一格找；不管裡面裝多少東西，查一次時間幾乎不變
- **key 型別限制**：內建型別（int、string、指標…）可直接當 key；自訂 struct/class 當 key 要另外提供 hash 特化
- **key 種類固定且少時，用固定大小陣列更快**：只有 26 個字母、10 個數字這種，`int count[26]` 透過 `c-'a'` 轉索引，複雜度一樣但常數因子小很多（見 [`container_selection.md`](container_selection.md)）
- **`for (auto& [k,v] : m)` 是語法糖**：等價於手動 iterator 迴圈，編譯器自動處理「走到下一個」，見 [`range_based_for.md`](range_based_for.md)

## 出現過的題目

| 題號 | 用法情境 |
|------|---------|
| 1 | Two Sum：`seen[value] = index` 邊遍歷邊記錄，查 `target - nums[i]` 有沒有出現過，取代 O(n²) 暴力雙迴圈 |
| 383 | Ransom Note：兩邊字串各建 `unordered_map<char,int>` 統計次數，單向比對「夠不夠用」（≥） |
| 242 | Valid Anagram：兩個 `unordered_map` 記錄 s、t 字元計數，比對是否完全一致 |
| 3 | Longest Substring Without Repeating Characters：`unordered_map<char,int>` 記錄字元上次出現位置，踩到「erase 期間迭代」的 UB（Q5）跟「iterator 當數字比較」（Q3 第 6 點） |
| 169 | Majority Element：邊遍歷邊 `st[nums[i]]++`，數量一超過 `n/2` 立刻提早 return |
| 217 | Contains Duplicate：`unordered_set`，邊走訪邊 `s.count(nums[i])` 查有沒有出現過，有就 `return true`，沒有就 `s.insert` |
| 133 | Clone Graph：`unordered_map<Node*, Node*>` 記錄「原節點→複製品」，同時身兼 visited 標記與查詢表；登記要在遞迴 neighbors 之前做 |
