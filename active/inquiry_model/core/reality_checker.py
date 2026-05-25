from core.llm import ask
from core.json_utils import parse_json
from frameworks.pyramid import REALITY_CHECK_SYSTEM, reality_check_user_prompt


def get_reality_question(topic: str, prior_context: str = "") -> dict:
    raw = ask(REALITY_CHECK_SYSTEM, reality_check_user_prompt(topic, prior_context))
    return parse_json(raw)
