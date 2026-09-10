# 217 Contains Duplicate

- Key Cogitation：Hash Set（邊走訪邊查重複）
- Level：Easy
- 相關概念卡：[`語法概念卡/unordered_map.md`](../語法概念卡/unordered_map.md)（unordered_set 章節）、[`語法概念卡/container_selection.md`](../語法概念卡/container_selection.md)

> 同一題每次複習都在本檔案下方累加一段，不開新檔。用「跟上次相比」欄位追蹤盲點是否解決。

---

## 複習 #1 — 2026-09-02

- 狀態：限時內完成
- 花費時間：10 分鐘

### 我的解法

```cpp
class Solution {
public:
    bool containsDuplicate(vector<int>& nums) {

        unordered_set<int> s;

        for (int i = 0; i < nums.size() ; i++){
            if( s.count(nums[i])){
                return true;
            }
            s.insert(nums[i]);
        }

        return false;
    }
};
```

- 時間複雜度：O(n)
- 空間複雜度：O(n)

### 解題過程

#### 虛擬碼階段：一次就想對

自己直接想出「開一個容器記錄看過的值，插入前先查有沒有出現過，有就回傳 true，沒有就存進去，走訪完都沒觸發就回傳 false」的邏輯，一次到位。

#### 容器選擇：第一次用到 unordered_set

一開始猶豫 `pair` 還是 `vector`，主動要求複習可用的容器。這題只需要判斷「值存不存在」，不需要額外配對的資訊，屬於 `unordered_set` 的使用時機（跟需要配對次數/索引的 `unordered_map` 不同），第一次實際用到這個容器（相關內容在 `unordered_map.md` 的 unordered_set 章節）。

#### 額外討論：Big-O 好但實測比較慢

送出後看到別人的「排序 + 掃相鄰元素」解法（O(n log n)）實測比自己的 O(n) `unordered_set` 版本跑得快，討論後理解是常數因子的差異：hash table 每次操作要算 hash、處理碰撞、動態配置記憶體（cache miss 多），排序後的 `vector` 連續記憶體、`std::sort` 本身高度優化，LeetCode 測資規模下常數因子的影響常常蓋過理論複雜度的差距。

### 1️⃣ 語法概念

- `unordered_set<T>`：只存值本身，沒有 key-value 配對，`insert`/`count`/`find`/`erase`，沒有 `[]` 運算子（這點跟 `unordered_map` 不同）

### 2️⃣ 邏輯與複雜度

- O(n) 時間、O(n) 空間，理論上是這題最優解（比排序版本的 O(n log n) 更好），但實測常數因子較大，跑分不一定比排序版本快——Big-O 只講成長趨勢，不代表小到中等資料量下誰的實際跑分比較快

### 3️⃣ 演算法 / 資料結構盲點

- 這題容器選擇最終判斷對了（`unordered_set` 而非 `pair`/`vector`），沒有落入之前反覆出現的猶豫；補齊了「只需要判斷存在、不需要配對資訊」這個判斷準則的實際應用經驗

### 跟上次相比

（第一次複習，留空）
