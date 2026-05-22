"""
xmind_to_md.py - Xmind / 整理 JSON → Markdown 工具（工具五）
輸出可讀可編輯的 MD，供人工調整後再轉回 JSON/Xmind
"""

import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from xmind_reader import read_xmind, get_root_topic


# ── 核心渲染 ──────────────────────────────────────────

def _collect_boundaries(node: dict, path: str = "", result: list = None) -> list:
    """遞迴收集所有 boundary，回傳 list of dict"""
    if result is None:
        result = []
    raw_ch = node.get("children", [])
    children = raw_ch.get("attached", []) if isinstance(raw_ch, dict) else raw_ch
    for bd in node.get("boundaries", []):
        raw = bd.get("range", "(0,0)").strip("()")
        start, end = (int(x) for x in raw.split(","))
        covered = [
            c.get("title", "").replace("\n", " / ")
            for c in children[start:end + 1]
        ]
        result.append({
            "title": bd.get("title", "").replace("\n", " / "),
            "path": path or "（根節點）",
            "covered": covered,
        })
    node_title = node.get("title", "").replace("\n", " / ")
    next_path = f"{path} > {node_title}".lstrip(" > ")
    for child in children:
        _collect_boundaries(child, next_path, result)
    return result


def _node_to_lines(node: dict, depth: int, lines: list, inline_bd_titles: set):
    """遞迴將節點渲染成 MD 行"""
    title = node.get("title", "").replace("\n", " / ")
    note_obj = node.get("note")
    if isinstance(note_obj, dict):
        note = note_obj.get("content", "").strip()
    elif isinstance(note_obj, str):
        note = note_obj.strip()
    else:
        note = ""
    raw_ch = node.get("children", [])
    children = raw_ch.get("attached", []) if isinstance(raw_ch, dict) else raw_ch

    # boundary 標題 inline 標記（方括號附於標題）
    own_bd_labels = [
        bd.get("title", "").replace("\n", " / ")
        for bd in node.get("boundaries", [])
        if bd.get("title")
    ]
    label_suffix = ""
    if own_bd_labels:
        label_suffix = "  〔" + " / ".join(own_bd_labels) + "〕"

    if depth == 0:
        lines.append(f"# {title}")
    elif depth == 1:
        lines.append(f"\n## {title}{label_suffix}")
    elif depth == 2:
        lines.append(f"\n### {title}{label_suffix}")
    elif depth == 3:
        lines.append(f"\n#### {title}{label_suffix}")
    else:
        indent = "  " * (depth - 4)
        bullet = f"{indent}- {title}{label_suffix}"
        lines.append(bullet)

    if note:
        if depth >= 4:
            # 行內補充
            lines[-1] = lines[-1] + f"  ← {note}"
        else:
            lines.append(f"> {note}")

    for child in children:
        _node_to_lines(child, depth + 1, lines, inline_bd_titles)


# ── 主轉換函式 ────────────────────────────────────────

def convert_to_md(source, sheet_index: int = 0, out_path: str = None) -> str:
    """
    source: .xmind 路徑（str）或整理後的 JSON dict
    sheet_index: 工作表索引（僅 xmind 路徑時有效）
    out_path: 輸出路徑，不填只回傳字串
    """
    if isinstance(source, str):
        data = read_xmind(source)
        root = get_root_topic(data, sheet_index)
        src_name = os.path.basename(source)
    else:
        # 整理後的 JSON dict
        root = source
        src_name = source.get("_meta", {}).get("source", "organized.json")
        src_name = os.path.basename(src_name)

    lines = [
        "---",
        f"source: {src_name}",
        "---",
        "",
    ]

    inline_bd_titles: set = set()
    _node_to_lines(root, 0, lines, inline_bd_titles)

    # ── 圈選框彙整 ─────────────────────────────────────
    bds = _collect_boundaries(root)
    if bds:
        lines += [
            "\n---\n",
            "## 圈選框（Boundaries）\n",
            "| 標題 | 所在位置 | 涵蓋節點 |",
            "|------|---------|---------|",
        ]
        for bd in bds:
            covered_str = " / ".join(bd["covered"]) if bd["covered"] else "—"
            lines.append(f"| {bd['title']} | {bd['path']} | {covered_str} |")

    md = "\n".join(lines) + "\n"

    if out_path:
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(md)

    return md


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("usage: python xmind_to_md.py <input.xmind> <output.md>")
        sys.exit(1)
    result = convert_to_md(sys.argv[1], out_path=sys.argv[2])
    print(f"output: {sys.argv[2]}")
