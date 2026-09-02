# 876 Middle of the Linked List

- Key Cogitation：Linked List（兩次走訪：計數＋定位）
- Level：Easy
- 相關概念卡：[`語法概念卡/linked_list.md`](../語法概念卡/linked_list.md)

> 同一題每次複習都在本檔案下方累加一段，不開新檔。用「跟上次相比」欄位追蹤盲點是否解決。

---

## 複習 #1 — 2026-09-01

- 狀態：有Bug
- 花費時間：20 分鐘

### 我的解法

```cpp
class Solution {
private:

    int count = 1;

    int calculateMiddle (ListNode* head){
        while(head->next != nullptr){
            count++;
            head = head->next;
        }
        return count/2 +1 ;
    }

public:
    ListNode* middleNode(ListNode* head) {

        int midCount = calculateMiddle(head);

        count = 1;

        while(count < midCount){
            count++;
            head = head->next;
        }

        return head;

    }
};
```

- 時間複雜度：O(n)
- 空間複雜度：O(1)

### 解題過程

#### 虛擬碼階段：奇偶分開的公式合併成一條

一開始把目標位置的公式分奇偶討論（奇數 `count/2`、偶數 `count/2+1`），用 `1->2->3->4->5` 驗證奇數公式：算出 `I=2`，但正確答案是第 3 個節點，抓出奇數公式少加 1。統一成 `count/2+1`，奇偶都驗證正確，不用分開討論。

#### 程式碼階段：兩個小問題

1. 呼叫函式時多打了型別宣告：`calculateMiddle (ListNode* head)` 改成 `calculateMiddle(head)`
2. 第二次走訪迴圈用 `count <= midCount` 會多移動一次，用 `1->2->3->4->5`（`midCount=3`）trace 出最後停在第 4 個節點而不是第 3 個，改成 `count < midCount` 才對

### 1️⃣ 語法概念

- 呼叫已經定義好的函式時，直接傳變數，不用重複寫型別宣告

### 2️⃣ 邏輯與複雜度

- O(n) 時間（兩次走訪，仍是線性）、O(1) 空間
- 目標位置公式 `count/2+1`（整數除法）可以同時涵蓋奇偶兩種情況，不用分開討論
- 兩次走訪版本雖然正確，但走訪了兩次；更省的做法是用快慢指標（fast/slow pointer）一次走訪就能定位到中點，之後遇到類似題目可以想一下要不要優先考慮

### 3️⃣ 演算法 / 資料結構盲點

- 迴圈邊界值（`<` 還是 `<=`）搭配「從哪個位置開始數、要移動幾次」又出現 off-by-one，是「迴圈裡的狀態管理」這個主要弱點的延伸樣態（這次是移動次數比目標位置多算一次），第 8 次同類問題出現

### 跟上次相比

（第一次複習，留空）
