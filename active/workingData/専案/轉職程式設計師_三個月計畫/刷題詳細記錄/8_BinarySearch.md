# 704 Binary Search

- Key Cogitation：Binary Search
- Level：Easy
- 相關概念卡：[`語法概念卡/binary_search.md`](../語法概念卡/binary_search.md)

> 同一題每次複習都在本檔案下方累加一段，不開新檔。用「跟上次相比」欄位追蹤盲點是否解決。

---

## 複習 #1 — 2026-08-12

- 狀態：有Bug
- 花費時間：40 分鐘

### 我的解法

```cpp
int search(vector<int>& nums, int target) {

    int index_head = 0;
    int index_tail = nums.size();

    if (nums.size() == 0) {
        return -1;
    }

    while (index_head < index_tail) {

        int index_count = index_head + (index_tail - index_head) / 2;

        if (target == nums[index_count]) {
            return index_count;
        } else {
            if (index_tail == index_head + 1) {
                return -1;
            } else {
                if (target > nums[index_count]) {
                    index_head = index_count;
                } else {
                    index_tail = index_count;
                }
            }
        }

    }

    return -1;

}
```

- 時間複雜度：O(log n)（符合題目要求）
- 空間複雜度：O(1)

### 解題過程

一開始考慮過用 `unordered_map` 建值→index 的對照表，O(1) 查詢。討論後釐清：這題只呼叫一次，建 map 本身要 O(n)，整體會是 O(n)，不符合題目要求的 O(log n)——`unordered_map` 的優勢只在「同一份資料要被查詢很多次」時，靠攤提成本才划算，單次查詢用不到。確立方向後改用二分法，虛擬碼前後修了五輪：

1. **迴圈繼續條件寫反**：一開始寫 `while(index_tail == index_head+1)`，意思是「只有頭尾差 1 才進迴圈」，但初始範圍通常遠大於 1，導致迴圈幾乎不會執行，直接落到 `return -1`。用 `nums=[1,2,3,4,5], target=3` 驗證抓出這個問題
2. **算中間索引忘記加回 `index_head` 偏移量**：`nums[(index_tail-index_head)/2]` 只在 `index_head=0` 時剛好是對的，範圍縮小後這個算法會存取到完全不在搜尋範圍內的位置。用 `index_head=3, index_tail=5` 的情境驗證，正確算法應該是 `index_head + (index_tail-index_head)/2`
3. **括號位置前後不一致**：同一份虛擬碼裡，一行寫 `nums[(index_tail-index_head)/2]`（除法在中括號內，算索引），另一行卻寫成 `nums[index_tail-index_head]/2`（除法在中括號外，變成「用範圍長度當索引取值，再把值除以 2」），完全是另一件事
4. **`index_count` 只在迴圈外算一次，之後從未更新**：`index_head`／`index_tail` 被更新之後，`index_count` 卻沒有跟著重新計算，導致每一輪都拿舊的中間索引重複比對同一個值，`index_head` 卡住不動，變成無窮迴圈。用 `nums=[1,2,3,4,5,6,7], target=6` 逐輪驗證抓出這個問題，修正成把 `index_count` 的計算搬進迴圈裡面，每輪重算
5. **迴圈提早排除掉最後一個還沒檢查的元素**：改成 `while(index_tail != index_head+1)` 之後，範圍縮小到只剩一個元素時（`index_tail == index_head+1`），迴圈直接不執行，這個元素永遠沒被拿去比對。用單一元素陣列 `nums=[5], target=5` 驗證（預期回傳 `0`，實際回傳 `-1`）抓出這個問題；同時也發現迴圈內部那段「頭尾只差 1」的判斷式，因為外層條件已經先排除了這個情況，是永遠不會被執行到的死碼。最終改成 `while(index_head < index_tail)`，讓範圍剩一個元素時仍會進迴圈比對，才解決

### 1️⃣ 語法概念

- 二分法計算中間索引，要用 `index_head + (index_tail - index_head) / 2`，不能只算 `(index_tail - index_head) / 2`——範圍縮小後 `index_head` 不是 `0`，忘記加回偏移量會存取到範圍外的位置
- 中括號 `[]` 裡的運算跟中括號外的運算完全是兩件事，`arr[(a-b)/2]`（算索引）跟 `arr[a-b]/2`（取值後再除）容易因為括號位置抄錯而混淆，要仔細核對每一行的括號位置是否一致

### 2️⃣ 邏輯與複雜度

- 最終版本 O(log n) 時間、O(1) 空間，符合題目要求
- 這題再次踩到「追蹤用的變數（`index_count`）做完動作後忘記同步更新」這個坑，跟 Merge Two Sorted Lists（`tail` 指標）、Valid Parentheses（`while` 條件依賴的狀態）是同一種模式，已經是第三次出現，跨題目盲點彙總已更新
- 迴圈邊界條件（`while` 該用 `==`、`!=` 還是 `<`）決定了「範圍縮小到只剩一個元素時，這個元素會不會被檢查到」，這題示範了三種寫法（`==`、內層改`!=`、最終改`<`）分別會漏掉哪些情況，值得記住：**迴圈邊界條件要明確想清楚「最後一個候選值」有沒有被涵蓋進去**

### 3️⃣ 演算法 / 資料結構盲點

- 已釐清：`unordered_map` 的 O(1) 查詢優勢，只有在「同一份資料被多次查詢、建置成本能被攤提」時才划算；單次查詢的題目，建置成本本身就會拖垮總複雜度，直接用資料「已排序」的性質做二分法更好——這點呼應 `order_vs_value.md` 框架，但角度不同：這次不是「順序重不重要」，而是「有沒有必要額外建立輔助結構，還是能直接利用輸入本身的特性（已排序）」

### 跟上次相比

（第一次複習，留空）
