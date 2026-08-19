# 242 Valid Anagram

- Key Cogitation：Hash Map
- Level：Easy
- 相關概念卡：[`語法概念卡/unordered_map.md`](../語法概念卡/unordered_map.md)、[`語法概念卡/order_vs_value.md`](../語法概念卡/order_vs_value.md)

> 同一題每次複習都在本檔案下方累加一段，不開新檔。用「跟上次相比」欄位追蹤盲點是否解決。

---

## 複習 #1 — 2026-08-11

- 狀態：超時
- 花費時間：30 分鐘

### 我的解法

```cpp
class Solution {
public:
    bool isAnagram(string s, string t) {

        if ( s.length() == 0 && t.length() == 0){
            return true;
        }
        if( s.length() != t.length()){
            return false;
        }

        unordered_map <char, int> sM, tM;

        for (int i = 0; i < s.length() ; i++){
            if( sM.find(s[i]) != sM.end()){
                sM[s[i]]++;
            }else{
                sM[s[i]] = 1;
            }
        }

        for (int i = 0; i < t.length() ; i++){
            if( tM.find(t[i]) != tM.end()){
                tM[t[i]]++;
            }else{
                tM[t[i]]=1;
            }
        }

        for(auto &[key, value]: sM){
            if(tM.find(key) == tM.end()){
                return false;
            }else{
                if(tM[key] != value){
                    return false;
                }
            }
        }

        return true;

    }
};
```

- 時間複雜度：O(n)
- 空間複雜度：O(n)（兩個 hash map）

### 解題過程

這題整體卡的地方不多，主要是題意理解跟語法細節，虛擬碼邏輯一次就設計對了：

- **題意理解**：一開始把 anagram 誤解成「字數一致但排序必須不同」，多加了「順序一定要不一樣」這個不存在的條件，用 `s="aa", t="aa"`（順序相同也算 anagram）釐清後修正
- **虛擬碼設計**：一次就想到用 `unordered_map` 而不是 `map`（有回頭對照自己做的 `order_vs_value.md` 框架，判斷這題順序不重要），也主動想到「其中一方 key 不存在」這個邊界情況要額外處理
- **語法練習**：主動要求同時練習「iterator 手動走訪」跟「range-based for」兩種寫法，兩版邏輯完全等價，都驗證過

### 1️⃣ 語法概念

- `sM[c]++`：`unordered_map` 的 `operator[]` 對不存在的 key 會自動建立 `value=0` 的 entry，再做 `++` 就變成 `1`——可以取代「先查有沒有出現、再決定要新增還是累加」的 if-else 判斷
- **range-based for 是語法糖**：`for (auto& [k,v] : m)` 背後等價於 `for (auto it = m.begin(); it != m.end(); ++it)`，「往下一個元素走」這個動作由編譯器自動處理，不需要、也不能自己額外寫遞增
- **iterator 的比較運算子限制**：`vector` 的 iterator 是 random access iterator，支援 `<`、`+`、`-`；`unordered_map`／`map` 的 iterator 只是 forward iterator，只支援 `==`／`!=`，不支援 `<`——底層是 hash table，沒有「誰在誰前面」這種可比較大小的概念

### 2️⃣ 邏輯與複雜度

- O(n) 時間、O(n) 空間，是這題的標準解法
- 已驗證：因為前面已經確保 `s.length() == t.length()`，只需要單方向比對 `sM` 的每個 key 是否都能在 `tM` 找到且次數相同，就足以保證兩邊完全一致（不需要再反向比對 `tM` 有沒有 `sM` 沒有的 key）

### 3️⃣ 演算法 / 資料結構盲點

- 這題是 `order_vs_value.md` 框架「順序不重要」類型的典型應用，主動聯想到 `unordered_map`，這個框架已經內化，沒有卡住

### 跟上次相比

（第一次複習，留空）
