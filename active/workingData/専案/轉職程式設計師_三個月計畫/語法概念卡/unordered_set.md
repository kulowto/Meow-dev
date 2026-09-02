# unordered_set

- 分類：STL 容器（Hash Table）
- 對應 C#：`HashSet<T>`

> 複習時先看 Q，自己講一遍答案，再點開 `<details>` 對答案。答錯或講不出來的，去下面「完整筆記」補。
> 跟 [`unordered_map.md`](unordered_map.md) 底層原理完全一樣（hash table），差別只在要不要存對應的 value。跟其他容器的選擇對照，見 [`container_selection.md`](container_selection.md) 速查表。

## 自我測驗

<details>
<summary>Q1. 這是什麼？什麼情境下會想到用它？</summary>

A1. 底層是 hash table 的容器，只存**值本身**，沒有 key-value 配對。看到「只需要判斷某個東西有沒有出現過／存不存在」（不需要額外記錄對應的次數、索引、或其他資訊）第一直覺該想到它，O(1) 查詢，比 `vector` 每次要線性掃描快很多。

</details>

<details>
<summary>Q2. 核心操作有哪些？怎麼寫？</summary>

A2.
```cpp
#include <unordered_set>

unordered_set<int> s;

s.insert(x);              // 插入 x（已存在就不會重複插入）
s.count(x);                // 0 或 1，判斷是否存在
s.find(x) != s.end();       // 回傳 iterator，判斷是否存在
s.erase(x);
for (auto& x : s) { }       // range-based for，直接拿到值本身（不是 pair）
```

</details>

<details>
<summary>Q3. 常見的坑是什麼？跟 `unordered_map` 比有什麼要注意的？</summary>

A3.
1. **沒有 `[]` 運算子**：`unordered_map` 可以用 `m[key]` 存取／自動建立，`unordered_set` 沒有這個語法，只能用 `insert`／`count`／`find`
2. `insert` 對已存在的值再插入一次，**不會報錯、也不會變成兩筆**，`set` 天生就是「值唯一」的容器，重複插入等於沒動作
3. 遍歷順序不固定，跟插入順序、值大小都無關（跟 `unordered_map` 一樣）
4. 要有序（遍歷時自動排序）要換 `set<T>`（紅黑樹版本，對應 `unordered_map`/`map` 的關係）
5. 對「空的」`unordered_set` 呼叫 `count`/`find` 完全安全，只會回傳「找不到」

</details>

<details>
<summary>Q4. 時間/空間複雜度？</summary>

A4. 平均插入/查詢/刪除都是 O(1)；最壞情況（hash 碰撞嚴重）退化成 O(n)。空間 O(n)。

</details>

## 完整筆記

跟 `unordered_map` 的選擇判斷準則：**需要「值 + 對應的另一個資訊」（次數、索引、任何配對資料）→ `unordered_map`；只需要「這個值有沒有出現過」，不需要額外資訊 → `unordered_set`**。用 `unordered_map<T,bool>` 硬凹出「有沒有出現過」的效果也能動，但語意上不精準，浪費一個用不到的 value 欄位，`unordered_set` 才是精準對應這個需求的工具。

跟 `vector` 比：`vector` 查一個值存不存在要整個掃過去，O(n)；重複查很多次（例如逐一檢查陣列裡每個元素有沒有出現過）會讓整體退化成 O(n²)。`unordered_set` 插入/查詢都是 O(1)，適合「邊走訪邊記錄看過的值、邊查有沒有重複」這種情境。

對應 C# 的 `HashSet<T>`，概念與操作幾乎一樣（`Add`/`Contains`/`Remove` 對應 `insert`/`count` 或 `find`/`erase`）。

### Big-O 比較好，實際跑分不一定比較快

`unordered_set` 版本 O(n) 理論上比「排序 + 掃相鄰元素」的 O(n log n) 好，但 LeetCode 測資規模下，實測常常是排序版本更快。原因是**常數因子**：hash table 每次操作要算 hash、處理碰撞、動態配置記憶體（節點散落在 heap 各處，cache miss 多）；排序後的 `vector` 是連續記憶體，CPU 讀取快取命中率高，`std::sort` 本身也是高度優化過的實作。資料量成長到非常大時，O(n) 的理論優勢才會明顯蓋過常數因子的劣勢。Big-O 只講成長趨勢，不代表小到中等資料量下誰的實際跑分比較快。

## 出現過的題目

| 題號 | 用法情境 |
|------|---------|
| 217 | Contains Duplicate：邊走訪陣列邊用 `s.count(nums[i])` 查有沒有出現過，有就直接 `return true`，沒有就 `s.insert(nums[i])`，走訪完都沒觸發就 `return false` |
