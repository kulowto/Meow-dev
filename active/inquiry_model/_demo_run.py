"""示範跑法 - 用預設回答模擬互動，展示完整 UI 流程"""
import sys, time
sys.path.insert(0, ".")
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

_answers = iter([
    "如何提升學習效率",
    "",                                                      # 模式（Enter = explore）
    "",                                                      # Reality Check（Enter = 跳過）
    "每天讀書 2 小時，但容易分心，讀完大部分都忘了",
    "希望讀完一本書後能記住 80% 的核心概念",
    "試過番茄鐘一個月，分心問題還是沒解決",
    "用劃重點和抄筆記，但翻回去看還是覺得陌生",
    "嘗試過心智圖，整理後感覺有幫助，但很花時間",
    "沒有固定複習週期，通常只讀一遍",
    "用 Notion 記錄，但幾乎不回頭看",
    "主要用手機 APP 看書，偶爾用 highlight 功能",
    "沒有系統化的方式衡量自己學了多少",
    "",                                                      # 繼續待續問題？（Enter = 跳過）
    "目前沒有特別的評估方式",
    "嘗試過但很快就放棄了",
    "主要問題是缺乏動力持續執行",
])


def _mock_input(prompt=""):
    val = next(_answers, "")
    sys.stdout.write(prompt + val + "\n")
    sys.stdout.flush()
    time.sleep(0.3)
    return val


from run import main
main(input_fn=_mock_input)
