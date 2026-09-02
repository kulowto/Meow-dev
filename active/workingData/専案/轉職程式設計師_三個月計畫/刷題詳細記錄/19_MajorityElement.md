# 169 Majority Element

- Key Cogitation：Hash Map（邊統計邊比對，提早回傳）
- Level：Easy
- 相關概念卡：[`語法概念卡/unordered_map.md`](../語法概念卡/unordered_map.md)、[`語法概念卡/container_selection.md`](../語法概念卡/container_selection.md)

> 同一題每次複習都在本檔案下方累加一段，不開新檔。用「跟上次相比」欄位追蹤盲點是否解決。

---

## 複習 #1 — 2026-08-27

- 狀態：有Bug
- 花費時間：60 分鐘

### 我的解法

```cpp
class Solution {
public:
    int majorityElement(vector<int>& nums) {

        unordered_map<int,int> st;
        int mc = nums.size()/2;

        for(int i = 0; i < nums.size(); i++){
            st[nums[i]]++;
            if(st[nums[i]] > mc){
                return nums[i];
            }
        }

        return -1;  // 理論上不會執行到，只是滿足編譯器要求
    }
};
```

- 時間複雜度：O(n)
- 空間複雜度：O(n)

### 解題過程

#### 虛擬碼階段：容器選擇繞了一圈才到 `unordered_map`

一開始想用 `vector` 儲存並邊存邊記次數，但沒說清楚 vector 裡存的是原始數值還是次數。被追問後改成 `Vector<char,int>`（想用 pair 概念存「值＋次數」），但這樣每次要更新某個值的次數得線性掃描整個 vector 找對應那筆，是 O(n) 查找。經提示回想起 Ransom Note、Longest Palindrome 學過的「要同時追蹤很多筆 key 對應的資料要用 `unordered_map`」，改用 `unordered_map<int,int>` 才是 O(1) 查詢/更新。

同時前一版邏輯裡多設計了一個「若都沒有超過 n/2，退回找等於 n/2 的值，可能回傳兩個結果」的分支，經提醒題目保證一定存在「次數 > ⌊n/2⌋」的多數元素、且函式回傳型別是單一 `int`，確認這個分支不可能發生也塞不進回傳型別，拿掉。

#### 程式碼階段：一開始型別寫錯 + 迴圈外缺 return

1. 一開始寫成 `unordered_map<char,int>`，跟題目 `vector<int> nums` 型別對不上，應為 `unordered_map<int,int>`
2. 迴圈跑完沒有觸發 return 時，函式沒有明確的 return 陳述式（未定義行為），雖然題目保證一定會在迴圈內 return、實務上不會發生，但補了 `return -1;` 滿足編譯器要求

### 1️⃣ 語法概念

- `unordered_map<int,int> st; st[nums[i]]++;` 一行完成「查有沒有出現、有就累加、沒有就設 1」，不存在的 key 存取時自動建立 `value=0`
- C++ 函式如果邏輯上「理論上」每條路徑都會 return，但編譯器分析不出來（例如依賴執行期才確定的迴圈一定會觸發 return），仍要補一個保底 `return`，否則是未定義行為

### 2️⃣ 邏輯與複雜度

- O(n) 時間、O(n) 空間；邊統計邊比對、一達到門檻就提早 return，不用等統計完再走訪一次找最大值，比「先統計完再找 max」更省一次迴圈
- `mc = nums.size()/2`（整數除法，等於 `⌊n/2⌋`），用 `st[nums[i]] > mc` 不論 n 奇偶都對應題目「次數 > ⌊n/2⌋」的定義，不用另外分奇偶討論

### 3️⃣ 演算法 / 資料結構盲點

- **又一次落入「多筆資料要用什麼容器裝」的猶豫**：先想到 vector、又想到 pair，才想到 unordered_map。第 3 次出現同一類容器選擇猶豫（Ransom Note、Climbing Stairs 之後），已在 `container_selection.md` 整理速查表，之後遇到「要同時追蹤很多筆 key 對應的資料」應該直接反射想到 `unordered_map`，不用繞一圈
- 誤設計了題目保證下不可能發生、且回傳型別也裝不下的分支，提醒之後先確認題目給的保證條件，再決定要不要處理某個邊界情況

### 跟上次相比

（第一次複習，留空）
