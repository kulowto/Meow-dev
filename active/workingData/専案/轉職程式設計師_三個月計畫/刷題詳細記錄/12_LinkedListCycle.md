# 141 Linked List Cycle

- Key Cogitation：Linked List、Two Pointers（Floyd's Cycle Detection）、Hash Set
- Level：Easy
- 相關概念卡：[`語法概念卡/linked_list.md`](../語法概念卡/linked_list.md)、[`語法概念卡/floyd_cycle.md`](../語法概念卡/floyd_cycle.md)、[`語法概念卡/order_vs_value.md`](../語法概念卡/order_vs_value.md)

> 同一題每次複習都在本檔案下方累加一段，不開新檔。用「跟上次相比」欄位追蹤盲點是否解決。

---

## 複習 #1 — 2026-08-19

- 狀態：有Bug
- 花費時間：1 小時

### 我的解法

主動練習了兩種做法：

**版本一：`unordered_set` 記錄走過的位址**

```cpp
unordered_set<ListNode*> visited;

bool hasCycle(ListNode *head) {

    if(head == nullptr){
        return false;
    }

    if(head->next == nullptr){
        return false;
    }

    if(visited.count(head)){
        return true;
    }else{
        visited.insert(head);
    }

    return hasCycle(head->next);

}
```

- 時間複雜度：O(n)　空間複雜度：O(n)

**版本二：快慢指標（Floyd's Cycle Detection），這題的最優解**

```cpp
bool hasCycle(ListNode *head) {

    if(head == nullptr){
        return false;
    }

    if(head->next == nullptr){
        return false;
    }

    ListNode *fast = head;
    ListNode *slow = head;

    while(fast != nullptr && fast->next != nullptr){
        fast = fast->next->next;
        slow = slow->next;

        if(fast == slow){
            return true;
        }

    }
    return false;
}
```

- 時間複雜度：O(n)　空間複雜度：**O(1)**

### 解題過程

#### 版本一：`unordered_set` 練習

1. 一開始把 `unordered_set` 宣告成函式**內部**的區域變數，配合遞迴使用——但每次遞迴呼叫都會重新宣告一個全新的空 `set`，上一層存進去的位址完全不會被下一層繼承，導致永遠偵測不到重複。用 `A→B→C→A` 的循環例子驗證，發現每一層的 `visited` 都是獨立、互不相通的，改成把 `visited` 搬到函式外面（跨呼叫共用同一份）才解決
2. 順便確認了這個設計的隱憂：`visited` 變成跨呼叫持續存在的狀態，如果同一個物件被拿去重複判斷不同的鏈結串列，會殘留上一輪的舊資料造成誤判——這題在 LeetCode 判題環境下不會踩到（每個測資都是全新物件），但記下來當作寫法上的提醒
3. `unordered_set`（少了 `ed`）打字錯誤
4. `head` 本身可能是 `nullptr`（空串列），要先檢查才能存取 `head->next`

#### 版本二：快慢指標

1. 一開始用 `if` 而不是 `while`，快慢指標只移動了一步就結束，沒有持續往前走到真的相遇或走到底為止。用 `A→B→C→D→B`（循環入口不是頭節點本身）驗證，這個例子要走 3 輪才會相遇，用 `if` 只做一次完全抓不到，改成 `while` 才對
2. 迴圈自然結束（沒有中途相遇）代表沒有循環，一開始忘記在迴圈後面補 `return false;`

### 1️⃣ 語法概念

- 只需要「判斷存不存在」、不需要額外存值時，用 `unordered_set`，不是 `unordered_map`——`map` 是 key-value 配對，這題用不到 value
- 指標本身「就是」位址，`unordered_set<ListNode*>` 直接把指標塞進去存，不需要額外轉換

### 2️⃣ 邏輯與複雜度

- 遞迴搭配「需要跨層共用的狀態」時，區域變數宣告在函式裡面會導致每層各自獨立、無法共用——這跟 Balanced Binary Tree、Flood Fill 遇到的「該固定/該共用的值處理方式錯誤」是同一個大類的坑，這次的變形是「共用狀態被錯誤地放進了會被重新初始化的區域變數裡」
- 快慢指標一定要用 `while` 迴圈持續移動，只做一步是最常見的實作疏漏，尤其是循環入口不在頭節點本身時，需要好幾輪才會相遇，不能只測「入口就是頭節點」這種最簡單的情況就以為對了

### 3️⃣ 演算法 / 資料結構盲點

- **Floyd's Cycle Detection（龜兔賽跑）**：快慢指標分別走 2 步、1 步，若存在循環兩者必定相遇，是偵測鏈結串列循環的標準做法，O(1) 空間勝過 Hash Set 的 O(n)，獨立做成 `floyd_cycle.md` 概念卡
- 這題也呼應 `order_vs_value.md` 框架的延伸：不需要額外容器記錄任何東西，直接利用「兩個不同速度的指標在同一條路徑上移動」這個性質本身就能判斷答案，跟 Binary Search 那題「善用輸入已有的性質、不額外建結構」是同一種思考方向

### 跟上次相比

（第一次複習，留空）
