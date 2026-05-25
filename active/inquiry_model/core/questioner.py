from core.llm import ask
from core.json_utils import parse_json
from frameworks.pyramid import (
    FOLLOWUP_SYSTEM, followup_user_prompt,
    CLEAN_FOLLOWUP_SYSTEM, clean_followup_user_prompt,
)

MAX_DEPTH = 3
_START_DEPTH = 1

# 三驗證完成狀態（每個支柱獨立追蹤）
_VERIFY_TYPES = {"定義驗證", "方法驗證", "數據驗證"}


def _evaluate(question: str, answer: str, depth: int, verified: list, mode: str) -> dict:
    if mode == "clean":
        raw = ask(CLEAN_FOLLOWUP_SYSTEM, clean_followup_user_prompt(question, answer, depth))
    else:
        raw = ask(FOLLOWUP_SYSTEM, followup_user_prompt(question, answer, depth, verified))
    return parse_json(raw)


def run_pillar(index: int, question: str, mode: str = "explore", input_fn=input) -> dict:
    """
    互動詢問一個支柱（深度 1），回傳完整紀錄 dict。
    mode: "explore"（預設，含盲點/視角）或 "clean"（潔淨語言模式）
    """
    print(f"\n{'─' * 52}")
    print(f"  支柱 {index}  {question}")
    print(f"{'─' * 52}")

    answer = input_fn("你的回答：").strip()
    while not answer:
        answer = input_fn("請輸入回答：").strip()

    pillar = {
        "question": question,
        "answer": answer,
        "followups": [],
        "insight": "",
        "blind_spot": None,
        "resolved": False,
        "pending_followup": None,
    }

    current_depth = _START_DEPTH
    current_q = question
    current_a = answer
    verified = []  # 已完成的三驗證類型

    while current_depth < MAX_DEPTH:
        print("  思考中…", end="\r")
        eval_result = _evaluate(current_q, current_a, current_depth, verified, mode)
        print("          ", end="\r")

        # 更新洞見與盲點
        if eval_result.get("insight"):
            pillar["insight"] = eval_result["insight"]
        if eval_result.get("blind_spot") and mode != "clean":
            pillar["blind_spot"] = eval_result["blind_spot"]
            print(f"\n  ⚠️  盲點：{eval_result['blind_spot']}")

        # 記錄三驗證進度
        q_type = eval_result.get("question_type", "")
        if q_type in _VERIFY_TYPES and q_type not in verified:
            verified.append(q_type)

        if eval_result.get("sufficient", True):
            pillar["resolved"] = True
            break

        followup_q = eval_result.get("followup")
        if not followup_q:
            pillar["resolved"] = True
            break

        next_depth = current_depth + 1
        label = f" [{q_type}]" if q_type else ""
        print(f"\n  ↳ 追問（深度 {next_depth}）{label}：{followup_q}")
        followup_a = input_fn("你的回答：").strip()
        while not followup_a:
            followup_a = input_fn("請輸入回答：").strip()

        pillar["followups"].append({
            "question": followup_q,
            "answer": followup_a,
            "depth": next_depth,
            "question_type": q_type,
        })

        current_q = followup_q
        current_a = followup_a
        current_depth = next_depth

    # 到達深度上限，做最後一次評估看是否真的完整
    if current_depth >= MAX_DEPTH:
        print("  思考中…", end="\r")
        final = _evaluate(current_q, current_a, current_depth, verified, mode)
        print("          ", end="\r")

        if final.get("insight"):
            pillar["insight"] = final["insight"]
        if final.get("blind_spot") and mode != "clean" and not pillar["blind_spot"]:
            pillar["blind_spot"] = final["blind_spot"]
            print(f"\n  ⚠️  盲點：{final['blind_spot']}")

        if final.get("sufficient", True):
            pillar["resolved"] = True
        else:
            # 有未解完的問題：記錄進待續清單
            pillar["resolved"] = False
            pillar["pending_followup"] = final.get("followup")

    if pillar["insight"]:
        print(f"\n  💡 {pillar['insight']}")

    return pillar


def run_pending(pending_questions: list, mode: str = "explore", input_fn=input) -> list:
    """
    處理主迴圈結束後的待續問題。
    每個 pending 只問一輪（已在 MAX_DEPTH，不再往下挖）。
    回傳補充後的 pending_questions 清單。
    """
    results = []
    for pq in pending_questions:
        print(f"\n{'═' * 52}")
        print(f"  📌 待續問題（支柱 {pq['pillar_index']}）")
        print(f"  {pq['question']}")
        print(f"{'═' * 52}")

        answer = input_fn("你的回答：").strip()
        while not answer:
            answer = input_fn("請輸入回答：").strip()

        print("  思考中…", end="\r")
        eval_result = _evaluate(pq["question"], answer, MAX_DEPTH, [], mode)
        print("          ", end="\r")

        pq["answer"] = answer
        pq["insight"] = eval_result.get("insight", "")
        pq["resolved"] = True

        if pq["insight"]:
            print(f"\n  💡 {pq['insight']}")

        results.append(pq)

    return results
