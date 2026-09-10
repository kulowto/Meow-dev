# 133 Clone Graph

- Key Cogitation：Graph DFS + Hash Map（原節點→複製品對照表）
- Level：Medium
- 相關概念卡：[`語法概念卡/range_based_for.md`](../語法概念卡/range_based_for.md)、[`語法概念卡/unordered_map.md`](../語法概念卡/unordered_map.md)、[`語法概念卡/class_basics.md`](../語法概念卡/class_basics.md)

> 同一題每次複習都在本檔案下方累加一段，不開新檔。用「跟上次相比」欄位追蹤盲點是否解決。

---

## 複習 #1 — 2026-09-10

- 狀態：有Bug
- 花費時間：90 分鐘

### 我的解法

```cpp
class Solution {
private:
    unordered_map<Node*, Node*> mp;   // 原節點 → 複製品

public:
    Node* cloneGraph(Node* node) {

        if(node == nullptr){
            return nullptr;
        }

        if(mp.find(node) != mp.end()){
            return mp[node];
        }else{
            Node* clone = new Node(node->val);
            mp[node] = clone;

            for(Node* nb : node->neighbors){
                clone->neighbors.push_back(cloneGraph(nb));
            }

            return clone;
        }
    }
};
```

- 時間複雜度：O(V + E)（每個節點、每條邊各處理一次）
- 空間複雜度：O(V)（map + 遞迴呼叫堆疊）

### 解題過程

#### 虛擬碼階段：從「兩階段」收斂到「單次 DFS 同時建立與串接」

一開始設想「先數出所有節點、全部 `new` 出來 → 再 DFS 走訪一遍記錄結構到容器 → 再用容器結構串接新節點」的三階段做法。經提問釐清三點：
1. 光「數出節點、new 出來」不夠，串接 neighbors 時需要「原節點 → 複製品」的對照，要用 `unordered_map<Node*, Node*>`（key 用位址而非 `val`，不依賴「值唯一」的假設）
2. 環不需要特別偵測——只要檢查「這個原節點是否已經在 map 裡」，已經在就直接回傳現成的複製品，同時解決「環無限遞迴」跟「同一節點被複製多次」兩個問題
3. 不需要兩階段，一次 DFS 走到每個節點時就同時「建立複製品 + 串接 neighbors 的複製品」

看了三角形圖（有環）的逐步示範 trace 後理解整個流程。

#### 程式碼階段：多輪除錯，集中在 C 類語法問題

1. `return new Node*()`：空圖直接 `return nullptr` 即可，`new Node*()` 是想 new 一個指標型別，語法不對
2. `mp` 一開始宣告成 `cloneGraph` 的區域變數：這題 `cloneGraph` 遞迴呼叫自己，區域變數每次呼叫都重置成空 map，「已複製過了嗎」的紀錄存不住——跟 Linked List Cycle 踩過的「共用狀態不能宣告成會被重置的區域變數」同一類坑。改成 class 成員變數（這題是真的需要跨遞迴共用狀態的正當情況，跟第 30 題「不需要卻用了」相反）
3. `mp[clone] = node->neighbors`：key、value、型別三個都錯——key 應為 `node`（原節點），value 應為 `clone`（複製品，型別 `Node*`），不是 `node->neighbors`（`vector<Node*>`）。正確為 `mp[node] = clone`
4. `clone` 宣告在 `else` 區塊裡，`for` 迴圈跟 `return clone` 在區塊外，看不到 `clone`——把 `return clone` 移進 `else` 區塊
5. 遍歷 `neighbors` 的寫法：`neightbors` 拼字錯誤（兩處）、`for(Node* nb = node->neighbors;)` 語法錯誤（vector 不能賦值給單一指標）。改用 range-based for `for(Node* nb : node->neighbors)`，中間還多打了一個分號要拿掉

### 1️⃣ 語法概念

- range-based for（`for(T x : container)`）：對應 C# 的 `foreach`，不用管索引，適合「只要依序處理每個元素、不需要知道是第幾個」的情境，已整理成 `range_based_for.md`
- `clone->neighbors.push_back(...)`：`clone` 是指標，用 `->` 進到節點內部取 `neighbors` 這個 vector，再對它 `push_back`

### 2️⃣ 邏輯與複雜度

- O(V+E) 時間、O(V) 空間，是這題最優解
- **「原節點 → 複製品」的 hash map 同時扮演兩個角色**：既是「已經複製過了嗎」的 visited 標記，又是「複製品是哪一個」的查詢表。這種一個結構身兼兩職的設計，跟 Two Sum 的 `seen[value]=index`（既記錄出現過、又記錄在哪）是同一種精神
- **登記 `mp[node] = clone` 一定要在遞迴 neighbors 之前做**：否則環繞回來時，`mp.find(node)` 查不到，會再 new 一個新的、無限遞迴

### 3️⃣ 演算法 / 資料結構盲點

- 第一次遇到「圖」的複製/走訪類題目，直覺想用「多階段、先全部建立再串接」的做法，其實用一次 DFS 搭配 hash map 就能同時完成建立與串接。之後遇到「複製/轉換一個有環的結構」，優先想「用 hash map 記錄『原 → 新』的對照，DFS 一次走完」
- 這題的成員變數 `mp` 是「正當使用」的案例（跨遞迴共用狀態），跟第 30 題「不需要卻用了」正好相反——判斷準則還是那句：這個值需不需要跨函式呼叫或跨遞迴層次持續存在

### 跟上次相比

（第一次複習，留空）
