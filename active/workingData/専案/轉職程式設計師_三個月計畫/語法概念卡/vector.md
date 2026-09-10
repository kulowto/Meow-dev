# vector：維度與索引

- 分類：STL 容器（動態陣列）
- 對應 C#：`List<T>`；二維版本對應 `List<List<T>>`

> 複習時先看 Q，自己講一遍答案，再點開 `<details>` 對答案。答錯或講不出來的，去下面「完整筆記」補。
> 大小是否編譯期固定、跟 `array` 的取捨，見 [`container_selection.md`](container_selection.md)。

## 自我測驗

<details>
<summary>Q1. `vector<int>` 跟 `vector<vector<int>>`，索引層數差在哪？</summary>

A1.
```cpp
vector<int> a = {1, 2, 3};
int x = a[0];              // a[0] 直接是一個 int

vector<vector<int>> b = {{1,2},{3,4}};
int y = b[0][0];            // b[0] 是 vector<int>（=={1,2}），要再 [0] 一次才拿到 int
vector<int> row = b[0];     // b[0] 本身就是完整的一個 vector<int>
```
`vector<T>` 的 `[i]` 拿到的是「一個 `T`」。如果 `T` 本身又是 `vector<...>`，`[i]` 拿到的還是那整個 `vector`，要再 `[j]` 一次才拿到裡面的元素。**索引幾次，取決於宣告時巢狀了幾層 `vector<...>`，不是憑印象猜**——寫程式碼前先看函式簽名或變數宣告，確認清楚維度再動手，不要邊寫邊猜。

</details>

<details>
<summary>Q2. 兩個不同維度的 vector（例如一個 `vector<vector<int>>`、一個 `vector<int>`）要互相取值、比對，要注意什麼？</summary>

A2. 分開想清楚每個變數各自的維度，**不要因為它們代表同一種「概念」（都是區間）就套用同一種索引方式**：
```cpp
vector<vector<int>>& intervals;   // 一堆區間，intervals[i] 是一個區間（vector<int>），intervals[i][0]/[1] 才是 start/end
vector<int>& newInterval;          // 單一一個區間，newInterval[0]/[1] 直接就是 start/end，不需要再多一層
```
把整個 `newInterval`（而不是它的某個元素）放進 `vector<vector<int>>` 的結果裡，直接 `res.push_back(newInterval)`；如果錯拿了 `newInterval[0]`（一個 `int`）去 push，型別跟 `res` 期待的 `vector<int>` 對不上，編不過。

</details>

<details>
<summary>Q3. 常見的坑是什麼？</summary>

A3.
1. **維度算錯導致多索引或少索引一層**：把 `vector<int>` 當 `vector<vector<int>>` 用（多套一層 `[]`），或反過來（該用 `[i][j]` 卻只寫了 `[i]`），都會編不過或型別不符
2. **傳參數用 `&`（reference）時，函式內部修改會直接影響呼叫端的原始變數**：`vector<int>& nIntv` 這種寫法，函式裡對 `nIntv[0]` 賦值，呼叫這個函式的地方傳進來的原始變數也會被跟著改掉，不是函式內部的獨立副本
3. `vector.size()` 回傳的是 `size_t`（unsigned），跟 `int` 比較或相減時要留意型別，避免無號數運算下溢的問題（例如 `size()-1` 在 `size()==0` 時會變成一個超大的正數，不是 `-1`）

</details>

<details>
<summary>Q4. 常用操作有哪些？</summary>

A4.
```cpp
vector<int> v;
v.push_back(x);          // 加到尾端
v.size();                 // 元素數量（size_t）
v.empty();                 // 是否為空
v[i];                      // 索引存取，不檢查邊界（超出範圍是未定義行為）
v.at(i);                   // 索引存取，超出範圍會丟例外
for (int x : v) { }        // range-based for
```

</details>

<details>
<summary>Q5. `auto [x, y] = v;` 這種結構化綁定，能用在 `vector` 上嗎？</summary>

