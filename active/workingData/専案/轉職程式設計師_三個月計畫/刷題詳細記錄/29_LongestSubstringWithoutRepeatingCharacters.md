# 3 Longest Substring Without Repeating Characters

- Key Cogitation：滑動視窗（Sliding Window）+ `unordered_map`
- Level：Medium
- 相關概念卡：[`語法概念卡/sliding_window.md`](../語法概念卡/sliding_window.md)、[`語法概念卡/unordered_map.md`](../語法概念卡/unordered_map.md)

> 同一題每次複習都在本檔案下方累加一段，不開新檔。用「跟上次相比」欄位追蹤盲點是否解決。

---

## 複習 #1 — 2026-09-07

- 狀態：有Bug
- 花費時間：90 分鐘

### 我的解法

```cpp
class Solution {
public:
    int lengthOfLongestSubstring(string s) {

        unordered_map<char,int> store; // {char, index}

        int maxCount = 0;
        int count = 0;
        int left = 0;

        if(s.length()==0){
            return 0;
        }

        for(int idx = 0; idx < s.length(); idx++){

            if(store.find(s[idx]) != store.end() ){
                if( left > store[s[idx]]){
                    left = left;
                }else{
                    left = store[s[idx]] + 1;
                }

                store[s[idx]] = idx;
            }else{
                store[s[idx]] = idx;
            }

            count = (idx - left) + 1;

            if(count > maxCount){
                maxCount = count;
            }

        }

        return maxCount;
    }
};
```

- 時間複雜度：O(n)
- 空間複雜度：O(min(n, 字元集大小))

### 解題過程

這題經歷了兩套完全不同的實作路線，最終送出的是路線二（滑動視窗）。

#### 虛擬碼階段：從「容器」構想逐步收斂

一開始構想「用計數器記錄目前連續幾個字元符合條件，遇到重複就歸零重來」，用具體反例（`"abba"`：如果歸零重來會誤判後面的 `a` 又重複）點出「跟整個字串所有出現過的字元比對」跟「只跟目前這段連續片段裡出現過的字元比對」是不同的事。

接著提出「遇到重複時，把定位點設成剛好遇到重複的位置、整個容器清空重來」，用 `"abcadef"` 反例（正確答案 `6`：`"bcadef"`）點出這樣會把不衝突的 `b`、`c` 也一併丟掉，答案偏小算成 `4`。修正成「只移除到上次那個重複字元出現的位置為止，不整個清空」，重新用 `"abcadef"` 驗證答案變成正確的 `6`。

#### 路線一（探索用，未送出）：`unordered_map` + 一邊迭代一邊 `erase`

依照「移除舊資料」的構想直接動手實作，用 `unordered_map<char,int>` 記錄每個字元的位置，遇到重複時掃過整個 map，把位置小於等於重複點的 entry 全部 `erase` 掉。除錯過程：

1. **C 類**：迴圈變數用未宣告的 `i`、少一個右括號、`earse` 拼字錯誤、`store[iter]` 誤用（`iter` 已經是 iterator，不能再包一層 `store[]`）、`reg`（iterator）直接跟數字做 `>=` 比較（iterator 不支援大小比較，跟 `unordered_map.md` 已記錄的坑同類）
2. **A 類（邊界）**：迴圈條件 `idx < s.length()-1` 搭配 `idx==s.length()-2` 當「尾部判斷」，用 `"abc"` trace 出最後一個字元根本沒被處理到，答案算成 `1`。改成迴圈跑滿 `s.length()`，迴圈外統一補一次比較
3. **A 類（iterator 失效）**：`for(iter...; iter++){ if(...) store.erase(iter->first); }`——`erase` 會讓 `iter` 失效，緊接著的 `iter++` 是未定義行為。修正成 `iter = store.erase(iter)` 搭配 `else` 分支手動 `++iter`
4. **A 類（另一個 iterator 也可能失效）**：獨立變數 `reg`（`store.find(s[idx])` 的 iterator）如果在迴圈中途被同一個迴圈 erase 掉自己指到的 entry，`reg` 也會失效。修正成迴圈開始前先把 `reg->second` 這個數字取出來存成普通變數，不要在迴圈裡持續依賴這個 iterator

這條路線邏輯修正後用 `"abcabcbb"`、`"pwwkew"` 驗證都算出正確答案，但因為設計上要「掃過整個 map 刪除過期資料」，效率不如路線二（最壞情況退化到 O(n²)），主動決定不送出，改採路線二重新設計。相關坑已整理進 `unordered_map.md` Q5。

#### 路線二（送出版）：`left` 索引 + 不刪除、只用範圍過濾

改用「不物理刪除 map 裡的舊資料，只維護一個 `left` 索引代表目前視窗起點，查詢時判斷『上次出現位置是否 `>= left`』來過濾過期紀錄」的設計。第一版漏了兩個地方：

1. `left = store[s[idx]]`（少 `+1`）：用 `"abba"` 的 `idx=2` trace 出視窗仍包含造成重複的字元本身，答案偏大
2. 沒有判斷「上次出現位置是否還在視窗內」：直接無條件把 `left` 設成上次出現位置，用 `"abba"` 的 `idx=3` trace 出讀到過期的舊紀錄（位置 `0`，早已被 `left=1` 排除在外），導致 `left` 錯誤地往回移動，答案算錯成 `4`

改成 `if(left > store[c]) 保持不變; else left = store[c]+1;`（等同 `left = max(left, store[c]+1)`），用 `"abba"`、`"abcadef"`、`"abcabcbb"`、`"pwwkew"` 四個例子驗證後確認邏輯正確，送出測試。

### 1️⃣ 語法概念

- 一邊迭代 `unordered_map` 一邊 `erase`：`iter = store.erase(iter)` 搭配手動控制遞增，不能用 `for` 迴圈自帶的 `iter++`；獨立持有的其他 iterator 若可能被同一輪迭代影響，要先把需要的值取出來存成普通變數，已整理進 `unordered_map.md` Q5

### 2️⃣ 邏輯與複雜度

- O(n) 時間、O(min(n,字元集大小)) 空間，是這題最優解（滑動視窗）
- **`left = max(left, 上次出現位置+1)` 是這個套路的核心公式**：`+1` 是為了排除造成重複的字元本身；跟 `left` 比較大小（而非無條件覆蓋）是為了避免過期紀錄讓 `left` 往回移動
- 路線一（掃 map 找過期資料刪除）在功能上也能做到正確結果，但每次重複都要掃一次整個 map，最壞情況 O(n²)；路線二用索引比較取代物理刪除，是同一個問題「不用真的清除資料、用範圍過濾代替」思路的體現，跟 Insert Interval 的「提早 break」有異曲同工之妙——找出資料本身具備的性質（這裡是『只要比較索引就知道是否過期』），用比較取代真正的操作

### 3️⃣ 演算法 / 資料結構盲點

- 第一次遇到「找最長連續不重複片段」類題目，直覺想到的是物理維護一個容器/清除機制，而不是「用索引框住範圍、靠比較過濾過期資料」這種更輕量的做法。之後遇到「連續子字串/子陣列 + 某個條件」類題目，優先考慮滑動視窗（雙指標），已整理進新概念卡 `sliding_window.md`
- 這題示範了同一個邏輯目標（排除過期/不需要的資料）可以用「物理刪除」或「範圍過濾」兩種方式達成，效能差異很大，之後設計資料結構操作時，先問自己「有沒有辦法用比較/索引取代真正的刪除/搬移動作」

### 跟上次相比

（第一次複習，留空）
