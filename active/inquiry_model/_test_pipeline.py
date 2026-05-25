"""完整 pipeline 測試腳本"""
import sys, time
sys.path.insert(0, ".")
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from core.decomposer import decompose
from core.synthesizer import synthesize
from core.recorder import new_session, save_markdown, save_json
from core.llm import ask
from core.json_utils import parse_json
from frameworks.pyramid import FOLLOWUP_SYSTEM, followup_user_prompt

topic = "learning efficiency improvement"

print("=== 完整 Pipeline 測試（ASCII topic）===")
print("主題：", topic)

# 1. Decompose
print()
print("[1/4] Decompose...")
structure = decompose(topic)
print("核心主張：", structure["core_claim"])
for i, p in enumerate(structure["pillars"], 1):
    print(f"  支柱 {i}：{p}")

session = new_session(topic, mode="explore")
session["core_claim"] = structure["core_claim"]

mock_answers = [
    "I spend 2 hours reading daily but get distracted easily and forget content",
    "I want to retain 80% of core concepts after reading a book",
    "I tried Pomodoro technique for a month but distraction issue persisted",
]

# 2. Followup
print()
print("[2/4] Followup 評估...")
for i, (q, a) in enumerate(zip(structure["pillars"], mock_answers), 1):
    time.sleep(2)  # 避免 rate limit
    raw = ask(FOLLOWUP_SYSTEM, followup_user_prompt(q, a, depth=1, verified=[]))
    ev = parse_json(raw)
    session["pillars"].append({
        "question": q, "answer": a, "followups": [],
        "insight": ev.get("insight", ""), "blind_spot": ev.get("blind_spot"),
        "resolved": ev.get("sufficient", True),
        "pending_followup": ev.get("followup") if not ev.get("sufficient") else None,
    })
    status = "✓" if ev.get("sufficient") else "→ 需追問"
    print(f"  支柱 {i} [{status}]: {ev.get('insight', '')[:70]}")

# 3. Synthesize
print()
print("[3/4] Synthesize...")
time.sleep(2)
md = synthesize(session)
print(md[:600], "...")

# 4. 存檔
print()
print("[4/4] 存檔...")
path = save_markdown(session, md)
save_json(session)
print("已儲存：", path)
print()
print("=== 全部通過 ===")
