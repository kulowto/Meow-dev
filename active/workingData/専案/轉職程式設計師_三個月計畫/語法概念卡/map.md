# map

- 分類：STL 容器（Ordered，紅黑樹）
- 對應 C#：`SortedDictionary<TKey,TValue>`

> 複習時先看 Q，自己講一遍答案，再點開 `<details>` 對答案。答錯或講不出來的，去下面「完整筆記」補。
> 跟 [`unordered_map`](unordered_map.md) 是同一組概念的兩面，建議一起複習對照。
> 這是「依值整理」家族的一員，何時該用、何時不該用，見 [`order_vs_value.md`](order_vs_value.md) 的判斷框架。

## 自我測驗

<details>
<summary>Q1. 這是什麼？跟 unordered_map 差在哪？</summary>

A1. 一樣是 key-value 容器，但底層是 [**紅黑樹**](red_black_tree.md)（自平衡二元搜尋樹），遍歷時會**自動依 key 由小到大排序**。跟 `unordered_map`（hash table）比，犧牲一點查詢速度（O(log n) 而非 O(1)），換取「順序」跟「範圍查詢」的能力。

</details>

<details>
<summary>Q2. 核心操作有哪些？跟 unordered_map 一樣嗎？</summary>

A2. API 幾乎一樣：
```cpp
m[key] = value;
m.insert({key, value});
m.count(key);
m.find(key);
m.erase(key);
for (auto& [k, v] : m) { }   // 保證依 key 由小到大遍歷
```
唯一差異是遍歷順序有保證，其他操作用法跟 `unordered_map` 幾乎相同（這也是兩者最容易搞混的地方）。

</details>

<details>
<summary>Q3. 常見的坑是什麼？</summary>

A3.
1. 查詢速度比 `unordered_map` 慢（O(log n) vs O(1)），沒有排序需求還選 `map` 是白白犧牲效能
2. 插入/刪除也是 O(log n)（樹要重新平衡），但**不像排序陣列插入要 O(n) 搬移資料**——這是它跟「排序陣列 + 二分法查詢」的關鍵差異，紅黑樹靠指標連接，插入只要接掛節點、不用搬動其他元素

</details>

<details>
<summary>Q4. 時間/空間複雜度？</summary>

A4. 查詢/插入/刪除都是 **O(log n)**（紅黑樹自平衡，最壞情況也保證這個複雜度，不會退化）。空間 O(n)。

</details>

## 完整筆記

`map<KeyType, ValueType>`，`#include <map>`。

底層節點結構、平衡規則、為什麼要平衡，完整說明見 [`red_black_tree.md`](red_black_tree.md)（獨立成卡，方便未來其他樹狀結構/節點相關用法都能連過去複習）。

這裡只講跟 `map` 直接相關的部分：查詢邏輯精神上跟[二分法查詢](binary_search.md)很像（每一步排除一半範圍），但差異在於：

| | 排序陣列 + 二分法查詢 | `map`（紅黑樹） |
|---|---|---|
| 儲存方式 | 連續記憶體，靠 index 定位 | 節點各自配置，靠指標連結 |
| 查詢 | O(log n) | O(log n) |
| 插入/刪除 | O(n)（要搬移維持連續+排序） | O(log n)（只要接掛節點） |
| 適合情境 | 資料建好後很少變動、常查詢 | 資料常常新增/刪除，同時要保持順序 |

詳細的記憶體佈局差異跟生活比喻見 `binary_search.md`。

## 出現過的題目

| 題號 | 用法情境 |
|------|---------|
|      | （尚未實際用到，先建卡打底）|
