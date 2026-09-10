# range-based for（範圍型 for 迴圈）

- 分類：C++ 語法糖
- 對應 C#：`foreach (var x in collection)`

> 複習時先看 Q，自己講一遍答案，再點開 `<details>` 對答案。答錯或講不出來的，去下面「完整筆記」補。

## 自我測驗

<details>
<summary>Q1. 這是什麼？什麼情境下用？</summary>

A1. 「讓一個變數依序代表容器裡的每一個元素，每次迴圈換下一個」的簡潔寫法，對應 C# 的 `foreach`。不用自己管索引、不用寫 `i++`、不用判斷 `i < size()`。**只要不需要知道「這是第幾個元素」、也不需要跳著存取**，就用它，比傳統 `for (int i=0; i<v.size(); i++)` 加 `v[i]` 簡潔。

```cpp
for (Node* nb : node->neighbors) {
    // nb 依序是 neighbors[0]、neighbors[1]、...
}
```

</details>

<details>
<summary>Q2. 三種寫法（值 / 參考 / const 參考）差在哪？怎麼選？</summary>

A2.
```cpp
for (int x : v)          // 複製一份。改 x 不影響原容器。適合小元素（int、指標）、只讀
for (int& x : v)         // 參考，不複製。改 x 會改到容器裡的元素。要「修改容器內容」時用
for (const int& x : v)   // const 參考，不複製也不能改。適合大元素（string、vector、大 struct）、只讀
```
判斷準則：
- 元素小（`int`、指標）+ 只讀 → `for (T x : v)`
- 元素大（`string`、`vector`…）+ 只讀 → `for (const auto& x : v)`（避免每圈複製一份大東西）
- 要修改容器裡的元素 → `for (auto& x : v)`

</details>

<details>
<summary>Q3. 可以用在哪些容器？搭配結構化綁定怎麼寫？</summary>

A3. 任何支援 `begin()`/`end()` 的容器：`vector`、`array`、`string`、`map`、`set`、`unordered_map`、`unordered_set`。

搭配 `map` 系列時用結構化綁定拆出 key、value：
```cpp
for (auto& [k, v] : m) { ... }   // k 是 key，v 是 value
```
（見 [`unordered_map.md`](unordered_map.md) 的「range-based for 是語法糖」章節）

</details>

<details>
<summary>Q4. 常見的坑是什麼？</summary>

A4.
1. **`for (T x : v)` 時修改 `x` 不會影響 `v`**：`x` 是複製品，要改到容器內容必須用 `for (T& x : v)`
2. **迴圈裡對正在遍歷的容器 `push_back` / `erase` 是未定義行為**：range-based for 進行中不能改變容器大小（會導致 iterator 失效），要在迴圈外先收集、迴圈結束後再操作
3. 大物件忘記加 `const auto&`，每圈都默默複製一份，效能損失（編譯器不會報錯，只是變慢）

</details>

## 完整筆記

range-based for 背後等價於：
```cpp
for (auto it = v.begin(); it != v.end(); ++it) {
    auto& x = *it;
    // ...
}
```
「走到下一個元素」這個動作編譯器自動處理，不需要（也不能）自己額外寫遞增——這也是為什麼它比傳統 for 迴圈不容易寫錯（少一個「忘記 `i++`」或「邊界寫錯」的機會）。

## 出現過的題目

| 題號 | 用法情境 |
|------|---------|
| 242 | Valid Anagram：遍歷 `unordered_map` 比對字元計數，練習 iterator 與 range-based for 兩種寫法 |
| 133 | Clone Graph：`for (Node* nb : node->neighbors)` 遍歷每個鄰居遞迴複製，不需要索引、不修改原容器，range-based for 最簡潔 |
