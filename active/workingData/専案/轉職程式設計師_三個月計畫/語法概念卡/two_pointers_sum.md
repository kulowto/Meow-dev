# 排序 + 雙指標找目標和（K-Sum 家族）

- 分類：解題思維框架（雙指標的另一種應用）
- 對應 C#：無直接語法對應，是思考套路

> 複習時先看 Q，自己講一遍答案，再點開 `<details>` 對答案。答錯或講不出來的，去下面「完整筆記」補。
> 跟 [`sliding_window.md`](sliding_window.md) 都是雙指標家族，差異：滑動視窗處理「連續子字串/子陣列」，這張卡處理「陣列裡任意幾個數字加起來等於某個目標值」。

## 自我測驗

<details>
<summary>Q1. 什麼時候該想到「排序 + 雙指標」？</summary>

A1. 題目要求「陣列裡找幾個數字，加起來等於某個目標值」（Two Sum 的變形：3Sum、4Sum 等），且**不要求保留原始順序**（找到的答案本身順序不重要）時，先排序陣列，再用雙指標從頭尾往中間逼近，比雙迴圈暴力枚舉快很多。

</details>

<details>
<summary>Q2. 核心結構長什麼樣？以 3Sum 為例</summary>

A2.
```cpp
sort(nums.begin(), nums.end());

for (int i = 0; i < nums.size(); i++) {
    if (i > 0 && nums[i] == nums[i-1]) continue;   // 跳過重複的「固定值」

    int target = -nums[i];
    int left = i + 1, right = nums.size() - 1;

    while (left < right) {
        int sum = nums[left] + nums[right];
        if (sum == target) {
            ans.push_back({nums[i], nums[left], nums[right]});
            left++;
            while (left < right && nums[left] == nums[left-1]) left++;   // 跳過重複值
        } else if (sum < target) {
            left++;
        } else {
            right--;
        }
    }
}
```
固定第一個數字（用一層迴圈依序選），剩下兩個數字在排序好的區間裡用雙指標找。

</details>

<details>
<summary>Q3. 為什麼不需要額外判斷「陣列太短、指標會不會超出範圍」這種邊界？</summary>

A3. `while(left < right)` 這個條件本身就已經涵蓋了「範圍不夠大」的情況——如果 `i` 太靠近尾端，導致 `left`、`right` 一開始就不滿足 `left < right`，這個 `while` 迴圈根本不會執行，不會有任何存取越界的風險。**先確認後面的邏輯本身有沒有天然涵蓋某個邊界，再決定要不要額外寫特殊判斷**，不要習慣性地多加一層檢查（3Sum 一開始多寫了一個 `if(idx > size-2) break` 的「尾段判斷」，其實完全不需要）。

</details>

<details>
<summary>Q4. 找到目標值之後，「跳過重複值」的比較方向容易搞錯，怎麼判斷該跟誰比？</summary>

A4. 移動指標之後，要跟**剛剛已經用過的值**比較，不是跟**還沒用過的下一個值**比較：

```cpp
left++;
while (left < right && nums[left] == nums[left-1]) left++;   // 跟 left-1（剛用過的值）比，不是 left+1
```

`left++` 之後，`left-1` 正是「剛剛被拿去記錄過組合的位置」。如果新的候選值（`nums[left]`）跟它一樣，代表拿去配對只會產生內容重複的組合，該跳過。如果誤用 `nums[left]==nums[left+1]`（跟還沒處理過的下一個值比），問的其實是完全不同的問題（「這個值後面是不是還有一個一樣的」），沒辦法阻止重複組合產生。`right` 那邊同理，方向相反（跟 `right+1` 比）。

</details>

<details>
<summary>Q5. 找到目標值後，需要同時移動 `left++` 跟 `right--` 嗎？</summary>

A5. 不一定，只動 `left`（或只動 `right`）也是正確的，兩種寫法都可以。因為陣列排序過，只移動 `left++` 之後，`nums[left]` 一定 `>=` 剛剛那個值，下一輪比較只會是「相等（找到新的一組）」或「太大（正常的 `right--` 邏輯會自己接手）」，不會出現「太小」的情況——原本的比較邏輯自然能處理後續，不需要在找到目標值時勉強兩邊都動。跟哪邊配合「跳過重複值」，就看你選擇移動哪一側。

</details>

<details>
<summary>Q6. 這個技巧本身踩過什麼 C++ 語言層級的坑？</summary>

A6. **同一個運算式裡，不能一邊修改一個變數、一邊又讀取它**：曾經寫過 `while(nums[left++] == nums[left])`，`left++` 修改了 `left`，緊接著同一行的 `nums[left]` 又讀取了它——C++ 沒有規定 `==` 兩邊誰先求值，這是未定義行為，不能依賴任何看起來「有效」的結果。要拆成獨立的敘述句：先做比較、再視情況移動指標，不要在同一個運算式裡又改又讀同一個變數。

</details>

## 完整筆記

跟 [`order_vs_value.md`](order_vs_value.md) 的判斷框架呼應：這類題目「答案本身的順序不重要」（找到哪幾個數字就好，回傳順序不限），所以排序陣列（打亂原始順序）完全沒問題，換來雙指標的效率。這跟「保留順序」家族（Stack、單一掃描）是相反的取捨方向。

## 出現過的題目

| 題號 | 用法情境 |
|------|---------|
| 15 | 3Sum：排序 + 固定第一個數字 + 雙指標找剩下兩數之和，搭配跳過重複的固定值（外層）與跳過重複的 left/right 值（內層） |
