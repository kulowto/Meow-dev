# 206 Reverse Linked List

- Key Cogitation：Linked List（三指標迭代反轉）
- Level：Easy
- 相關概念卡：[`語法概念卡/linked_list.md`](../語法概念卡/linked_list.md)

> 同一題每次複習都在本檔案下方累加一段，不開新檔。用「跟上次相比」欄位追蹤盲點是否解決。

---

## 複習 #1 — 2026-08-27

- 狀態：有Bug
- 花費時間：60 分鐘

### 我的解法

```cpp
/**
 * Definition for singly-linked list.
 * struct ListNode {
 *     int val;
 *     ListNode *next;
 *     ListNode() : val(0), next(nullptr) {}
 *     ListNode(int x) : val(x), next(nullptr) {}
 *     ListNode(int x, ListNode *next) : val(x), next(next) {}
 * };
 */
class Solution {
public:
    ListNode* reverseList(ListNode* head) {
        ListNode* prev = nullptr;
        ListNode* curr = head;

        while (curr != nullptr){
            ListNode* reg = curr->next;
            curr->next = prev;
            prev = curr;
            curr = reg;
        }

        return prev;
    }
};
```

- 時間複雜度：O(n)
- 空間複雜度：O(1)

### 解題過程

#### 虛擬碼階段

一開始提出遞迴解，但設計成「另外開一個新的鏈結串列，把後序回傳的節點位址一一接上」——邏輯可行但多繞一圈，其實不需要額外開新串列，直接改動原節點的 `next` 就能就地反轉。轉向迭代法後，四個動作（存下一個節點、反轉指標、移動 prev、移動 curr）反覆試了 4 次順序才排對：

1. 第一次漏了移動 `curr`，且把 `prev` 設成還沒處理過的下一個節點
2. 第二次順序對調，讓 `prev = curr` 執行完才做 `curr->next = prev`，等於指標反轉時用了已經被更新過的 `prev`，造成 `node1->next` 指向自己形成自環
3. 第三次完全沒做反轉動作（`curr->next = reg` 等於沒變），且 `curr` 忘記更新
4. 第四次才排對：`reg = curr->next` → `curr->next = prev` → `prev = curr` → `curr = reg`

核心教訓：多個狀態變數要在同一輪更新時，**反轉指標一定要用「還沒被覆蓋過的舊 `prev`」**，順序上「讀取舊值 → 寫入新指標 → 才能覆蓋變數」缺一不可對調。

#### 程式碼階段

邏輯確認後直接轉譯，只漏了 `ListNode* reg` 的型別宣告（C++ 不能像 C# 一樣省略宣告直接賦值），補上即可跑對。

#### 額外釐清：`curr` 與 `curr->next` 的區別

圖解過程中發現使用者對「變數本身存的位址」跟「該位址指向節點裡的 `next` 欄位」這兩層概念混淆，已用位址圖解（`curr = 0x100` vs 進到 `0x100` 盒子裡讀/寫 `next` 欄位）釐清。

### 1️⃣ 語法概念

- `curr`（指標變數本身，存的是位址）跟 `curr->next`（進到該位址節點內部，讀寫 `next` 欄位）是不同層級的東西，混在一起想是這次卡住的根本原因
- `ListNode* reg` 忘記宣告型別直接賦值，C++ 不像 C#/JS 允許隱式宣告

### 2️⃣ 邏輯與複雜度

- O(n) 時間、O(1) 空間，是這題最優解（遞迴版本則是 O(n) 空間，因為 call stack）
- 迭代反轉的四步順序本質：**先讀出待覆蓋的舊值，才能安心覆蓋** —— 只要有任何一步把「等一下還要用到的舊值」提前覆蓋掉，就會產生自環或跳步的錯誤，這題把「迴圈裡狀態變數管理」的坑用最小的例子暴露出來

### 3️⃣ 演算法 / 資料結構盲點

- 遞迴設計時直覺想「額外開一個新串列承接結果」，而不是「直接動原節點的指標」，是對「原地反轉可以重用既有節點、不需要新結構」這件事不夠敏感，之後遇到反轉/重排類題目可以先問自己「有沒有辦法不開新容器，直接動原本的指標」

### 跟上次相比

（第一次複習，留空）
