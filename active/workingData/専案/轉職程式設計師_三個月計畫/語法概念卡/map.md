# map

- 分類：STL 容器（Ordered，紅黑樹）
- 對應 C#：`SortedDictionary<TKey,TValue>`

> 複習時先看 Q，自己講一遍答案，再點開 `<details>` 對答案。答錯或講不出來的，去下面「完整筆記」補。
> 跟 [`unordered_map`](unordered_map.md) 是同一組概念的兩面，建議一起複習對照。
> 「依值整理」家族的一員，何時該用、何時不該用，見 [`order_vs_value.md`](order_vs_value.md)。

## 自我測驗

<details>
<summary>Q1. 這是什麼？跟 unordered_map 差在哪？</summary>

A1. 一樣是 key-value 容器，但底層是**紅黑樹**（自平衡二元搜尋樹，見下方「底層機制」），遍歷時會**自動依 key 由小到大排序**。跟 `unordered_map`（hash table）比，犧牲一點查詢速度（O(log n) 而非 O(1)），換取「順序」跟「範圍查詢」的能力。

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
2. 插入/刪除也是 O(log n)（樹要重新平衡），但**不像排序陣列插入要 O(n) 搬移資料**——紅黑樹靠指標連接，插入只要接掛節點、不用搬動其他元素

</details>

<details>
<summary>Q4. 時間/空間複雜度？</summary>

A4. 查詢/插入/刪除都是 **O(log n)**（紅黑樹自平衡，最壞情況也保證這個複雜度，不會退化）。空間 O(n)。

</details>

## 底層機制：紅黑樹（Red-Black Tree）

<details>
<summary>M1. 紅黑樹是什麼？為什麼需要「平衡」？</summary>

M1. 一種**自平衡二元搜尋樹**。普通 BST 如果不平衡，最壞情況（例如依序插入 1,2,3,4,5）會**退化成一條鏈**，查詢變 O(n)，失去樹狀結構的意義。紅黑樹靠幫每個節點加一個「顏色」屬性（紅/黑）加上幾條規則，強制樹高維持在 O(log n)，不管怎麼插入刪除都不退化。

</details>

<details>
<summary>M2. 節點結構、平衡規則（知道大方向就好，不用背、不用實作）</summary>

M2. 節點比普通 BST 多兩個欄位：`parent` 指標（平衡調整時往上找）、`color`（紅或黑）。
平衡規則大方向：根節點必須黑、紅節點的子節點不能也是紅、從任一節點到所有後代 leaf 的路徑上黑節點數量相同。違反規則時靠**旋轉（rotation）**加**變色**調整回來。
刷題階段只要知道：它保證 insert / delete / search 在任何情況下都是 O(log n)。

</details>

<details>
<summary>M3. 為什麼 STL 選紅黑樹，不選 AVL 樹？</summary>

M3. AVL 樹對平衡的要求更嚴（左右子樹高度差最多 1），查詢稍快，但插入/刪除要做更多次旋轉。紅黑樹平衡要求較寬鬆，旋轉次數少，更適合「寫入頻繁」的通用型容器。知道「有取捨」就好。

</details>

## 完整筆記

`map<KeyType, ValueType>`，`#include <map>`。C++ STL 的 `map`、`set` 底層都是紅黑樹。

跟「排序陣列 + [二分法查詢](binary_search.md)」的取捨（查詢都是 O(log n)，差在插入/刪除跟記憶體佈局）：

| | 排序陣列 + 二分法查詢 | `map`（紅黑樹） |
|---|---|---|
| 儲存方式 | 連續記憶體，靠 index 定位 | 節點各自配置，靠指標連結 |
| 插入/刪除 | O(n)（要搬移維持連續+排序） | O(log n)（只要接掛節點） |
| 適合情境 | 資料建好後很少變動、常查詢 | 資料常常新增/刪除，同時要保持順序 |

「節點 + 指標」家族還有 [`linked_list`](linked_list.md)（更單純的單向鏈結）。樹狀結構走訪幾乎都搭配 [`recursion`](recursion.md)。

## 出現過的題目

| 題號 | 用法情境 |
|------|---------|
|      | （尚未實際用到，先建卡打底）|
