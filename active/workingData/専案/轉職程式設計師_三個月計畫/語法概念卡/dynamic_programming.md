# 動態規劃（Dynamic Programming, DP）

- 分類：解題思維框架
- 對應 C#：無直接語法對應，概念直接套用

> 複習時先看 Q，自己講一遍答案，再點開 `<details>` 對答案。
> 跟 [`recursion.md`](recursion.md) 是搭配關係：DP 通常從一個正確的遞迴關係式開始，再想辦法避免重複計算。

## 自我測驗

<details>
<summary>Q1. DP 解決的核心問題是什麼？</summary>

A1. 單純的遞迴（例如 `f(n) = f(n-1) + f(n-2)`）雖然邏輯正確，但同一個子問題（例如 `f(3)`）會在不同的呼叫路徑裡被**重複計算很多次**，導致時間複雜度變成指數等級（O(2ⁿ)）。DP 的核心就是：**把算過的子問題答案存起來，之後再遇到直接查表，不用重新遞迴**，把指數複雜度降回多項式（通常是 O(n)）。

</details>

<details>
<summary>Q2. 怎麼判斷一題該用 DP？</summary>

A2. 兩個特徵都符合，DP 是強烈候選：
1. **可以拆成遞迴關係式**：這一步的答案，可以用前面幾步的答案組合出來（例如「想最後一步是怎麼走的」）
2. **子問題會重複出現**（overlapping subproblems）：如果單純遞迴會不會有同一個子問題被算好幾次？如果會，就值得用 DP 記住答案

</details>

<details>
<summary>Q3. Memoization（記憶化）vs Tabulation（表格法），兩種做法差在哪？</summary>

A3.
- **Memoization（由上而下）**：維持原本遞迴的寫法，但加一個容器（陣列/`unordered_map`）記錄「這個子問題算過了嗎」，算過直接回傳存好的答案，不用重新遞迴
- **Tabulation（由下而上）**：不用遞迴，改用迴圈，從最小的子問題（base case）開始，依序往上算到目標，邊算邊存進陣列。Climbing Stairs 最終版本就是這種由下而上的思路，只是進一步把陣列簡化成兩個滾動變數

兩種殊途同歸，時間複雜度通常一樣，Tabulation 通常沒有遞迴呼叫的額外開銷（call stack），實務上常常更快、更省空間。

</details>

<details>
<summary>Q4. 什麼時候可以不用完整的陣列，只用幾個變數就夠？</summary>

A4. 如果這一步的答案**只依賴前面固定幾步**（例如 Climbing Stairs 只依賴前 2 步，不需要更早之前的），就不需要把整個歷史記錄都存進陣列，只要用幾個變數「滾動」記住最近需要的幾個值，空間複雜度可以從 O(n) 降到 O(1)。如果這一步的答案可能依賴任意更早的步驟，才需要完整的陣列/容器。

</details>

<details>
<summary>Q5. 「以目前位置結尾的最大和」這種 DP（Kadane's Algorithm）怎麼想？</summary>

A5. 核心遞迴關係式：`cur = max(nums[i], cur + nums[i])`——走到每個位置，只有兩種選擇：**接續前面累積的和**，或**放棄前面、從這個位置重新開始**，取較大的那個。另外用一個變數持續記錄「目前為止看過的最大值」：`maxSum = max(maxSum, cur)`。

```cpp
int cur = 0;
int maxSum = INT_MIN;

for (int i = 0; i < nums.size(); i++){
    cur = max(nums[i], cur + nums[i]);
    maxSum = max(maxSum, cur);
}
return maxSum;
```

跟 Climbing Stairs 一樣，這一步的答案只依賴「前一步累積的結果」，不需要完整陣列，兩個滾動變數（`cur`、`maxSum`）就夠，O(n) 時間、O(1) 空間。

另一種等價寫法（同一個遞迴關係式的不同記帳方式）：不用 `max(nums[i], cur+nums[i])`，改成「先無條件累加，如果累加後變負的就歸零」：
```cpp
currSum += val;
maxSum = max(maxSum, currSum);
if (currSum < 0) currSum = 0;
```
兩者數學上等價：`cur < 0` 時，`nums[i]` 一定比 `cur + nums[i]` 大，效果相同。

**`INT_MIN` 當安全初始值的技巧**：`maxSum` 要記錄「目前為止看過的最大值」，如果簡單粗暴設成 `0`，遇到「全部都是負數」的輸入會出錯（`0` 代表『什麼都不選』，但題目通常不允許空結果，`0` 反而會被誤判成比任何合法負數答案都大）。用 `<climits>` 提供的 `INT_MIN`（該型別能表示的最小值）當初始值，保證比任何合法輸入都小，**第一輪比較一定會被換掉**，不需要額外判斷「這是不是第一筆資料」的特殊分支。之後遇到「要找最大值，但不確定第一筆資料本身合不合法／陣列可能全負」的情境，都可以用這招取代「用 `nums[0]` 初始化 + 特殊判斷第一輪」的寫法。

</details>

## 完整筆記

Climbing Stairs 這題的完整演進路徑，可以當成理解 DP 的範例：

1. 先想出正確的遞迴關係式：`ways(n) = ways(n-1) + ways(n-2)`，base case `ways(0)=ways(1)=1`
2. 發現單純遞迴會重複計算（同一個子問題被呼叫好幾次），時間複雜度 O(2ⁿ)，題目給的 `n` 太大會超時
3. 想用容器記憶化（陣列/`unordered_map`），選容器時要考慮「需要存很多筆資料」這件事（見 [`container_selection.md`](container_selection.md)）
4. 意識到這一步只依賴前兩步，不需要完整陣列，用兩個滾動變數把空間壓到 O(1)

## 出現過的題目

| 題號 | 用法情境 |
|------|---------|
| 70 | Climbing Stairs：`ways(n)=ways(n-1)+ways(n-2)`，最終用兩個滾動變數取代陣列記憶化，達到 O(n) 時間、O(1) 空間 |
| 53 | Maximum Subarray（Kadane's Algorithm）：`cur=max(nums[i],cur+nums[i])` 判斷接續還是重新開始，`maxSum` 用 `INT_MIN` 初始化避免全負數輸入時被 `0` 誤判 |
