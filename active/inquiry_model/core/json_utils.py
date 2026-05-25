import json
import re


def _fix_string_newlines(text: str) -> str:
    """把 JSON 字串值內的 literal 控制字元替換為跳脫版本"""
    result = []
    in_string = False
    i = 0
    while i < len(text):
        c = text[i]
        if c == '"' and (i == 0 or text[i - 1] != "\\"):
            in_string = not in_string
            result.append(c)
        elif in_string and c == "\n":
            result.append("\\n")
        elif in_string and c == "\r":
            result.append("\\r")
        elif in_string and c == "\t":
            result.append("\\t")
        else:
            result.append(c)
        i += 1
    return "".join(result)


def parse_json(raw: str) -> dict:
    """從 LLM 回應中穩健地提取 JSON，處理 ```json...``` 與控制字元問題"""
    # 直接解析
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        pass

    # 剝除 markdown code block 標記
    stripped = re.sub(r"^```(?:json)?\s*\n?", "", raw.strip())
    stripped = re.sub(r"\n?```\s*$", "", stripped)

    # 修正控制字元後解析
    try:
        return json.loads(_fix_string_newlines(stripped))
    except json.JSONDecodeError:
        pass

    # 找第一個 { 到最後一個 } 再試
    start = stripped.find("{")
    end = stripped.rfind("}") + 1
    if start >= 0 and end > start:
        try:
            return json.loads(_fix_string_newlines(stripped[start:end]))
        except json.JSONDecodeError:
            pass

    # 最終手段：移除字串值內所有控制字元（ASCII 0-31）
    cleaned = re.sub(
        r'"((?:[^"\\]|\\.)*)"',
        lambda m: '"' + re.sub(r'[\x00-\x1f]', ' ', m.group(1)) + '"',
        stripped
    )
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        pass

    raise ValueError(f"無法從回應中提取 JSON：{raw[:300]}")
