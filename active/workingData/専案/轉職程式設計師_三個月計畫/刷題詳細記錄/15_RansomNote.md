# 383 Ransom Note

- Key Cogitation：Hash Map
- Level：Easy
- 相關概念卡：[`語法概念卡/unordered_map.md`](../語法概念卡/unordered_map.md)、[`語法概念卡/order_vs_value.md`](../語法概念卡/order_vs_value.md)

> 同一題每次複習都在本檔案下方累加一段，不開新檔。用「跟上次相比」欄位追蹤盲點是否解決。

---

## 複習 #1 — 2026-08-24

- 狀態：有Bug
- 花費時間：30 分鐘

### 我的解法

```cpp
unordered_map <char, int> um;

for(int i = 0 ; i < ransomNote.length() ; i++){
    if(um.count(ransomNote[i]))
        um[ransomNote[i]]++;
    else
        um[ransomNote[i]] = 1;
}

for (auto& [key,value] : um){

    int count = 0;

    for(int i = 0; i < magazine.length() ; i++){
        if(magazine[i] == key){
            count++;
        }
    }

    if ( count < value ){
        return false;
    }
}

return true;
```

- 時間複雜度：O(k×m)（k 是 `ransomNote` 裡不同字元種類數，m 是 `magazine` 長度，每種字元都要重新掃一次 `magazine`）
- 空間複雜度：O(k)

### 解題過程

#### 虛擬碼/設計階段

正確理解這題跟 Valid Anagram 的差異（單向檢查「夠不夠用」，不是雙向完全相等），一開始想用 `pair<char,int>` 統計字元次數，被指出 `pair` 只能裝「一組」資料，這題需要同時追蹤很多種不同字元各自的次數，屬於「很多組」的情境，改用 `unordered_map<char,int>`（複習了 `pair` 跟 `unordered_map` 的差異：`pair` 是固定兩個值的小容器，`unordered_map` 內部其實就是用很多個 `pair` 組成的）。

#### 程式碼階段的問題

1. **統計次數的 if-else 判斷式寫反了**：一開始「已經出現過」執行 `= 1`（蓋掉之前累積的次數），「第一次出現」執行 `++`——兩個分支剛好對調，導致重複出現的字元次數永遠統計成 1。用 `ransomNote = "aa"` 驗證抓出這個問題，修正成「已出現過就 `++`，沒出現過就設成 1」
2. **多餘的重複查詢**：在已經用結構化綁定 `for (auto& [key,value] : um)` 拿到 `value` 的情況下，又額外呼叫一次 `um.find(key)` 重新查一遍，是多餘的
3. **變數作用域錯誤**：`int v` 宣告在 `if(it != um.end()){ ... }` 區塊裡面，區塊結束後在外面使用會編不過（跟第 2 點是同一段多餘程式碼造成的，拿掉多餘查詢後這個問題也一併解決）
4. `unordered_map` 打字錯誤（少了 `ed`）

### 1️⃣ 語法概念

- `unordered_map` 計數的 if-else 判斷，寫反方向是這次卡最久的地方：「已存在」對應累加、「不存在」對應初始化成 1，這個對應關係要想清楚方向，或者直接用 `um[key]++`（不存在會自動建立 `value=0` 再 `++`）省掉整段 if-else，減少寫反的機會
- 結構化綁定 `for (auto& [key,value] : um)` 已經直接給出 key 對應的 value，不需要再額外呼叫 `find` 重新查一次

### 2️⃣ 邏輯與複雜度

- 目前版本 O(k×m)，正確但不是最優解，見「可加強空間」

### 3️⃣ 演算法 / 資料結構盲點

- 這題跟 Two Sum、Valid Anagram 是同一類「需要統計/比對次數」的題目，`order_vs_value.md` 框架適用（順序不重要，直接用 Hash Map）

### 可加強空間

- **兩邊都建 `unordered_map`，不要對其中一邊做線性掃描**：目前對 `ransomNote` 的每個字元，都重新把整個 `magazine` 掃一遍數次數，變成 O(k×m)。如果 `magazine` 也先建一個 `unordered_map<char,int>` 統計好，之後只要對 `ransomNote` 的 map 逐一比對兩邊的次數即可，可以把複雜度降到 O(n+m)：
  ```cpp
  unordered_map<char, int> noteCount, magCount;
  for (char c : ransomNote) noteCount[c]++;
  for (char c : magazine) magCount[c]++;

  for (auto& [key, value] : noteCount) {
      if (magCount[key] < value) return false;
  }
  return true;
  ```

- **字元種類固定且少時，用固定大小陣列取代 `unordered_map`，比 hash map 更快**：這題字元限定小寫英文字母（只有 26 種可能），可以直接用 `c - 'a'` 轉成 `0`~`25` 的索引，不需要 hash 機制：
  ```cpp
  int count[26] = {0};

  for (char c : magazine) {
      count[c - 'a']++;
  }

  for (char c : ransomNote) {
      count[c - 'a']--;
      if (count[c - 'a'] < 0) {
          return false;
      }
  }

  return true;
  ```
  時間複雜度一樣是 O(n+m)，但常數因子小很多：陣列用 index 直接定位不用算 hash、記憶體連續 cache 命中率高、不像 `unordered_map` 有動態配置記憶體的開銷。**判斷準則：key 的種類數量固定且很少時（例如 26 個字母、10 個數字），優先考慮陣列取代 `unordered_map`**；key 種類不確定或數量可能很大，才需要 `unordered_map` 的彈性。這個技巧額外把「兩邊分開統計再比對」簡化成「一邊建陣列、另一邊邊減邊檢查是否小於 0」，少寫一次迴圈

### 跟上次相比

（第一次複習，留空）
