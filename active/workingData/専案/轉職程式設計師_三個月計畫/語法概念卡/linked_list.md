# 鏈結串列（Linked List）

- 分類：資料結構（節點 + 指標）
- 對應 C#：沒有直接對應的內建型別（C# 用 `LinkedList<T>` 但內部細節被封裝，不需要自己管指標）

> 複習時先看 Q，自己講一遍答案，再點開 `<details>` 對答案。答錯或講不出來的，去下面「完整筆記」補。
> 跟 [`map.md`](map.md)（紅黑樹，「節點 + 指標」的樹狀版本）是同一種「節點 + 指標」家族的概念，之後遇到其他節點相關的資料結構都可以互相連結複習。
> 這是「保留順序」家族的代表，何時該用它、何時不該用，見 [`order_vs_value.md`](order_vs_value.md) 的判斷框架。判斷鏈結串列是否有循環，見 [`floyd_cycle.md`](floyd_cycle.md)（快慢指標）。

## 自我測驗

<details>
<summary>Q1. LeetCode 的 ListNode 長什麼樣子？核心概念是什麼？</summary>

A1.
```cpp
struct ListNode {
    int val;
    ListNode *next;
};
```
每個節點只有兩個東西：`val`（存的資料）、`next`（指向下一個節點的指標）。整條串列就是一串各自獨立配置在記憶體裡的節點，靠指標一個接一個串起來，不像陣列要求連續記憶體。

</details>

<details>
<summary>Q2. 怎麼存取節點、建立新節點、走訪整條串列？</summary>

A2.
```cpp
head->val;              // 取值（-> 是指標取成員，等於 (*head).val）
head->next;              // 取下一個節點的指標

ListNode* n = new ListNode(5);   // heap 上建立新節點

ListNode* cur = head;             // 走訪：用一個指標當「目前走到哪」的游標
while (cur != nullptr) {
    // 處理 cur->val
    cur = cur->next;
}
```

</details>

<details>
<summary>Q3. Dummy Head（虛擬頭節點）技巧是什麼？為什麼要用？</summary>

A3. 建一個沒有實際意義的起始節點，`tail` 指標從它開始往後接：
```cpp
ListNode dummy(0);
ListNode* tail = &dummy;
// ... 之後每接一個真正的節點，tail = tail->next; 往後移
return dummy.next;   // 真正的串列從 dummy 的下一個開始
```
用意：不用特別處理「第一個節點要接誰」這種邊界情況，所有節點都用同一套「接到 `tail->next`，再把 `tail` 往後移」的邏輯處理。

</details>

<details>
<summary>Q4. 常見的坑是什麼？</summary>

A4.
1. **`&` 用錯地方**：如果變數本身已經是指標（例如 `ListNode* p`），要複製它指向同一個節點只要直接賦值 `ListNode* q = p;`，不需要再 `&p`——那樣會變成 `ListNode**`（指標的指標），型別對不上。`&` 只用在「這個變數本身不是指標」的情況（例如 `&dummy`，因為 `dummy` 是物件不是指標）。
2. **`list1` 跟 `list1->next` 是不同的東西**：`list1`（變數本身）存的是「目前這個節點」的位址；`list1->next` 是進到節點內部，讀出「下一個節點」的位址。要操作/接上現在這個節點本身，用 `list1`；要往前移動、看下一個節點，用 `list1->next`。
3. **判斷「串列是否為空」，要檢查指標本身，不是它的欄位**：`if (list1 == nullptr)`，不是 `if (list1->val == ...)`——如果 `list1` 真的是 `nullptr`，後者會先對空指標取值而崩潰。
4. **對 `nullptr` 呼叫 `->` 是未定義行為**，走訪或比較節點前一定要先確認不是 `nullptr`。
5. **`cur = cur->next;` 忘記寫，或用來追蹤狀態的指標（例如 `tail`）做完動作後忘記同步移動**，會造成無窮迴圈，或是新接的節點被下一輪覆蓋、資料遺失。
6. **`new ListNode(x)` 不是 C++ 唯一的建立方式**：也可以在 stack 上直接宣告 `ListNode n(x);` 再用 `&n` 取位址，函式結束會自動釋放，不用手動 `delete`——dummy head 常用這招。

</details>

<details>
<summary>Q5. 時間/空間複雜度？</summary>

A5. 走訪整條串列是 O(n)。跟陣列比，插入/刪除（已經拿到節點位置的情況下）是 O(1)（只要改指標），不像陣列插入要搬移後面所有元素；但鏈結串列沒有 O(1) 隨機存取，要找第 k 個節點得从頭走 O(n)。

</details>

<details>
<summary>Q6. 原地反轉鏈結串列（迭代法）怎麼寫？順序為什麼是這樣？</summary>

A6.
```cpp
ListNode* prev = nullptr;
ListNode* curr = head;

while (curr != nullptr) {
    ListNode* reg = curr->next;   // 1. 先存住舊的 next，不然改完就找不到了
    curr->next = prev;             // 2. 反轉指標，一定要用「還沒被覆蓋的舊 prev」
    prev = curr;                   // 3. prev 往前移一格
    curr = reg;                    // 4. curr 往前移一格（用剛剛存的 reg）
}

return prev;   // 迴圈結束時 curr 為 nullptr，prev 就是新的頭節點
```
關鍵不是死背這四行，而是順序背後的原因：**多個狀態變數要在同一輪更新時，任何一步都不能用「本輪已經被自己覆蓋過的新值」**。這裡是先讀出 `curr->next` 存進 `reg`，再拿舊的 `prev` 去覆蓋 `curr->next`，最後才依序把 `prev`、`curr` 往前移。順序對調（例如先 `prev = curr` 再 `curr->next = prev`）會讓節點的 `next` 指向自己，形成自環。
不需要額外開一個新的鏈結串列來承接結果——原地反轉是直接改動既有節點的 `next`，比另外建新串列更省，遇到反轉/重排類題目可以先想「能不能直接動原本的指標」。

</details>

## 完整筆記

鏈結串列跟陣列的取捨，本質上跟 [`map`（紅黑樹）vs 排序陣列 + 二分法查詢](map.md) 是同一種「連續記憶體換隨機存取」vs「指標連結換插入彈性」的取捨，可以對照著理解。

## 出現過的題目

| 題號 | 用法情境 |
|------|---------|
| 21 | Merge Two Sorted Lists：用 dummy head + tail 指標，兩個指標各自走訪 L1、L2，較小的節點接到 tail 尾端，merge 完成後回傳 `dummy->next` |
| 206 | Reverse Linked List：三指標（`prev`/`curr`/`reg`）迭代原地反轉，見 Q6 |
