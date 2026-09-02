# Class 基礎語法：private / public、成員函式、成員變數

- 分類：C++ 基礎語法（物件導向）
- 對應 C#：概念幾乎一樣（`private`/`public`、成員方法、欄位），語法也很接近，差異主要在 LeetCode 的 class 題目常常要自己設計內部輔助結構

> 複習時先看 Q，自己講一遍答案，再點開 `<details>` 對答案。
> LeetCode 的「設計類」題目（例如用 Stack 實作 Queue）常會用到這裡的語法，是 `stack.md`／`recursion.md` 之外，另一塊常被忽略但很基礎的東西。

## 自我測驗

<details>
<summary>Q1. `private` 跟 `public` 差在哪？</summary>

A1. `public:` 底下宣告的成員（函式/變數），類別外部可以直接透過物件呼叫/存取。`private:` 底下的只能在**類別內部**（同一個類別自己的成員函式裡）被使用，外部程式碼呼叫不到。設計輔助函式（不想讓外部看到、只是內部拿來重複使用的邏輯）時放在 `private:`。

</details>

<details>
<summary>Q2. 類別內部，一個成員函式要呼叫「另一個成員函式」，語法怎麼寫？</summary>

A2. **直接寫函式名稱呼叫就好，不需要任何物件前綴**：
```cpp
class MyQueue {
private:
    void shiftStack() { ... }   // 私有輔助函式

public:
    int pop() {
        shiftStack();   // 直接呼叫，不用寫 this->shiftStack() 或其他前綴
        ...
    }
};
```
因為呼叫發生在**同一個類別內部**，編譯器知道你指的就是自己這個物件的成員函式，不像外部呼叫需要先有一個物件（例如 `myQueue.pop()`）才能呼叫。

</details>

<details>
<summary>Q3. 成員變數（member variable）跟區域變數，差在哪？為什麼這題要用成員變數？</summary>

A3. **成員變數**宣告在類別裡（不在任何函式內部），會**跟著整個物件的生命週期存在**，物件沒被銷毀之前，值會一直保留，可以被同一個物件的所有成員函式共用、跨多次呼叫延續狀態。**區域變數**宣告在函式內部，每次呼叫函式都會重新建立、函式執行完就消失。

Implement Queue using Stacks 這題需要 `sIn`、`sOut` 這兩個 Stack 在 `push`、`pop`、`peek` 之間**持續累積內容**，如果宣告成某個函式裡的區域變數，每次呼叫都會被重置成空的——這正是 Linked List Cycle 那題「共用狀態不能宣告成會被重置的區域變數」踩過的坑，這裡用「宣告成類別的成員變數」正確解決了同樣的問題。

</details>

<details>
<summary>Q4. 可以在一個成員函式裡面，直接定義另一個函式嗎？</summary>

A4. 不行，**C++ 不支援巢狀函式定義**（不像某些語言可以在函式內部直接宣告另一個函式）。需要一個輔助函式（例如遞迴用的 DFS/helper）時，要把它獨立寫成 class 的另一個成員函式（通常放 `private:`），跟原本的函式平行並列，不能寫在裡面。如果這個輔助函式需要跟呼叫它的函式共用某個值（例如遞迴過程中要持續更新的全域最大值），那個值也要跟著變成成員變數，不能留在原本函式的區域變數。

</details>

## 完整筆記

LeetCode 的「設計資料結構」類題目（`class MyXxx { ... }` 這種格式，例如這題、LRU Cache 之類的），核心都是同一套模式：需要跨函式呼叫持續存在的資料放成員變數，內部邏輯需要拆分重複使用的部分放私有輔助函式。跟一般單一函式的題目（`class Solution { bool xxx(...) { ... } }`）比，多了「怎麼設計這個類別本身的內部結構」這一層。

## 出現過的題目

| 題號 | 用法情境 |
|------|---------|
| 232 | Implement Queue using Stacks：`sIn`、`sOut` 兩個 `stack<int>` 當成員變數持續累積狀態，`shiftStack()` 私有函式封裝搬移邏輯，被 `pop()`/`peek()` 直接呼叫 |
| 543 | Diameter of Binary Tree：一開始把 `DFS` 寫成巢狀函式編不過，改成獨立的 `private` 成員函式，全域最大直徑 `res` 也改成成員變數，讓 `DFS` 遞迴過程能持續更新它 |
