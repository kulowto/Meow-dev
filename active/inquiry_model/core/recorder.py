import json
from pathlib import Path
from datetime import datetime

SESSIONS_DIR = Path("D:/Meow-Env/Meow-Dev/active/inquiry_sessions")


def new_session(topic: str, mode: str = "explore") -> dict:
    return {
        "topic": topic,
        "mode": mode,
        "reality_summary": None,
        "core_claim": "",
        "pillars": [],
        "pending_questions": [],
        "synthesis": "",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }


def save_markdown(session: dict, synthesis_md: str) -> Path:
    SESSIONS_DIR.mkdir(exist_ok=True)
    safe_topic = session["topic"][:20].replace(" ", "_").replace("/", "-")
    date_str = datetime.now().strftime("%Y-%m-%d")
    filename = f"{date_str}_{safe_topic}.md"
    path = SESSIONS_DIR / filename

    mode_label = "（潔淨語言模式）" if session["mode"] == "clean" else ""
    header = f"# {session['topic']}{mode_label}\n討論時間：{session['timestamp']}\n\n"
    path.write_text(header + synthesis_md, encoding="utf-8")
    return path


def save_json(session: dict) -> Path:
    SESSIONS_DIR.mkdir(exist_ok=True)
    safe_topic = session["topic"][:20].replace(" ", "_").replace("/", "-")
    date_str = datetime.now().strftime("%Y-%m-%d")
    filename = f"{date_str}_{safe_topic}.json"
    path = SESSIONS_DIR / filename
    path.write_text(json.dumps(session, ensure_ascii=False, indent=2), encoding="utf-8")
    return path
