"""
inquiry_model — 結構化詢問工具 v0.2
用法：python run.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from core.decomposer import decompose
from core.questioner import run_pillar, run_pending
from core.synthesizer import synthesize
from core.recorder import new_session, save_markdown, save_json
from core.reality_checker import get_reality_question

BANNER = """
╔══════════════════════════════════════════╗
║       結構化詢問工具  v0.2               ║
║  金字塔原理 × 分而治之 × 問題追蹤器      ║
╚══════════════════════════════════════════╝
"""


def _ask_mode(input_fn=input) -> str:
    print("\n【模式選擇】")
    print("  1. explore（預設）：完整探索，含盲點揭露與視角擴展")
    print("  2. clean   ：潔淨語言，只跟著你說的方向走，不討論盲區")
    choice = input_fn("選擇模式（直接 Enter 為 explore）：").strip()
    return "clean" if choice in ("2", "clean") else "explore"


def _ask_reality_check(topic: str, mode: str, input_fn=input) -> str | None:
    """詢問使用者是否要做前置 Reality Check，回傳 summary 或 None"""
    print("\n【可選】是否要先說明一下你目前的狀況？（背景/已試過的/上次 AI 的進度）")
    do_check = input_fn("要（y）/ 跳過（直接 Enter）：").strip().lower()
    if do_check != "y":
        return None

    rc = get_reality_question(topic)

    print(f"\n  {rc.get('question_to_ask', '目前的狀況是什麼？')}")
    context_answer = input_fn("你的回答：").strip()
    if not context_answer:
        return None

    return context_answer


def _compile_pending(session: dict) -> list:
    """從所有 pillars 收集未解決的問題，加入 session 的 pending_questions"""
    pending = []
    for i, p in enumerate(session["pillars"], 1):
        if not p.get("resolved", True) and p.get("pending_followup"):
            pending.append({
                "pillar_index": i,
                "pillar_question": p["question"],
                "question": p["pending_followup"],
                "answer": None,
                "insight": "",
                "resolved": False,
            })
    return pending


def main(input_fn=input):
    print(BANNER)

    topic = input_fn("請輸入你想釐清的方向或主題：\n> ").strip()
    while not topic:
        topic = input_fn("> ").strip()

    mode = _ask_mode(input_fn)
    session = new_session(topic, mode)

    # 可選：Reality Check
    reality_summary = _ask_reality_check(topic, mode, input_fn)
    if reality_summary:
        session["reality_summary"] = reality_summary
        print(f"\n  ✓ 已記錄現況背景")

    print("\n  分析中，請稍候…")
    structure = decompose(topic, reality_summary or "")
    session["core_claim"] = structure["core_claim"]
    pillars_q = structure["pillars"]

    note = structure.get("note")
    if note and str(note).lower() not in ("null", "none", ""):
        print(f"\n  ℹ️  {note}")

    mode_label = "【潔淨語言模式】" if mode == "clean" else ""
    print(f"\n【核心主張】{session['core_claim']} {mode_label}")
    print("\n接下來依序詢問三個支柱問題，請盡量具體回答。")
    print("（每次只問一個問題，回答完再推進）\n")

    # 主詢問迴圈（三支柱）
    for i, q in enumerate(pillars_q, 1):
        pillar_data = run_pillar(i, q, mode, input_fn)
        session["pillars"].append(pillar_data)

    # 問題追蹤器：收集未解完的問題
    session["pending_questions"] = _compile_pending(session)

    if session["pending_questions"]:
        print(f"\n{'─' * 52}")
        print(f"  📋 有 {len(session['pending_questions'])} 個問題尚未完整討論：")
        for pq in session["pending_questions"]:
            print(f"     • [支柱 {pq['pillar_index']}] {pq['question']}")
        print(f"{'─' * 52}")
        cont = input_fn("\n要繼續處理這些問題嗎？（y / 直接 Enter 跳過）：").strip().lower()
        if cont == "y":
            resolved = run_pending(session["pending_questions"], mode, input_fn)
            session["pending_questions"] = resolved

    # 彙整
    print(f"\n{'═' * 52}")
    print("  彙整中，請稍候…")
    synthesis_md = synthesize(session)
    session["synthesis"] = synthesis_md

    print("\n" + synthesis_md)

    md_path = save_markdown(session, synthesis_md)
    save_json(session)
    print(f"\n{'─' * 52}")
    print(f"  已儲存：{md_path}")


if __name__ == "__main__":
    main()
