# 973 K Closest Points to Origin

- Key Cogitation：排序（`pair<距離,索引>` + `sort`）
- Level：Medium
- 相關概念卡：[`語法概念卡/vector.md`](../語法概念卡/vector.md)

> 同一題每次複習都在本檔案下方累加一段，不開新檔。用「跟上次相比」欄位追蹤盲點是否解決。

---

## 複習 #1 — 2026-09-05

- 狀態：有Bug
- 花費時間：60 分鐘

### 我的解法

```cpp
class Solution {
private:

    int x,y;

    int pSumOfSquares(vector<int>& p){
        x = p[0];
        y = p[1];

        return (x * x)+(y * y);
    }

public:
    vector<vector<int>> kClosest(vector<vector<int>>& p, int k) {

        vector<pair<int,int>> store; // {d, index}
        vector<vector<int>> res;

        for(int i = 0; i < p.size() ; i++){
            store.push_back({pSumOfSquares(p[i]),i});
        }

        sort(store.begin(), store.end());

        for(int i = 0; i < k ; i++){
            auto [d, index] = store[i];

            res.push_back(p[index]);
        }

        return res;
    }
};
```

- 時間複雜度：O(n log n)
- 空間複雜度：O(n)

### 解題過程

#### 虛擬碼階段：一次到位

自己直接想出「算出每個點的距離平方值、跟原始索引綁在一起、排序後取前 K 個」的完整邏輯，沒有卡住。主動確認了距離平方（不用開根號）就足以比較大小、`pow`/`sqrt` 語法，以及 `pair` 排序的預設行為（先比 `.first` 再比 `.second`）。

#### 程式碼階段：語法問題（vector 不支援結構化綁定）

一開始想用 `auto [x, y] = p[i];` 從 `p[i]`（型別是 `vector<int>`）直接拆出 `x`、`y`，主動詢問後確認 `vector` 是執行期才決定大小的動態容器，不支援結構化綁定（結構化綁定只能用在編譯期就知道固定元素個數的型別，例如 `pair`、`tuple`、`array`），改用一般索引 `p[i][0]`、`p[i][1]` 取值。後續在 `store[i]`（型別是 `pair<int,int>`）上使用 `auto [d, index] = store[i];` 則正確，能看出已經記住兩者的差異。

### 1️⃣ 語法概念

- 結構化綁定（`auto [a,b] = x;`）只能用在編譯期固定元素個數的型別（`pair`、`tuple`、`array`、固定成員數的 struct），`vector` 是動態容器不支援，已補進 `vector.md`
- `pair<T1,T2>` 的預設排序規則：先比 `.first`，`.first` 相等再比 `.second`，把要排序的依據放在 `.first` 就能直接用 `sort` 不用寫比較函式
- 平方優先用 `x*x` 而非 `pow(x,2)`（更快、不用處理浮點指數運算）；只需要比較距離大小時，`sqrt` 是嚴格遞增函式，可以省略開根號直接比較平方和

### 2️⃣ 邏輯與複雜度

- O(n log n) 時間（排序）、O(n) 空間，是常見的標準解法
- 更優的做法是用 heap（`priority_queue`，大小維持在 `k`）做法可以把時間複雜度降到 O(n log k)，當 `k` 遠小於 `n` 時比排序全部再取前 K 個更省，之後刷到 heap／priority_queue 相關題目時可以回來對照

### 3️⃣ 演算法 / 資料結構盲點

- `pSumOfSquares` 把 `x`、`y` 設計成成員變數，但這兩個值只在函式內部使用、不需要跨呼叫保留狀態，改成函式內的區域變數更合適（成員變數應該保留給「真的需要跨函式呼叫或跨遞迴層次共用」的狀態，這題不需要，是前幾題「該用成員變數卻沒用」的相反案例——這次是不需要用卻用了）

### 跟上次相比

（第一次複習，留空）
