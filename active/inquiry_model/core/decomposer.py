from core.llm import ask
from core.json_utils import parse_json
from frameworks.pyramid import DECOMPOSE_SYSTEM, decompose_user_prompt


def decompose(topic: str, reality_summary: str = "") -> dict:
    """回傳 {"core_claim": str, "pillars": [str, str, str], "note": str|None}"""
    raw = ask(DECOMPOSE_SYSTEM, decompose_user_prompt(topic, reality_summary))
    return parse_json(raw)
