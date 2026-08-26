# stack

- 分類：STL 容器（容器配接器，Container Adapter，LIFO）
- 對應 C#：`Stack<T>`（但 C# 的 `Pop()` 有回傳值，C++ 沒有，這是最大差異）

> 複習時先看 Q，自己講一遍答案，再點開 `<details>` 對答案。答錯或講不出來的，去下面「完整筆記」補。
> 這是「保留順序」家族的代表，跟 [`order_vs_value.md`](order_vs_value.md) 的判斷框架一起複習。

## 自我測驗

<details>
<summary>Q1. 這是什麼？什麼情境下會想到用它？</summary>

A1. 後進先出（LIFO）的容器。看到「最近發生的事要最先被處理/關閉」——巢狀、配對、順序相關的題目（例如括號配對），第一直覺要想到 Stack，而不是統計數量或排序。

</details>

<details>
<summary>Q2. 核心操作有哪些？</summary>

A2.
```cpp
st.push(x);      // 放到最上面
st.pop();         // 移除最上面的元素，沒有回傳值！
st.top();         // 讀最上面的元素，不移除
st.empty();       // 是否為空
st.size();        // 元素數量
```

</details>

<details>
<summary>Q3. 常見的坑是什麼？</summary>

A3.
1. `pop()` **不回傳值**，跟 C# 的 `Stack<T>.Pop()` 不一樣。想拿到值要先 `top()` 讀，再 `pop()` 丟掉。
2. 對空 stack 呼叫 `top()` 或 `pop()` 是**未定義行為**，不會幫你檢查、也不會丟例外。任何呼叫前一定要先 `if (!st.empty())` 檢查。
3. 沒辦法用 index 或迭代器看中間元素，只能碰最上面那顆——如果發現自己想「看中間第幾個」，代表這題可能不該用純 stack。

</details>

<details>
<summary>Q4. 時間/空間複雜度？</summary>

A4. `push`、`pop`、`top`、`empty` 全部 O(1)。底層預設用 `deque` 實作。

</details>

## 完整筆記

`stack` 是容器配接器，本質上把底層容器（預設 `deque`）的介面限制成「只能動最上面」。刻意設計成這樣，就是為了強制你只能照 LIFO 順序操作，天生就保留了「發生順序」的資訊——這也是為什麼順序相關的題目會直接對應到它，見 [`order_vs_value.md`](order_vs_value.md)。

## 出現過的題目

| 題號 | 用法情境 |
|------|---------|
| 20 | Valid Parentheses：左括號 push 進 stack，右括號跟 stack 頂端比對，不對或 stack 空就 false；跑完 stack 要為空才是 true |
| 232 | Implement Queue using Stacks：兩個 stack 互相搬移模擬 FIFO，見 [`class_basics.md`](class_basics.md) |
