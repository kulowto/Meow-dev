# 110 Balanced Binary Tree

- Key Cogitation：Binary Tree、Recursion
- Level：Easy
- 相關概念卡：[`語法概念卡/recursion.md`](../語法概念卡/recursion.md)

> 同一題每次複習都在本檔案下方累加一段，不開新檔。用「跟上次相比」欄位追蹤盲點是否解決。

---

## 複習 #1 — 2026-08-18

- 狀態：有Bug
- 花費時間：1 小時

### 我的解法

```cpp
class Solution {
public:
    bool isBalanced(TreeNode* root) {
        return checkBalanced(root).second;
    }

private:
    pair<int, bool> checkBalanced (TreeNode* root){

        int countHight;
        bool isBalanced = true;

        pair<int, bool> leftNode, rightNode;

        // BaseCase
        if ( root == nullptr ){

            countHight = -1;
            // leafNode = 0, 1 + max(-1, -1) = 0

            isBalanced = true;
            return {countHight, isBalanced};
        }

        leftNode = checkBalanced(root->left);
        rightNode = checkBalanced(root->right);

        countHight = 1+max(leftNode.first, rightNode.first);

        if( leftNode.second == false ||  rightNode.second == false ){
            isBalanced = false;
        }else{
            if( leftNode.first > rightNode.first ){
                if ((leftNode.first-rightNode.first) > 1){
                    isBalanced = false;
                }
            }else if( leftNode.first < rightNode.first ){
                if (( rightNode.first - leftNode.first) > 1){
                    isBalanced = false;
                }
            }
        }

        return {countHight, isBalanced};

    }
};
```

- 時間複雜度：O(n)（每個節點只被 `checkBalanced` 呼叫一次，高度計算跟平衡檢查在同一次遞迴完成）
- 空間複雜度：O(h)（遞迴呼叫堆疊深度，h 為樹高）

### 解題過程

#### 觀念學習：什麼是「高度」

一開始不確定「高度」的定義，釐清為「從這個節點往下走到最遠葉節點，經過幾條邊」，並確立慣例：葉節點高度為 0、空節點（`nullptr`）高度為 -1（這樣 `1 + max(左,右)` 的公式對葉節點也能自動算出正確的 0，不用另外特別處理）。

#### 虛擬碼階段

一開始想成「先算完整棵樹的高度，再另外做一次走訪去比對每個節點左右子樹高度差」，這是兩個分開的步驟，效率不好（每個節點的高度都要被重複計算，最壞情況退化成 O(n²)）。討論後改成「高度計算跟平衡檢查同時做，在同一次遞迴完成」，用一次遞迴達到 O(n)。

也修正了一個邊界疏漏：一開始只寫「差值大於 1 回傳 false，小於 1 繼續」，漏了「剛好等於 1」這個合法情況沒被涵蓋，補上「小於等於 1」才完整。

#### 程式碼階段的坑

1. **base case 條件用 `root->left == nullptr || root->right == nullptr` 判斷是否為葉節點，用錯運算子**：只要有一邊沒有子節點就觸發，導致「只有單邊子節點」的節點被誤判成葉節點，忽略掉還存在的另一邊子樹。用單邊鏈狀的樹（`1→2→3`）驗證抓出這個問題，修正成直接判斷 `root == nullptr`，讓真正的葉節點透過 `1+max(-1,-1)=0` 這個公式自動算出正確結果，不用額外特判
2. **同一個遞迴呼叫（`checkBalanced(root->left)`、`checkBalanced(root->right)`）在同一層被重複呼叫了 3 次以上**：每呼叫一次都要重新遞迴整個子樹，等於又把「重複計算」的問題用另一種方式帶回來。修正成左右子樹各自只呼叫一次、存進區域變數，之後全部從變數取值
3. **`max()` 直接用在兩個 `pair` 上，結果賦值給 `int` 型別的變數**：型別不符編不過，修正成先用 `.first` 取出各自的高度再比較
4. **完全沒檢查子樹自己是否已經不平衡（`.second`）**：只比對高度差，忽略了「子樹內部可能早就不平衡」的情況，導致某些深層不平衡的樹會被誤判成平衡。補上 `leftNode.second == false || rightNode.second == false` 的檢查
5. **`isBalanced` 變數沒有預設值**：如果高度差判斷都沒觸發 `= false`，這個變數會是未初始化的垃圾值。修正成宣告時就給預設值 `true`，只有真的發現不平衡才改成 `false`

### 1️⃣ 語法概念

- `pair<int, bool>`：`.first`、`.second` 分別取兩個值，適合「一個遞迴要同時回傳兩種不同型別資訊」的情境（這題是高度 + 是否平衡）
- base case 判斷「是不是葉節點」時，直接判斷 `root == nullptr` 比判斷 `root->left`/`root->right` 是否為 `nullptr` 更安全、更不容易漏掉單邊子節點的情況，讓公式本身自動處理葉節點，不用額外特判

### 2️⃣ 邏輯與複雜度

- 最終版本 O(n) 時間、O(h) 空間，把「算高度」跟「查平衡」合併成同一次遞迴，避免了分開兩次走訪導致的重複計算
- 同一個遞迴呼叫在同一層被重複呼叫多次，是這題最大的效率地雷：只要牽涉遞迴呼叫，任何要用到同一個子問題結果的地方，都該先存進變數，不要每次要用就重新呼叫一次

### 3️⃣ 演算法 / 資料結構盲點

- 遞迴函式如果需要同時回傳多種不同型別的資訊，`pair`（或自訂 struct）是常見做法；也可以用參考參數，或利用「合法值的範圍」設計哨兵值（sentinel）技巧，用單一回傳值同時傳遞兩種意義——四種做法這題都討論過，之後可以依情境挑選

### 可加強空間

- **提早結束**：左子樹算完馬上檢查是否已經不平衡，不平衡就直接 `return`，連右子樹都不用呼叫，可以省下不必要的遞迴：
  ```cpp
  pair<int, bool> checkBalanced(TreeNode* root) {
      if (root == nullptr) return {-1, true};

      pair<int, bool> leftNode = checkBalanced(root->left);
      if (!leftNode.second) return {-1, false};

      pair<int, bool> rightNode = checkBalanced(root->right);
      if (!rightNode.second) return {-1, false};

      int countHight = 1 + max(leftNode.first, rightNode.first);
      bool isBalanced = abs(leftNode.first - rightNode.first) <= 1;

      return {countHight, isBalanced};
  }
  ```
- **`abs()` 取代手動的「先比大小、再算差值」**：`<cmath>` 的 `abs(a - b)` 可以取代「先判斷誰比較大、分兩個分支各自算差值」這種寫法，兩個數字只在乎差距、不在乎正負號時可以直接用，比手寫 if-else 精簡

### 跟上次相比

（第一次複習，留空）
