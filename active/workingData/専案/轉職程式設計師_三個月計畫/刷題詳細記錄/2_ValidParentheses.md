# 20 Valid Parentheses

- Key Cogitation：Stack
- Level：Easy

> 同一題每次複習都在本檔案下方累加一段，不開新檔。用「跟上次相比」欄位追蹤盲點是否解決。

---

## 複習 #1 — 2026-08-07

- 狀態：寫不出來（靠提問釐清思路才寫出來，非獨立完成，不計入「過」）
- 花費時間：未計時（非限時單次作答，透過多輪討論完成）

### 我的解法

```cpp
#include <stack>
class Solution {
public:
    bool isValid(string s) {

    bool ans = true;
    char ls[] = {'(','{','['};
    char rs[] = {')','}',']'};
    stack<char> st;

    for(int i =0; i<s.length() ; i++){
        for(int j = 0; j < std::size(ls) ; j++){
            if( s[i] == ls[j]){
                st.push(s[i]);
            }else if ( s[i] == rs[j]){
                if(st.empty()){
                    ans = false;
                } else if(st.top() != ls[j]){
                    ans = false;
                }else{
                    st.pop();
                }
            }
        }
    }

    return ans;

    }
};
```

- 時間複雜度：O(n)（內層固定跑 3 次，常數倍，整體仍是 O(n)）
- 空間複雜度：O(n)（stack 最壞情況存到 n/2 個左括號）

### 解題過程（除錯軌跡）

這題卡了三輪才過，過程本身比最終程式碼更值得記：

1. **第一版**：用「數左右括號各出現次數，數量相等就 valid」的統計法。核心盲點——完全沒考慮**順序**跟**巢狀配對**，`"(]"`、`")("` 這種數量對但順序錯的字串會被誤判為 valid。同時內層 `while` 忘記寫成 `if`，條件沒有隨迴圈改變，無窮迴圈把 `count[j]` 一路加到 `int` 溢位（signed integer overflow）。
2. **想清楚 Stack 方向**：一開始虛擬碼把「該被存起來」跟「該被拿來比對」的觸發符號寫反了（誤以為右括號先存、左括號才觸發比對），也誤寫了「左括號後面接右括號＝false」這條規則——這條規則本身跟 `"()"` 這種最基本的合法情況直接矛盾。修正後才確立正確方向：**左括號進 stack，右括號立刻跟 stack 頂端比對**。
3. **實作階段的坑**：
   - `char ls[] = {...}` 陣列是 C 原生陣列，**沒有 `.size()`**（跟 `vector`/`string` 不同，這點容易因為平常用慣 STL 容器而忘記），要用 `std::size(ls)` 或 `sizeof(ls)/sizeof(ls[0])`
   - `if(st.empty()){ ans=false; }` 後面沒接 `else`，導致空 stack 時還是會往下執行 `st.top()` —— 對空 stack 呼叫 `top()` 是未定義行為，是這題除了溢位以外的第二個「沒有檔住就會出事」的坑

### 1️⃣ 語法概念

- `stack<char>` 核心操作：`push`（存）、`pop`（丟棄最上面，**沒有回傳值**）、`top`（讀最上面，不移除）、`empty`（判斷是否為空，`top`/`pop` 前必查）
- C 原生陣列（`char arr[]`）跟 STL 容器不同，沒有 `.size()` 成員函式，要用 `std::size()`（C++17）或 `sizeof` 算
- `while` 迴圈條件沒有隨內容改變會造成無窮迴圈，這次直接撞出整數溢位——寫 `while` 前要先確認迴圈內有沒有東西會讓條件變成 false

### 2️⃣ 邏輯與複雜度

- 目前雙層迴圈（外層掃字元、內層掃 3 種括號類型）時間複雜度是 O(n)，因為內層固定只跑 3 次，是常數，不影響整體級數，但寫法上還有兩個可以優化的地方（見下方「可加強空間」）
- 已修正的邏輯坑：`st.empty()` 判斷跟 `st.top()` 判斷原本是兩個獨立 `if`（沒有互斥），改成 `if / else if / else` 三分支互斥後，空 stack 時不會再誤觸 `top()`

### 3️⃣ 演算法 / 資料結構盲點

- 這題的核心洞察：只要問題牽涉「**最近發生的事要最先被處理/關閉**」（巢狀、配對、順序相關），第一直覺要想到 **Stack（LIFO）**，不是統計數量
- 跟第一題 Two Sum 的盲點是同一種類型的延伸：那題是「看到互補關係要想 Hash Map」，這題是「看到巢狀配對要想 Stack」——都是「先辨識題型對應的標準資料結構，而不是先用暴力法硬寫」，這點已經記進 `跨題目盲點彙總.md`

### 可加強空間

- **提早結束**：`ans` 一旦變成 `false` 可以直接 `return false;`，不用把剩下的字元全部掃完
- **內層迴圈提早跳出**：找到符合的 `ls[j]`/`rs[j]` 之後可以 `break`，不用把 3 個都比完
- **拿掉內層迴圈**（~~原本建議用 `unordered_map<char,char>`~~，已修正）：這題括號種類固定只有 3 組，用 `switch` 取代內層迴圈比 `unordered_map` 更合適——hash map 查值要算 hash、可能有記憶體間接跳轉，這個開銷對只有 3 組固定配對的場景反而比 `switch`/`if-else` 直接比較更大。`unordered_map` 的優勢要在資料量大、key 動態不固定時才明顯（例如 Two Sum 那種數值範圍大的情境），不適合套用在這種小型固定集合上
- **邏輯結尾漏掉的邊界**：原本 `return ans;` 沒有檢查跑完後 stack 是否為空，導致 `"["` 這種只有左括號、沒有對應右括號的輸入會誤判成 true。修正為 `return ans && st.empty();`——這其實是自己虛擬碼裡本來就寫了的最後一步（「所有值跑完且 ST 為空值才是 TRUE」），只是沒有真的轉成程式碼，值得記住：**虛擬碼的每一步都要對照程式碼逐條檢查有沒有漏掉，不能只憑印象覺得「應該有寫」**

### switch 版本參考

把「可加強空間」提到的幾點（提早結束、拿掉內層迴圈改用 switch、修正後的 stack 是否為空判斷）一起套用：

```cpp
class Solution {
public:
    bool isValid(string s) {
        stack<char> st;

        for (char c : s) {
            switch (c) {
                case '(':
                case '{':
                case '[':
                    st.push(c);
                    break;
                case ')':
                    if (st.empty() || st.top() != '(') return false;
                    st.pop();
                    break;
                case '}':
                    if (st.empty() || st.top() != '{') return false;
                    st.pop();
                    break;
                case ']':
                    if (st.empty() || st.top() != '[') return false;
                    st.pop();
                    break;
            }
        }

        return st.empty();
    }
};
```

跟原本版本的差異：
- 內層 3 次比較的 for 迴圈拿掉，改用 `switch` 一次判斷字元類型，交給編譯器優化成 jump table
- 一遇到不合法組合立刻 `return false;`，不用等迴圈跑完
- `for (char c : s)` 是 range-based for（C++11），直接拿到每個字元本身，不用透過 index 存取 `s[i]`，省了一次索引運算，可讀性也更好
- 最後 `return st.empty();` 就是「跑完且 stack 為空才 true」，不用額外的 `ans` 變數

### 跟上次相比

（第一次複習，留空）
