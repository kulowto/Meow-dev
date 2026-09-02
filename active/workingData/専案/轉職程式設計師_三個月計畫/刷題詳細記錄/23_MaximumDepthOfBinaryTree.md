# 104 Maximum Depth of Binary Tree

- Key Cogitation：Tree DFS（節點數版本的深度，不需要成員變數）
- Level：Easy
- 相關概念卡：[`語法概念卡/recursion.md`](../語法概念卡/recursion.md)

> 同一題每次複習都在本檔案下方累加一段，不開新檔。用「跟上次相比」欄位追蹤盲點是否解決。

---

## 複習 #1 — 2026-09-02

- 狀態：有Bug
- 花費時間：30 分鐘

### 我的解法

```cpp
class Solution {
private:
    int DFS(TreeNode* root){

        if (root == nullptr){
            return 0;
        }

        int LnD, RnD;
        LnD = DFS(root->left);
        RnD = DFS(root->right);

        return max(LnD, RnD) + 1;
    }

public:
    int maxDepth(TreeNode* root) {
        if (root == nullptr){
            return 0;
        }else{
            return DFS(root);
        }
    }
};
```

- 時間複雜度：O(n)
- 空間複雜度：O(h)（h 為樹高，遞迴呼叫堆疊）

### 解題過程

#### 虛擬碼階段：套用上一題（Diameter）的邊數技巧,一開始繞了一圈

一開始沿用上一題「`node==nullptr` 回傳 `-1`」的邊數版本設計，並在根節點另外「再 +1」把邊數轉成節點數。經提問確認：這題本身要的答案就是節點數量的深度，不像 Diameter 需要邊數版本方便組合左右兩邊，不需要 `-1` 這個轉換，改成 `node==nullptr` 直接回傳 `0`，`max(Ln,Rn)+1` 公式不變，就是標準的節點數深度，不用再額外 `+1`。

#### 程式碼階段：三個問題依序修正

1. **最嚴重的一次**：一開始用「`root->left==nullptr && root->right==nullptr` 才算 base case」判斷葉節點，沒有先檢查 `root` 本身是不是 `nullptr`。用 `1 -> (right)2` 這種只有一邊子節點的樹 trace 出：`DFS(1)` 判斷式為 false（因為右邊不是 null），往下呼叫 `DFS(root->left)`（也就是 `DFS(nullptr)`），但函式內部沒有先檢查 `root==nullptr` 就直接用 `root->left`，對空指標取值是未定義行為。補上獨立的 `if(root==nullptr) return 0;` base case 放在最前面解決
2. 補上 `root==nullptr` base case 之後，原本判斷葉節點的 `if(root->left==nullptr||root->right==nullptr){...}` 整段，跟外面沒有子節點時的邏輯出現大量重複程式碼（`if` 內的 `else` 分支跟外面那段幾乎一模一樣），確認 `DFS(nullptr)` 本身已經安全回傳 `0`，不需要再額外判斷子節點是不是 `nullptr`，整段拿掉
3. 「葉節點特別回傳 `0`」這個判斷也是多餘的：拿掉之後，葉節點的 `LnD`、`RnD` 都會是 `DFS(nullptr)=0`，`max(0,0)+1=1`，自然算出正確的節點數深度，不需要特別處理，也讓 `maxDepth` 不用再額外 `+1`

### 1️⃣ 語法概念

- 對 `nullptr` 呼叫 `->` 是未定義行為，遞迴函式處理樹節點時，`root==nullptr` 的 base case 要放在最前面、獨立處理，不能只靠「檢查子節點是不是 null」代替

### 2️⃣ 邏輯與複雜度

- O(n) 時間、O(h) 空間，是這題最優解
- **base case 已經涵蓋的情況，不需要在呼叫端額外判斷一次**：只要 `DFS(nullptr)` 本身安全，呼叫者可以直接無條件呼叫 `DFS(root->left)`、`DFS(root->right)`，不用先檢查子節點是不是 null 才決定要不要呼叫——讓遞迴的 base case 自己處理邊界，呼叫端的邏輯才能保持單一、不用重複分支

### 3️⃣ 演算法 / 資料結構盲點

- 沿用上一題的技巧（`-1` 起始值）沒有先確認這題是否真的需要，是「套用上一題的解法而不重新檢視題目本身要求」的盲點，之後遇到看起來相似的題目，先確認這題真正要的輸出格式（節點數還是邊數），再決定要不要沿用之前的技巧
- 樹的遞迴少了 `root==nullptr` 這個最基本的 base case，導致訪問到未定義行為，是跟 `linked_list.md` 「對 nullptr 呼叫 `->` 是未定義行為」同一類坑，第一次在樹的題目上出現，之後遇到樹的遞迴要優先確認這個 base case 有沒有寫

### 跟上次相比

（第一次複習，留空）
