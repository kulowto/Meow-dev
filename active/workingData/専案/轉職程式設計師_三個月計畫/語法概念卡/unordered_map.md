# unordered_map

- 分類：STL 容器（Hash Table）
- 對應 C#：`Dictionary<TKey,TValue>`

> 複習時先看 Q，自己講一遍答案，再點開 `<details>` 對答案。答錯或講不出來的，去下面「完整筆記」補。
> 這是「依值整理」家族的代表，何時該用它、何時不該用，見 [`order_vs_value.md`](order_vs_value.md) 的判斷框架；跟其他容器的選擇對照，見 [`container_selection.md`](container_selection.md) 速查表。

## 自我測驗

<details>
<summary>Q1. 這是什麼？什麼情境下會想到用它？</summary>

A1. 底層是 hash table 的 key-value 容器。看到「配對/互補」類問題（例如 `target - nums[i]` 這種形式，要查某個值有沒有出現過）第一直覺就該想到它，用空間換時間、O(1) 查表。

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
for (auto& [k, v] : m) { }   // C++17 結構化綁定遍歷
```

</details>

<details>
<summary>Q3. 常見的坑是什麼？（跟直覺不一樣、容易寫錯的地方）</summary>

A3.
1. `m[key]` 如果 key 不存在會**自動新增**一個預設值 entry（int 是 0），不會像 C# `Dictionary` 那樣丟例外。只是想「檢查存在」千萬別直接 `if (m[key] == ...)`，要用 `count` 或 `find`。
2. 遍歷順序不固定，跟插入順序、key 大小都無關。要有序要換 [`map`](map.md)。
3. `count` 只查一次表判斷有無，`find` 可以一次拿到 iterator 直接取值——如果查完馬上要用值，用 `find` 比 `count` + `m[key]`（查兩次）更好。
4. `find` 拿到的 iterator 要用 `it->first`（key）、`it->second`（value）取值，不是直接當成 value 用。
5. 同一個 key 不會有兩筆資料，重複 `m[key] = xxx` 只會覆蓋成最後一次的值，不會累積。
6. 對「空的」`unordered_map` 呼叫 `count`/`find` 完全安全，只會回傳「找不到」——這點跟 `stack` 空的時候呼叫 `top()`/`pop()` 是未定義行為不一樣，是兩種容器行為上的差異。
7. `m[c]++` 可以取代「先查有沒有出現、有就累加、沒有就新增設 1」的 if-else：不存在的 key 會自動建立 `value=0`，再 `++` 就變成 `1`。
8. iterator 只能用 `==`／`!=` 比較，**不支援 `<`**（底層 hash table 沒有「誰在誰前面」的概念）。`for (auto it = m.begin(); it != m.end(); it++)` 才對，不能用 `it < m.end()`——這是跟 `vector` 的 random access iterator 最大的差異。

</details>

<details>
<summary>Q4. 時間/空間複雜度？</summary>

A4. 平均插入/查詢/刪除都是 O(1)；最壞情況（hash 碰撞嚴重）退化成 O(n)，但一般題目不會刻意設計碰撞。空間 O(n)。

</details>

<details>
<summary>Q5. 一邊走訪、一邊要 `erase` 某些 entry，正確寫法是什麼？</summary>

A5. **不能**用一般的 `for` 迴圈自帶的 `iter++` 搭配迴圈內的 `erase`：

```cpp
// 錯誤：erase 之後 iter 已失效，接著 for 迴圈還會執行 iter++（對失效的 iterator 操作，未定義行為）
for (auto iter = store.begin(); iter != store.end(); iter++) {
    if (該刪除) store.erase(iter->first);
}
```

`erase(iter)` 或 `erase(key)` 都會讓「指向被刪除那個 entry」的 iterator 失效。要讓迴圈自己控制何時前進：

```cpp
// 正確：erase 回傳「指向下一個元素」的 iterator，用它取代手動 ++；沒刪除時才自己 ++iter
for (auto iter = store.begin(); iter != store.end(); ) {
    if (該刪除) {
        iter = store.erase(iter);
    } else {
        ++iter;
    }
}
```

**額外要注意**：如果迴圈開始前，另外拿了一個獨立的 iterator（例如 `auto reg = store.find(key);`）在迴圈判斷式裡使用，只要迴圈中途把 `reg` 指到的那個 entry 也刪掉了，`reg` 一樣會失效，之後再讀 `reg->second` 就是未定義行為——即使你已經用上面的正確寫法處理了 `iter`，`reg` 是另一個獨立變數，erase 不會幫你同步更新它。安全做法是**在迴圈開始前，先把 `reg` 指到的值取出來存成一個普通變數**（例如 `int regValue = reg->second;`），迴圈裡用這個普通變數比較，不要在迴圈進行中持續依賴一個可能被同一個迴圈弄失效的 iterator。

</details>

## 完整筆記

`unordered_map<KeyType, ValueType>`，`#include <unordered_map>`。

