"""
xmind_organizer.py - Xmind AI 語意整理工具（工具三）
讀取 Xmind 樹狀結構 → 轉文字 → AI 分類歸納 → 回傳標準化 JSON
輸出交由 xmind_writer.py（寫回 .xmind）或 xmind_to_canvas.py（Canvas）處理
"""

import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(__file__))
from xmind_reader import read_xmind, get_root_topic

_SCHEMA_DIR = os.path.join(os.path.dirname(__file__), "..", "schema")
_SPEC_PATH = os.path.join(_SCHEMA_DIR, "(Prompt) Xmind資訊整理Prompt規格.md")


# ── LLM 客戶端（可抽換平台） ───────────────────────────

class LLMClient:
    """
    統一 LLM 呼叫介面，支援抽換 provider。
    目前實作：anthropic（ANTHROPIC_API_KEY 環境變數）
    未來擴充：openai / gemini / local 等
    """
    DEFAULTS = {
        "anthropic": "claude-opus-4-7",
    }

    def __init__(self, provider: str = "anthropic", model: str = None):
        self.provider = provider
        self.model = model or self.DEFAULTS.get(provider, "")

    def chat(self, system: str, user: str) -> str:
        if self.provider == "anthropic":
            return self._call_anthropic(system, user)
        raise NotImplementedError(f"Provider '{self.provider}' 尚未實作")

    def _call_anthropic(self, system: str, user: str) -> str:
        import anthropic
        client = anthropic.Anthropic()  # 讀 ANTHROPIC_API_KEY
        msg = client.messages.create(
            model=self.model,
            max_tokens=4096,
            system=system,
            messages=[{"role": "user", "content": user}],
        )
        return msg.content[0].text


# ── Xmind 樹 → 文字（給 AI 讀） ──────────────────────

def tree_to_text(node: dict, depth: int = 0) -> str:
    """將 Xmind 節點遞迴轉為縮排文字，保留備註與 boundaries"""
    indent = "  " * depth
    title = node.get("title", "").replace("\n", " / ")
    note_obj = node.get("note")
    note = note_obj.get("content", "") if note_obj else ""
    line = f"{indent}- {title}"
    if note:
        line += f"  [備註: {note.strip()}]"
    parts = [line]

    # boundaries：記錄圈選框標題與涵蓋範圍
    for bd in node.get("boundaries", []):
        bd_title = bd.get("title", "").replace("\n", " / ")
        bd_range = bd.get("range", "")
        parts.append(f"{indent}  [boundary: \"{bd_title}\" {bd_range}]")

    for child in node.get("children", {}).get("attached", []):
        parts.append(tree_to_text(child, depth + 1))
    return "\n".join(parts)


# ── AI 回應解析 ───────────────────────────────────────

def _parse_response(raw: str) -> dict:
    """從 AI 回應中提取 JSON；支援 ```json...``` 區塊或裸 JSON"""
    match = re.search(r"```json\s*([\s\S]+?)\s*```", raw)
    if match:
        return json.loads(match.group(1))
    return json.loads(raw.strip())


# ── 載入 Prompt 規格 ──────────────────────────────────

def _load_system_prompt() -> str:
    try:
        with open(_SPEC_PATH, encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return _DEFAULT_PROMPT


_DEFAULT_PROMPT = """\
你是一位心智圖資訊整理專家。使用者會提供一份「發想中」的心智圖文字結構，請你：

1. 分析現有節點的語意與關係
2. 重新分類歸納，讓層次更清晰，同類合併、異類分開
3. 拆分語意過廣的節點，合併重複語意的節點
4. 在缺少說明的地方補充 note（備註），不需要說明的就不加
5. 保留所有原始資訊，不刪減重要內容

輸出規則：
- 只回傳一個 JSON 程式碼區塊，區塊外不要有任何其他文字
- 格式如下：
```json
{
  "title": "根節點標題",
  "children": [
    {
      "title": "分類標題",
      "note": "補充說明（選填）",
      "children": [...]
    }
  ]
}
```
- 以繁體中文命名節點
- 每層子節點建議不超過 7 個
- note 只有在有實質補充時才填，不要填廢話\
"""


# ── 主整理函式 ────────────────────────────────────────

def organize(
    xmind_path: str,
    sheet_index: int = 0,
    provider: str = "anthropic",
    model: str = None,
) -> dict:
    """
    讀取 Xmind → AI 整理 → 回傳標準化 JSON 樹。

    回傳格式：
    {
      "title": str,
      "children": [...],
      "_meta": {"source": str, "root_title": str}
    }
    """
    data = read_xmind(xmind_path)
    root = get_root_topic(data, sheet_index)
    text = tree_to_text(root)
    system = _load_system_prompt()
    client = LLMClient(provider=provider, model=model)

    print(f"[organizer] 呼叫 {client.provider} / {client.model}，整理中...")
    raw = client.chat(system, f"請整理以下心智圖內容：\n\n{text}")

    result = _parse_response(raw)
    result["_meta"] = {
        "source": xmind_path,
        "root_title": root.get("title", ""),
    }
    return result


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: python xmind_organizer.py <input.xmind>")
        sys.exit(1)
    import pprint
    out = organize(sys.argv[1])
    out.pop("_meta", None)
    pprint.pprint(out, width=80)
