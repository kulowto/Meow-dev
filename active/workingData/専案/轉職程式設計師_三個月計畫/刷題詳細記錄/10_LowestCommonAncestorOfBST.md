# 235 Lowest Common Ancestor of a Binary Search Tree

- Key Cogitation：BST、Recursion
- Level：Medium
- 相關概念卡：[`語法概念卡/recursion.md`](../語法概念卡/recursion.md)、[`語法概念卡/order_vs_value.md`](../語法概念卡/order_vs_value.md)

> 同一題每次複習都在本檔案下方累加一段，不開新檔。用「跟上次相比」欄位追蹤盲點是否解決。

---

## 複習 #1 — 2026-08-17

- 狀態：有Bug
- 花費時間：30 分鐘

### 我的解法

```cpp
class Solution {
public:
    TreeNode* lowestCommonAncestor(TreeNode* root, TreeNode* p, TreeNode* q) {

        if(!root) return nullptr;

        if(root->val > p->val && root->val > q->val){
            return lowestCommonAncestor(root->left, p, q);
        }

        if(root->val < p->val && root->val < q->val){
            return lowestCommonAncestor(root->right, p, q);
        }

        return root;

    }
};
```

- 時間複雜度：平均 O(log n)（BST 高度），最壞情況（樹歪成一條鏈）O(n)
- 空間複雜度：O(log n)～O(n)（遞迴呼叫堆疊深度）

### 解題過程

#### 虛擬碼階段：一次就想對了核心邏輯

正確理解 BST 的順序性可以拿來優化搜尋方向後，虛擬碼一次就寫出「兩者都比 root 小往左、都比 root 大往右、其餘情況 root 就是答案」的核心邏輯，而且自己想通了「p 是 q 的祖先」這個邊界情況，其實已經被「其餘情況回傳 root」這個 else 分支自動涵蓋，不需要額外寫特殊判斷。

#### 真正卡住的地方：遞迴的思考方式，不是這題本身的邏輯

虛擬碼邏輯確定後，卡在「不知道何時該直覺想到用遞迴」——原本的直覺是「先找到 p、q 兩點，再往回推共同點」，這是迴圈式/手動搜尋式的思路，不是遞迴式思考。

透過討論釐清了關鍵心法：**Leap of Faith（信任的一躍）**——不需要在腦中把整個遞迴過程一層一層走過去驗證，只需要相信「呼叫自己處理更小的子問題，那個呼叫一定會給出正確答案」，自己這一層只需要負責「決定要不要把問題丟給誰」，以及「什麼情況下自己就是答案」。這個概念做成獨立概念卡 `recursion.md`。

#### 程式碼階段的兩個 bug

1. **判斷式重複比對 `p`，`q` 完全沒被檢查**：`if(root->val > p->val && root->val > p->val)` 兩次都寫成 `p->val`，`q->val` 一次都沒出現，方向判斷少考慮了 `q` 的位置
2. **遞迴呼叫的回傳值被丟掉，函式永遠回傳當下那一層的 `root`**：`lowestCommonAncestor(root->left, p, q);` 沒有用 `return` 接住結果，兩個 `if` 都沒有 return，最後統一執行 `return root;`——不管遞迴內部算出什麼，最外層永遠只會吐出自己那層的 `root`。用 `p=3, q=5`（正確答案應為 `4`）驗證，抓出實際回傳的是最外層的 `6`

### 1️⃣ 語法概念

- 遞迴呼叫如果要把結果當作整個函式的答案往上傳，一定要用 `return` 接住那次呼叫的結果，不能只是「呼叫但不使用回傳值」

### 2️⃣ 邏輯與複雜度

- 最終版本平均 O(log n)，是這題的標準解法，善用 BST 的順序性避免走訪整棵樹
- 「判斷式打錯成兩次同一個變數」這類錯誤（`p->val` 打了兩次，`q->val` 完全沒出現）容易在程式碼看起來「結構正確」時被忽略，寫完要逐行核對每個變數名稱是不是真的對應到該對應的東西

### 3️⃣ 演算法 / 資料結構盲點

- 這題再次驗證 BST 的順序性可以直接拿來優化搜尋方向，是 `order_vs_value.md` 框架的延伸應用
- **核心突破：學會辨識「這個問題套用在更小的同類子問題上，是不是完全一樣的問題」，是判斷該不該用遞迴的關鍵直覺**，並且理解「Leap of Faith」——遞迴時只需要處理「當下這一層該做什麼決定」，信任子問題的遞迴呼叫會給出正確答案，不需要在腦中手動追蹤整個遞迴過程

### 跟上次相比

（第一次複習，留空）