跟 [`map`](map.md)（紅黑樹，O(log n)，key 自動排序）的差異：沒有排序需求時優先用 `unordered_map`，比較快。`map` 對應 C# 的 `SortedDictionary<K,V>`。詳細的底層機制比較（紅黑樹 vs hash table）見 `map.md`。

key 型別限制：內建型別（int、string...）可以直接當 key。自訂 struct/class 當 key 要另外提供 hash 特化，否則編不過（之後遇到再細講）。

### `unordered_set`：只要「存不存在」，不需要 value 時用這個

`unordered_set<T>` 跟 `unordered_map` 底層原理相同（hash table），差別是**只存值本身，沒有 key-value 配對**。只需要判斷「這個東西有沒有出現過」，不需要額外存一個對應的值時，用 `unordered_set` 比 `unordered_map` 更適合。完整用法、常見坑見獨立卡片 [`unordered_set.md`](unordered_set.md)。

### 命名由來

- `map`：不是「循跡」，是**映射**——key 對應 value 的關係（一個 key 對應一個 value，但不同 key 可以指向同個 value，不是嚴格的數學一對一）
- `unordered`：不保證遍歷順序。因為底層是 hash table，元素落在哪個 bucket 是看 key 的 hash 值決定，跟插入順序、key 大小完全無關——犧牲順序、換取 O(1) 直接定位的查詢速度

### 生活比喻（幫助理解「直接定位」而不是「搜尋」）

- **健身房置物櫃**：輸入密碼直接算出對應格子，不用一格一格找。密碼 = key，置物櫃內容 = value；分配到哪一格跟入場先後順序無關（= unordered）
- **超商取貨櫃**：拿取件編號直接定位貨架位置，不用把整排包裹看過一遍找名字
- **停車場感應票證**：卡片一嗶直接調出紀錄，不用翻一份完整的入場車輛清單

三者共通點：**只要給對 key，不管容器裡裝了多少東西，查一次的時間幾乎不變（O(1)）**，代價是完全不能保證裡面的排列順序。

### key 種類固定且少時，用固定大小陣列取代它更快

`unordered_map` 的彈性（任意型別、任意數量的 key）是有代價的：要算 hash、資料散落在記憶體不同位置、內部會動態配置記憶體。如果 key 的種類**固定又很少**（例如只有 26 個小寫英文字母、10 個數字），直接用一個固定大小陣列（`int count[26]`），透過 `c - 'a'` 轉成索引直接存取，時間複雜度一樣，但常數因子小很多、實測更快（Ransom Note 這題示範過）。key 種類不確定或數量可能很大時，才需要真正用到 `unordered_map` 的彈性。

### range-based for 是語法糖

`for (auto& [k,v] : m)` 背後等價於 `for (auto it = m.begin(); it != m.end(); ++it) { auto& [k,v] = *it; }`——「走到下一個元素」這個動作編譯器自動處理，不需要（也不能）自己額外寫遞增。不只 `unordered_map`，`vector`、`map`、`set` 等所有支援 `begin()`/`end()` 的容器都能用這個語法。

## 出現過的題目

| 題號 | 用法情境 |
|------|---------|
| 1 | Two Sum：用 `seen[value] = index` 邊遍歷邊記錄，查 `target - nums[i]` 有沒有出現過，取代 O(n²) 暴力雙迴圈 |
| 383 | Ransom Note：兩邊字串各自建 `unordered_map<char,int>` 統計次數，單向比對「夠不夠用」（≥），不是雙向完全相等 |
| 242 | Valid Anagram：兩個 `unordered_map` 分別記錄 s、t 的字元計數，比對是否完全一致；練習 iterator 走訪與 range-based for 兩種寫法 |
| 3 | Longest Substring Without Repeating Characters：`unordered_map<char,int>` 記錄每個字元上次出現的位置，遇到重複時掃過整個 map 刪除過期 entry。踩到「erase 期間迭代」的 UB（見 Q5），以及誤把 iterator（`reg`）當數字用 `>=` 比較（呼應 Q3 第 8 點，iterator 不支援大小比較） |
| 169 | Majority Element：`unordered_map<int,int>` 邊遍歷邊 `st[nums[i]]++`，數量一超過 `n/2` 立刻提早 return，不用等統計完再找最大值 |
| 133 | Clone Graph：`unordered_map<Node*, Node*>` 記錄「原節點→複製品」，同時身兼「已複製過了嗎」的 visited 標記與「複製品是誰」的查詢表；登記要在遞迴 neighbors 之前做，否則環繞回來查不到 |
