# 53 Maximum Subarray

- Key Cogitation：Dynamic Programming（Kadane's Algorithm）
- Level：Medium
- 相關概念卡：[`語法概念卡/dynamic_programming.md`](../語法概念卡/dynamic_programming.md)

> 同一題每次複習都在本檔案下方累加一段，不開新檔。用「跟上次相比」欄位追蹤盲點是否解決。

---

## 複習 #1 — 2026-09-02

- 狀態：有Bug
- 花費時間：30 分鐘

### 我的解法

```cpp
class Solution {
public:
    int maxSubArray(vector<int>& nums) {

        int cur, maxSum;

        cur = 0;
        maxSum = INT_MIN;

        for(int i = 0; i < nums.size(); i++){
            cur = max(nums[i], cur + nums[i]);
            if (cur > maxSum){
                maxSum = cur;
            }
        }

        return maxSum;
    }
};
```

- 時間複雜度：O(n)
- 空間複雜度：O(1)

### 解題過程

#### 虛擬碼階段：自己動手 trace 推導出 Kadane's Algorithm

一開始想用遞迴，對每個位置各自往左右兩邊重新加總比對，經提問點出這樣會有大量重複計算。改用一次由左到右的走訪，自己動手把範例陣列 `-2 1 -3 4 -1 2 1 -5 4` 逐位 trace「接續前面的和」還是「從這裡重新開始」，親自推導出 `cur = max(nums[i], cur+nums[i])` 這個遞迴關係式，等同標準的 Kadane's Algorithm，沒有被直接告知答案。

#### 程式碼階段：全負數的邊界情況

第一版把 `maxSum` 初始化成 `0`，送出後在全負數輸入（如 `[-3,-1,-2]`）出錯：`0` 代表「什麼都不選」，但題目要求子陣列至少一個元素，全負數情況下「不選」的 `0` 反而被誤判成比任何合法答案都大，回傳 `0` 而不是正確的 `-1`。

先改成 `if(i==0) maxSum=nums[i];` 用第一筆資料當初始值解決，之後看到別人的解法用 `INT_MIN` 取代，理解到用型別能表示的最小值當初始值可以保證第一輪比較一定會被換掉，不需要額外的 `i==0` 特殊判斷分支，改用這個寫法。

#### 額外討論：另一份參考解法跑分較快

看到另一份用 `currSum += val; if(currSum<0) currSum=0;` 的寫法，討論後確認這是同一個遞迴關係式的等價寫法（`cur<0` 時 `nums[i]` 一定比 `cur+nums[i]` 大），跟自己的版本邏輯上沒有實質差異，不像上次 hash set vs 排序有明確的架構級原因，跑分差異較可能是判題機雜訊。

### 1️⃣ 語法概念

- `INT_MIN`（`<climits>`）：該型別能表示的最小值，適合當「保證會被第一筆合法資料取代」的安全初始值，取代「用 `nums[0]` 初始化 + 額外判斷第一輪」的寫法

### 2️⃣ 邏輯與複雜度

- O(n) 時間、O(1) 空間，是這題最優解（Kadane's Algorithm）
- 核心遞迴關係式 `cur = max(nums[i], cur+nums[i])`：這一步只依賴前一步的結果，屬於「只依賴前面固定幾步」的 DP，只需要滾動變數，不需要完整陣列或遞迴

### 3️⃣ 演算法 / 資料結構盲點

- 累加/比較用的變數，初始值選得不夠謹慎時，容易讓「不合法的選項」（這題是『什麼都不選』的 `0`）意外變成預設候選答案，之後遇到「找最大/最小值」類題目，要先想清楚初始值會不會不小心引入一個不該存在的合法候選

### 跟上次相比

（第一次複習，留空）
