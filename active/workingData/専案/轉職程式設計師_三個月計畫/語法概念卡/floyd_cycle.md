# Floyd's Cycle Detection（快慢指標 / 龜兔賽跑）

- 分類：演算法技巧（雙指標的延伸應用）
- 對應 C#：無直接語法對應，概念可直接套用

> 複習時先看 Q，自己講一遍答案，再點開 `<details>` 對答案。
> 跟 [`linked_list.md`](linked_list.md) 是同一個情境下的搭配技巧，跟 [`order_vs_value.md`](order_vs_value.md) 也有關聯：不額外建容器，直接利用資料本身的性質。

## 自我測驗

<details>
<summary>Q1. 這是什麼？什麼情境下會想到用它？</summary>

A1. 兩個指標從同一個起點出發，一個一次走 1 步（慢指標），一個一次走 2 步（快指標）。看到「判斷鏈結串列/序列裡有沒有循環」這類題目，直接想到這個技巧，不需要額外的容器記錄走過的節點。

</details>

<details>
<summary>Q2. 核心邏輯怎麼寫？</summary>

A2.
```cpp
ListNode *fast = head;
ListNode *slow = head;

while (fast != nullptr && fast->next != nullptr) {
    fast = fast->next->next;
    slow = slow->next;

    if (fast == slow) {
        return true;   // 相遇，代表有循環
    }
}
return false;   // fast 走到底了，沒有循環
```

</details>

<details>
<summary>Q3. 為什麼「一定會相遇」？常見的坑是什麼？</summary>

A3.
- **為什麼會相遇**：如果存在循環，快指標每一輪比慢指標多走 1 步，等於在循環內持續「縮短」跟慢指標的距離，遲早會追上——只要有循環，兩者必定在有限步數內相遇，不可能永遠錯開
- **一定要用 `while` 持續移動，不能只做一步**：循環入口不一定是頭節點本身，可能要走好幾輪才會真的相遇，只測「入口就是頭」這種最簡單情況容易誤以為做一次就夠
- **迴圈條件要同時檢查 `fast` 跟 `fast->next`**：因為快指標一次要往前存取兩步（`fast->next->next`），如果只檢查 `fast != nullptr`，`fast->next` 可能已經是 `nullptr`，對它再取 `->next` 會崩潰
- **迴圈正常結束（沒有中途相遇）要記得 `return false`**：容易漏寫，是這題常見的收尾疏漏

</details>

<details>
<summary>Q4. 時間/空間複雜度？跟用 Hash Set 記錄走過節點的做法比較？</summary>

A4. 時間 O(n)，空間 **O(1)**——不需要任何額外容器，只用兩個指標變數。跟「用 `unordered_set<ListNode*>` 記錄走過的位址」的做法比，時間複雜度一樣是 O(n)，但快慢指標把空間複雜度從 O(n) 降到 O(1)，是這題的最優解。

</details>

## 完整筆記

這個技巧可以延伸到其他「找中點」「找循環起點」類的題目（例如找鏈結串列中點：快指標走到底時，慢指標剛好在中間），核心都是利用「兩個速度不同的指標在同一條路徑上移動」這個性質，不需要額外資料結構。

## 出現過的題目

| 題號 | 用法情境 |
|------|---------|
| 141 | Linked List Cycle：快慢指標判斷鏈結串列是否有循環，O(1) 空間勝過 `unordered_set` 版本的 O(n) |
