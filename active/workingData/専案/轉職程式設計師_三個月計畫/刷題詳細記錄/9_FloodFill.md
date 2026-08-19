# 733 Flood Fill

- Key Cogitation：DFS、Grid Traversal
- Level：Easy
- 相關概念卡：[`語法概念卡/grid_traversal.md`](../語法概念卡/grid_traversal.md)

> 同一題每次複習都在本檔案下方累加一段，不開新檔。用「跟上次相比」欄位追蹤盲點是否解決。

---

## 複習 #1 — 2026-08-17

- 狀態：寫不出來（最後關鍵的結構性修正是直接被提供，非自己想通）
- 花費時間：1 小時

### 我的解法

```cpp
class Solution {
public:
    vector<vector<int>> floodFill(vector<vector<int>>& image, int sr, int sc, int color) {

        int curColor = image[sr][sc];

        if( curColor == color ){
            return image;
        }

        dfs(image, sr, sc, curColor, color);
        return image;

    }

private:
    void dfs(vector<vector<int>>& image, int r, int c, int curColor, int newColor){

        int dx[] = {-1,1,0,0}; // Up,down,left,right (x-Axis)
        int dy[] = {0,0,-1,1}; // Up,down,left,right (y-Axis)

        if( r < 0 || r >= image.size() ||
            c < 0 || c >= image[0].size()){
                return;
            }

        if( image[r][c] != curColor){
            return;
        }

        image[r][c] = newColor;

        for (int i = 0 ; i < 4; i++ ){
            dfs(image, r+dx[i], c+dy[i], curColor, newColor );
        }

    }

};
```

- 時間複雜度：O(m×n)（每格最多被走訪一次，染色後顏色跟 `curColor` 不符會直接擋掉重複走訪）
- 空間複雜度：O(m×n)（最壞情況遞迴呼叫堆疊深度，例如整張圖都同色）

### 解題過程

這題選擇跳過虛擬碼、直接寫程式碼（依規則允許嘗試），結果卡了將近一小時，過程分幾個階段：

#### 前置概念：BFS/DFS 複習、方向增量陣列

先複習了 BFS/DFS 的底層運作原理（DFS 用 stack/遞迴、先衝到底再回頭；BFS 用 queue、一層一層擴散），確定這題順序不重要，DFS（遞迴）跟 Invert Binary Tree 的遞迴模式接近，選定方向。另外學了「方向增量陣列」（`dx`/`dy` + 迴圈跑 4 次）取代四個方向各寫一次的寫法，並確立「網格沒有像樹一樣的 `nullptr` 天然邊界，要自己明確檢查範圍」——這兩點都獨立做成 `grid_traversal.md` 概念卡。

#### 型別觀念混淆：把 `vector<vector<int>>&` 誤解成 pair、把參考當指標

一開始想用 `(image->first)->first`、`*image[0][0]` 這類寫法取得維度跟值，混淆了三件事：
1. `image` 是 `vector<vector<int>>`，不是 `pair`，沒有 `.first`/`.second`
2. `image` 是**參考**（reference），不是指標，永遠不用 `*` 解參考，用法跟直接用物件本身一樣
3. `image[0][0]` 已經是實際的 `int` 值，不是位址，不能再對它 `*`

修正成 `image.size()`（行數）、`image[0].size()`（列數，用 `.size()` 不是 `.length()`——這是 `vector` 沒有的 `string` 專屬方法）。

#### 程式碼撰寫階段，連續好幾輪的問題

1. `int dx = {...}` 少了陣列括號、迴圈變數用 `i` 卻索引成 `dx[i]`（打錯成 `d`/`i` 不一致）、`if(...)；{` 條件式裡多一個分號、呼叫函式時重複寫參數型別（`floodFill(vector<vector<int>>& image, ...)`）——這些都是編譯期就能抓到的語法錯誤
2. 邊界檢查 `>` 應該是 `>=`（跟 Binary Search 那題同一種 off-by-one）
3. 超出邊界時原本用 `return`（整個函式結束）、後來改用 `break`（跳出整個迴圈）、都不是正確答案，正確要用 `continue`（只跳過這一個方向，繼續檢查下一個方向）
4. 顏色檢查放在遞迴呼叫**之後**，順序反了，且起點 `(sr,sc)` 自己從頭到尾沒有被染色
5. **`color == curColor`（新舊顏色剛好一樣）的邊界情況**：一開始完全沒考慮，加入判斷後又寫錯位置（`image[sr][sc] == color`，比較的是「剛染色完的值」跟「新顏色」，這兩者永遠相等，導致函式在檢查完第一個方向前就提早結束，連基本情況都被弄壞）
6. **核心結構性問題（最後靠直接給答案才解決）**：每次遞迴呼叫都重新用 `image[r][c]` 計算 `curColor`，但遞迴進去之前這格早就被染成新顏色了，導致 `curColor` 永遠等於新顏色，遞迴進去馬上又被判定「顏色已經一樣」而提早結束，整個 flood fill 完全無法擴散超過一步。改寫成「拆成 public/private 兩個函式，`curColor` 在最頂層算一次，之後全程當**參數**往下傳，不再重新計算」才解決
7. 過程中重寫時，一度把「染色」這個動作整個漏寫，導致邏輯上會造成無窮遞迴（顏色永遠不變，鄰居會不斷互相遞迴檢查彼此）

### 1️⃣ 語法概念

- `vector` 用 `.size()`，不是 `.length()`（`.length()` 是 `string` 專屬）
- **參考（reference）不需要、也不能用 `*` 解參考**，用法跟直接使用物件本身一樣；`*` 只用在**指標**上。這題又踩到一次「把參考當指標」的坑，跟 Merge Two Sorted Lists 那題是同一種混淆
- `dx[]`／`dy[]` 方向增量陣列的宣告要記得中括號，索引變數要跟迴圈變數一致

### 2️⃣ 邏輯與複雜度

- 最終版本 O(m×n) 時間，是這題的標準解法
- `continue`／`break`／`return` 三者在迴圈裡的行為差異，這題完整踩過一輪（`return` 結束整個函式、`break` 跳出整個迴圈、`continue` 只跳過這一輪）——想清楚「我要跳過的範圍是什麼」再選對的關鍵字
- **核心教訓**：遞迴時，如果某個值（例如 `curColor`）在整個遞迴過程中應該保持不變，就該用**參數**往下傳，不要在每一層重新從可能已經被修改過的資料裡去算。這題跟 Binary Search 的 `index_count`、Merge Two Sorted Lists 的 `tail` 指標，都是「追蹤用的變數該更新卻沒更新／該固定卻被重新計算」同一大類的狀態管理問題

### 3️⃣ 演算法 / 資料結構盲點

- DFS（遞迴）處理「網格連通區域擴散」問題的標準套路：邊界檢查 + 條件檢查（含用顏色比對取代額外的「已走訪」標記）+ 動作（染色）+ 對四個方向遞迴，這個順序本身要記熟，之後遇到類似題目（例如「島嶼數量」這類連通區域問題）可以直接套用

### 跟上次相比

（第一次複習，留空）