A5. 不行。結構化綁定只能用在**編譯期就知道固定有幾個元素**的型別上，例如 `pair`、`tuple`、`array`，或成員數量固定的 struct。`vector` 是**執行期才決定大小**的動態容器，編譯器沒辦法保證「這個 vector 一定剛好有幾個元素」，所以不支援這個語法，寫了會編不過。

```cpp
pair<int,int> p = {1, 2};
auto [x, y] = p;              // 合法，pair 大小固定為 2

vector<int> v = {1, 2};
auto [x, y] = v;               // 不合法，vector 大小是動態的，編不過

int x = v[0];                   // 要拿 vector 裡的值，用一般索引
int y = v[1];
```

</details>

<details>
<summary>Q6. `vector<vector<int>>` 想用某個索引（例如樹的深度）直接存取，但不確定這個索引存不存在，該怎麼補足大小？</summary>

A6. `vector` 不會自動長大到容納某個索引，`v[i]` 對超出目前 `size()` 的索引存取是未定義行為。要先確保 `size()` 夠大：

```cpp
while (v.size() <= idx) {
    v.push_back({});   // 一次補一格，直到夠用為止
}
v[idx].push_back(x);
```

**只用 `if` 檢查一次是不夠的**：如果 `idx` 一次比目前 `size()` 大超過 `1`（例如 `size()=0` 但 `idx=1`），`if` 只會補一次（讓 `size()` 變成 `1`），還是不夠存取 `v[1]`。要用 `while`（或直接 `resize(idx+1)`）確保無論差距多少都能一次補足。

</details>

<details>
<summary>Q7. 遞迴傳遞索引/深度這種參數時，`depth++` 跟 `depth+1` 差在哪？</summary>

A7. `depth++` 是**後置遞增**，除了「回傳目前的值當參數」，還會**修改 `depth` 這個變數本身**（副作用）。如果同一個函式呼叫裡多次用到 `depth++`（例如分別傳給 `DFS(left, depth++)` 跟 `DFS(right, depth++)`），第二次呼叫拿到的值會是「已經被第一次呼叫悄悄加過 1」的值，兩次子呼叫拿到的深度會不一樣（都不是你要的「父節點深度+1」），而且函式結束後想用 `depth` 記錄自己這一層時，這個變數也已經被改過好幾次，不再代表原本的深度。

只是想「算出一個新的值傳給子呼叫，但不改動自己手上的 `depth`」，直接用 `depth+1`（一般加法，沒有副作用）就好，不要用 `depth++`。

</details>

## 完整筆記

遇到多維 `vector`（尤其函式簽名裡同時出現 `vector<T>` 跟 `vector<vector<T>>` 兩種參數，例如區間類題目常見 `vector<vector<int>>& intervals` 搭配 `vector<int>& newInterval`）時，**先花一句話確認每個變數各自的維度，再開始寫索引**，不要憑「感覺上都是同一種東西」就套用同一套 `[i][j]` 寫法。這種混淆比單純的 off-by-one 更容易讓人卡很久，因為型別錯誤有時候要等到編譯或執行才會發現，不像邏輯錯誤可以用具體例子直接 trace 出來。

## 出現過的題目

| 題號 | 用法情境 |
|------|---------|
| 57 | Insert Interval：`intv` 是 `vector<vector<int>>`、`nIntv` 是 `vector<int>`，一開始把 `nIntv` 誤當二維操作（`nIntv[0][0]`），也誤把 `nIntv[0]`（單一 int）push 進期待 `vector<int>` 的結果陣列，撞牆許久後全部砍掉重寫才一次處理好 |
| 973 | K Closest Points to Origin：`p[i]` 是 `vector<int>`，一開始想用 `auto [x,y]=p[i];` 結構化綁定取值，確認 vector 不支援後改用一般索引 `p[i][0]`/`p[i][1]` |
| 102 | Binary Tree Level Order Traversal：DFS 遞迴傳遞深度時誤用 `depth++`（副作用改動自己手上的深度），改成 `depth+1`；`rtn[depth]` 存取前用 `while(rtn.size()<=depth) push_back({})` 補足大小，只用 `if` 補一次不夠 |
