# 278 First Bad Version

- Key Cogitation：Binary Search（在單調布林序列上找第一個 True）
- Level：Easy
- 相關概念卡：[`語法概念卡/binary_search.md`](../語法概念卡/binary_search.md)

> 同一題每次複習都在本檔案下方累加一段，不開新檔。用「跟上次相比」欄位追蹤盲點是否解決。

---

## 複習 #1 — 2026-08-21

- 狀態：有Bug
- 花費時間：1 小時

### 我的解法

```cpp
// The API isBadVersion is defined for you.
// bool isBadVersion(int version);

class Solution {
public:
    int firstBadVersion(int n) {
        int head = 0;
        int tail = n;
        int mid;

        while( head+1 < tail ){

            mid = head + (tail - head)/2;

            if( isBadVersion(mid) == true ){
                tail = mid;
            }else{
                head = mid;
            }

        }

        return tail;

    }
};
```

- 時間複雜度：O(log n)
- 空間複雜度：O(1)

### 解題過程

#### 虛擬碼階段

一開始用具體例子（`F F F F T`、`F F F T T`、`F F T T T` 三種情境）手動推導規則，抓出一個核心邏輯錯誤：一開始設計「往左搜尋停下來回傳 `head`、往右搜尋停下來回傳 `tail`」，這個規則會依照「從哪個方向走過來」給出不同答案，用 `F F F T T` 驗證會誤判成回傳 `3`（實際上位置 3 是 False，不可能是答案）。修正成統一規則：**`head` 永遠代表確定是 False 的位置，`tail` 永遠代表確定是 True 的位置，兩者相鄰時固定回傳 `tail`**，不依賴搜尋方向。

#### 程式碼階段的連環問題

1. **回傳型別跟布林值搞混**：一開始邊界處理寫「`n == False` 直接回傳 False」，混淆了「這題回傳的是版本編號（int）」跟「isBadVersion 回傳 bool」這兩件事
2. **`mid` 計算忘記加回 `head` 偏移量**：`mid = (tail-head)/2`，跟 Binary Search（704）踩過的坑一模一樣，這是第 2 次犯同一個錯誤，已經記進跨題目盲點彙總
3. **拿 `head`、`tail`（int）直接跟布林值比較**：`head == false`，`head` 是版本編號不是布林值，這樣寫迴圈條件永遠不成立，迴圈完全不會執行
4. **把「該停止」的狀態當成「該繼續」的條件**：`while(head == tail-1)` 這種寫法，把頭尾相鄰（該結束的時刻）當成迴圈繼續執行的條件，方向整個反了，改成 `while(head+1 < tail)` 才對
5. **迴圈內殘留了永遠不會觸發、或者更嚴重會提早回傳錯誤答案的 `if` 判斷**：一開始留了一個帶 `head==tail-1` 的判斷式（因為外層迴圈條件已經保證不可能發生，是死碼，但白白多呼叫兩次 `isBadVersion`，違反題目「減少呼叫次數」的要求）；拿掉 `head==tail-1` 後只剩 `isBadVersion(head)==false && isBadVersion(tail)==true`，這兩個條件其實是「head/tail 該一直維持的性質」，幾乎每輪都成立，導致函式在還沒真正縮小範圍前就提早回傳了錯誤答案（用 `F F F T T` 驗證，一進迴圈就誤判回傳 `5`，正確答案是 `4`）。最後確認這整段判斷從一開始就是多餘的，全部刪除才解決
6. **邊界情況：如果第一個壞版本剛好是版本 1**：`head` 一開始設成 `1`，但如果 `bad=1`，`head=1` 從一開始就不符合「確定是 False」這個自訂規則。用 `n=2, bad=1`（序列 `T,T`）驗證，`head=1` 時迴圈直接不執行、回傳錯誤的 `tail=2`。修正成 `head` 初始值設為 `0`（版本編號不存在的虛擬位置，保證「確定 False」這個性質從一開始就成立，不用擔心版本 `1` 本身是不是壞的）

### 1️⃣ 語法概念

- `mid = head + (tail - head) / 2`，不能只算 `(tail-head)/2`，這是第 2 次犯這個錯誤
- 布林值（`isBadVersion()` 的回傳值）跟數字（版本編號）是完全不同的東西，不能互相比較或混用

### 2️⃣ 邏輯與複雜度

- 最終版本 O(log n)，符合題目要求
- 二分法「找第一個 True」這類題目，`head`/`tail` 初始值的選擇要特別注意邊界：`head` 要設成一個「保證確定是 False」的虛擬位置（這題是 `0`，比最小合法版本號小 1），不能直接用第一個合法值當初始值，否則答案剛好落在邊界時會出錯

### 3️⃣ 演算法 / 資料結構盲點

- 這題是「在單調布林序列裡找第一個 True」這個二分法變體的標準題，跟一般在數字陣列裡找目標值的二分法（704）本質相同，只是判斷條件從「數值大小比較」換成「呼叫 API 拿布林結果」，核心的縮小範圍邏輯完全一樣

### 跟上次相比

（第一次複習，留空）
