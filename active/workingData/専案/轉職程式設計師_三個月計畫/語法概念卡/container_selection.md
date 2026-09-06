# 容器選擇速查表

- 分類：解題思維框架（查閱型，不是自我測驗型——這張卡是給你快速對照用，細節/原理去看各自的專屬概念卡）
- 對應 C#：容器概念大多對應（`List<T>`、`Dictionary<K,V>`），但「陣列大小是否編譯期固定」這件事 C# 沒有這麼嚴格的限制，是 C++ 特有的坑

> 這張卡不是自我測驗格式，是**決策對照表**：遇到「該用哪個容器」的疑問時直接查這張表，找到對應列後再連結去看詳細的專屬概念卡。

## 核心比對表

| 疑問 | 選 A | 選 B | 判斷依據 |
|------|------|------|---------|
| 陣列大小什麼時候決定？ | `std::array<T,N>` | `std::vector<T>` | 大小**編譯期**就固定 → `array`；大小要在**執行期**才知道、或之後可能變動 → `vector`。`N` 是變數（例如函式參數 `n`）就不能用 `array`，會編不過 |
| 只需要打包「兩個」值，還是要裝「很多組」資料？ | `pair<T1,T2>` | `unordered_map<K,V>` | 固定兩個值綁在一起（例如函式要回傳兩種資訊）→ `pair`；需要同時追蹤很多個不同 key 各自的資料 → `unordered_map`。細節見 [`unordered_map.md`](unordered_map.md) |
| 只需要判斷「這個值存不存在」，還是需要「對應的另一個資訊」？ | `unordered_set<T>` | `unordered_map<K,V>` | 只在乎有沒有出現過（例如判斷重複、記錄走訪過的節點）→ `unordered_set`，不用浪費一個用不到的 value 欄位；需要額外記錄次數/索引等對應資料 → `unordered_map`。細節見 [`unordered_set.md`](unordered_set.md) |
| 需要查詢的 key 種類多不多、範圍固不固定？ | 固定大小陣列（如 `int[26]`） | `unordered_map<K,V>` | key 種類**固定又少**（26 個字母、10 個數字這種）→ 陣列直接用 index 定位，比 hash map 快（不用算 hash、記憶體連續、無動態配置開銷）；key 種類不確定或很多 → `unordered_map`。詳見 [`unordered_map.md`](unordered_map.md) 的「key 種類固定且少時」章節 |
| 需要照 key 排序嗎？ | `map<K,V>` | `unordered_map<K,V>` | 需要遍歷時自動照 key 排序、或需要範圍查詢 → `map`（紅黑樹，O(log n)）；只在乎查詢快、不管順序 → `unordered_map`（hash table，O(1) 平均）。詳見 [`map.md`](map.md) |
| 需要保留原始順序，還是只在乎值本身？ | Stack / 雙指標 / 單一掃描 | Hash Map / 排序類結構 | 答案是否受「誰先誰後」影響？受影響 → 保留順序的做法；不受影響 → 依值查找的做法。完整判斷框架見 [`order_vs_value.md`](order_vs_value.md) |
| 需要 LIFO 還是 FIFO？ | `stack<T>` | `queue<T>`（或用兩個 stack 模擬） | 最近進去的先出來（巢狀、配對、回溯）→ Stack；最先進去的先出來 → Queue。詳見 [`stack.md`](stack.md)，用 Stack 實作 Queue 見 [`class_basics.md`](class_basics.md) |

跟 DP 記憶化容器的選擇一起看：[`dynamic_programming.md`](dynamic_programming.md)。

## 快速心法

1. **容器大小是不是變數決定的？** 是 → 別用 `array`，用 `vector`
2. **要存的是「一組」還是「很多組」資料？** 一組 → `pair`；很多組 → `map` 系列
3. **key 範圍小到可以直接數出來嗎（幾十個以內、固定）？** 可以 → 優先考慮陣列，不要預設用 hash map
4. **需要排序嗎？** 需要 → `map`；不需要 → `unordered_map`
5. **答案跟順序有沒有關係？** 用 [`order_vs_value.md`](order_vs_value.md) 判斷

## 出現過的題目

| 題號 | 用法情境 |
|------|---------|
| 383 | Ransom Note：一開始想用 `pair<char,int>`，被指出應該用 `unordered_map`；後來又學到 key 種類固定（26 字母）時用固定陣列比 `unordered_map` 更快 |
| 70 | Climbing Stairs：一開始想用 `std::array<int, n-1>` 做記憶化，但 `n` 是執行期變數，`array` 大小必須編譯期固定，該用 `vector`；最終用兩個滾動變數取代整個容器，把空間複雜度降到 O(1) |
| 409 | Longest Palindrome：52（大小寫字母種類數）是寫死的編譯期常數，符合 `array` 而非 `vector` 的使用時機，串連了「key 種類固定少→用陣列」跟「大小是常數→用 array」兩個教訓 |
| 169 | Majority Element：一開始又想到 `vector`／`Vector<char,int>`（pair 概念）裝「值＋次數」，繞了一圈才想到 `unordered_map`，第 3 次出現同一類猶豫 |
| 3 | Longest Substring Without Repeating Characters：參考解法把 `unordered_map<char,int>` 換成 `array<int,128>`（字元直接當索引，涵蓋整個 ASCII），比 `c-'a'` 偏移量轉索引的範圍更廣，同一個「key 種類固定且小→用陣列」原則的延伸應用 |
