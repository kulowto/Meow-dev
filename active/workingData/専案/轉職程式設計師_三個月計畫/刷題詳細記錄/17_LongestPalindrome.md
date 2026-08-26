# 409 Longest Palindrome

- Key Cogitation：Array（固定大小陣列統計次數）
- Level：Easy
- 相關概念卡：[`語法概念卡/container_selection.md`](../語法概念卡/container_selection.md)

> 同一題每次複習都在本檔案下方累加一段，不開新檔。用「跟上次相比」欄位追蹤盲點是否解決。

---

## 複習 #1 — 2026-08-26

- 狀態：限時內完成（使用者主張程式碼階段的問題純屬打字失誤，非邏輯或語法誤用；虛擬碼階段有兩處靠討論修正——漏乘 2、容器選 vector 還是 array，已提醒但使用者維持此判定）
- 花費時間：30 分鐘

### 我的解法

```cpp
class Solution {
public:
    int longestPalindrome(string s) {

        std::array<int,52> store = {0};

        int count = 0;

        for(int i = 0; i <s.length() ; i++){

            int index;

            if(islower(s[i])){
                index = s[i] - 'a';
            }

            if(isupper(s[i])){
                index = s[i] - 'A' + 26;
            }

            store[index]++;

            if(store[index]>=2){
                count = count + 2;
                store[index] = store[index]%2;
                // 這種算法，邊界不會超過2
            }
        }

        for(int index = 0 ; index < store.size() ; index++){
            if( store[index] == 1){
                return count + 1;
            }
        }

        return count;

    }
};
```

- 時間複雜度：O(n)
- 空間複雜度：O(1)（固定 52 大小陣列，不隨輸入變化）

### 解題過程

#### 虛擬碼階段

一開始想通「偶數次的字元兩兩成對放兩側、奇數次的字元用掉大部分配對後剩一個可以放中間」的核心洞察。但公式一開始漏乘 2：把「配對數」直接當成「長度」，用 `"abccccdd"` 驗證（正確答案 7，公式算出 4）抓出少了「每對佔用 2 個字元位置」這個轉換，修正成 `2 × count + (1 或 0)`。

#### 容器選擇：串連 Ransom Note 跟 Climbing Stairs 兩個舊教訓

一開始想用 `vector` 開 52 個空間，經提問後想通：52 是寫死的常數（不會因輸入變化），符合 `array` 的使用時機，不是 `vector` 的（`vector` 適合大小要看執行期資料決定的情境）。同時也應用了 Ransom Note 學到的「字元種類固定又少 → 用陣列不用 hash map」。

#### 程式碼階段：兩個打字錯誤

1. `std::Array` 大寫開頭，應為小寫 `std::array`
2. 判斷大小寫轉索引時，變數名打成沒宣告過的 `c`，應該用迴圈裡的 `s[i]`

### 1️⃣ 語法概念

- `islower()`/`isupper()`（`<cctype>`）判斷大小寫，搭配 `s[i] - 'a'` / `s[i] - 'A' + 26` 把字元轉成 0~51 的索引，是 Ransom Note `c - 'a'` 技巧的延伸（多一組大寫，用 `+26` 避免跟小寫索引重疊）

### 2️⃣ 邏輯與複雜度

- O(n) 時間、O(1) 空間，是這題的最優解
- **邊累加邊配對**的寫法（`store[index]>=2` 就直接算進 `count` 並歸零）比「統計完再統一算」更精簡，一次迴圈同時完成統計跟配對，不用事後再走訪一次算配對數

### 3️⃣ 演算法 / 資料結構盲點

- 這題再次驗證「字元種類固定且少 → 優先用陣列而非 hash map」的判斷準則（`container_selection.md`），也再次用到「大小是編譯期常數 → 用 array 不用 vector」的判斷（Climbing Stairs 學到的）

### 跟上次相比

（第一次複習，留空）
