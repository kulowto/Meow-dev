# 1 Two Sum

- Key Cogitation：Hash Map
- Level：Easy

> 同一題每次複習都在本檔案下方累加一段，不開新檔。用「跟上次相比」欄位追蹤盲點是否解決。

---

## 複習 #1 — 2026-08-06

- 狀態：有Bug
- 花費時間：15 分鐘

### 我的解法

```cpp
class Solution {
public:
    vector<int> twoSum(vector<int>& nums, int target) {

        for( int i=0 ; i < nums.size() ; i++ ){
            for( int j=i+1; j < nums.size() ; j++ ){
                if( (nums[i] + nums[j]) == target ){
                    return vector<int>({i,j});
                }
            }
        }

        return vector<int>();

    }
};
```

- 時間複雜度：O(n²)
- 空間複雜度：O(1)

### 1️⃣ 語法概念

- `return vector<int>({i,j});` 是用 initializer list 建構子建立 vector；`{i,j}` 是 C++11 大括號初始化語法，本身不是容器
- 因為 return type 已經是 `vector<int>`，可以簡化成 `return {i, j};`，不需要手動再包一層 `vector<int>(...)`
- 對照 C#：類似 `return new List<int> { i, j };`，但 C++ 能靠 return type 推導型別，省略 `new`/型別名稱

### 2️⃣ 邏輯與複雜度

- 雙層迴圈暴力解，時間複雜度 O(n²)，n 大時會明顯變慢
- 邏輯正確，找不到解時回傳空 vector（題目保證有解，這裡沒問題）

### 3️⃣ 演算法 / 資料結構盲點

- 沒用到 `unordered_map`，屬於這題最大的盲點：「配對/互補」類問題（看到 `target - nums[i]` 這種形式）第一直覺應該想到 Hash Map 查表
- 正解版本：

```cpp
class Solution {
public:
    vector<int> twoSum(vector<int>& nums, int target) {
        unordered_map<int,int> seen; // value -> index

        for (int i = 0; i < nums.size(); i++) {
            int need = target - nums[i];
            if (seen.count(need)) {
                return {seen[need], i};
            }
            seen[nums[i]] = i;
        }
        return {};
    }
};
```

- 時間複雜度 O(n)，空間複雜度 O(n)
- `unordered_map` 對應 C# 的 `Dictionary<TKey,TValue>`：`seen[key] = value` 存值、`seen.count(key)` 判斷是否存在（C# 是 `ContainsKey`）、`seen[key]` 取值

### 跟上次相比

（第一次複習，留空）

---

## 複習 #2 — 2026-08-08

- 狀態：超時（研究 `unordered_map` 用法花了較久時間，未精確計時）
- 花費時間：超時，實際分鐘數未記錄

### 我的解法

```cpp
class Solution {
public:
    vector<int> twoSum(vector<int>& nums, int target) {

        unordered_map <int,int> umap;

        for(int i=0; i < nums.size() ; i++ ){
            int comp = target - nums[i];
            if(umap.find(comp)!=umap.end()){
                return {umap[comp], i};
            }
            umap[nums[i]] = i;
        }
        return{};
    }
};
```

- 時間複雜度：O(n)
- 空間複雜度：O(n)

### 除錯過程

改寫成 `unordered_map` 版本中途卡了幾輪：

1. **變數名打錯**：`int comp = target - num[i];` 少了 `s`，`num` 跟宣告的 `nums` 對不上，編不過
2. **回傳型別錯誤**：一開始寫 `return;`，但函式回傳型別是 `vector<int>`，不能空 return，要改成 `return {};`
3. **邏輯漏掉核心一步**：只寫了查詢（`umap.find`），完全忘記把值存進 `umap`——導致 `umap` 從頭到尾是空的，查詢永遠找不到東西。這是這次卡最久的地方，因為知道語法（`umap[key]=value`）不等於知道「什麼時候該用它、用意是什麼」
4. **想清楚「先查後存」的順序**：一開始沒意識到存值的位置會影響正確性。如果先存再查，當 `target` 剛好是某數字的兩倍時，會查到自己剛存進去的那筆，錯誤地拿自己的 index 配對自己。確認後把「存值」放在「查詢」之後，兩者順序正確

### 1️⃣ 語法概念

- `umap.find(key) != umap.end()`：`find` 找不到時回傳的 iterator 會等於 `end()`，這是判斷「有沒有找到」的標準寫法，跟 `count(key)` 效果一樣但只查一次表
- `umap[nums[i]] = i;` 是「邊掃邊記」的核心動作：key 存看過的數字本身，value 存它的 index，之後才有東西可以查

### 2️⃣ 邏輯與複雜度

- 單一迴圈，時間複雜度 O(n)，比複習 #1 的 O(n²) 雙層迴圈好一個等級
- 空間複雜度 O(n)（最壞情況全部數字都要存進 `umap`），這是用空間換時間換來的

### 3️⃣ 演算法 / 資料結構盲點

- 這次真正卡住的不是「不會寫語法」，而是「不理解語法背後要達成的目的」——知道 `umap[key]=value` 怎麼寫，但沒想到「查詢前要先有東西可查」這件事需要自己主動存值。之後遇到 Hash Map 相關題目，可以先問自己：「我要查的東西，是不是要先有人把它存進去？」

### 跟上次相比

- 上次的盲點（沒想到用 `unordered_map`）這次解決了：主動選了 `unordered_map` 來寫
- 新出現的問題：從「知道要用什麼工具」進步到「還不熟工具的正確使用時機跟順序」——這是更細一層的卡點，比上次的盲點更進階，也算是進步的訊號
