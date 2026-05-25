from core.llm import ask
from frameworks.pyramid import SYNTHESIZE_SYSTEM


def _build_user_prompt(session: dict) -> str:
    lines = [f"主題：{session['topic']}", f"核心主張：{session['core_claim']}", ""]

    if session.get("reality_summary"):
        lines.append(f"現況背景：{session['reality_summary']}")
        lines.append("")

    for i, p in enumerate(session["pillars"], 1):
        lines.append(f"支柱 {i}：{p['question']}")
        lines.append(f"回答：{p['answer']}")
        for fq in p.get("followups", []):
            lines.append(f"  追問（深度 {fq.get('depth', '?')}）[{fq.get('question_type', '')}]：{fq['question']}")
            lines.append(f"  追問回答：{fq['answer']}")
            if fq.get("blind_spot"):
                lines.append(f"  盲點：{fq['blind_spot']}")
        if p.get("insight"):
            lines.append(f"洞見：{p['insight']}")
        if p.get("blind_spot"):
            lines.append(f"盲點：{p['blind_spot']}")
        lines.append("")

    if session.get("pending_questions"):
        lines.append("待續問題（未完整討論）：")
        for pq in session["pending_questions"]:
            lines.append(f"  - [支柱 {pq['pillar_index']}] {pq['question']}")

    return "\n".join(lines)


def synthesize(session: dict) -> str:
    """回傳完整的 Markdown 彙整字串"""
    return ask(SYNTHESIZE_SYSTEM, _build_user_prompt(session), max_tokens=2048)
