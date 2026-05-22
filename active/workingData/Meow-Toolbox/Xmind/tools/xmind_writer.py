"""
xmind_writer.py - 從整理結果建立 Xmind 檔案（工具四）
接收 xmind_organizer.organize() 回傳的 JSON 樹，打包成 .xmind 檔案。
解耦設計：整理邏輯在 organizer，格式轉換在此。
"""

import os
import sys
import uuid

sys.path.insert(0, os.path.dirname(__file__))
from xmind_reader import write_xmind


# ── JSON 樹 → Xmind topic ────────────────────────────

def _build_topic(node: dict) -> dict:
    """從整理結果的 dict 節點建構 Xmind topic dict，支援 note 與 boundaries"""
    topic = {
        "id": str(uuid.uuid4()),
        "class": "topic",
        "title": node.get("title", ""),
    }
    if note := node.get("note", ""):
        topic["note"] = {"content": note}
    children = node.get("children", [])
    if children:
        topic["children"] = {
            "attached": [_build_topic(c) for c in children]
        }
    # boundaries：從 JSON 帶入圈選框
    boundaries = node.get("boundaries", [])
    if boundaries:
        topic["boundaries"] = [
            {
                "id": str(uuid.uuid4()),
                "class": "boundary",
                "title": bd.get("title", ""),
                "range": bd.get("range", "(0,0)"),
            }
            for bd in boundaries
        ]
    return topic


# ── 主寫入函式 ────────────────────────────────────────

def build_xmind(organized: dict, src_path: str, out_path: str) -> str:
    """
    把 organize() 回傳的 JSON 樹寫成 .xmind 檔案。

    organized:  xmind_organizer.organize() 的回傳值
    src_path:   原始 .xmind 路徑（用來複製 ZIP 內其他資源）
    out_path:   輸出路徑

    回傳 out_path。
    """
    meta = organized.get("_meta", {})
    sheet_title = f"{meta.get('root_title', '整理後')}（整理版）"

    root_topic = _build_topic(organized)
    data = [{
        "id": str(uuid.uuid4()),
        "class": "sheet",
        "title": sheet_title,
        "rootTopic": root_topic,
    }]
    write_xmind(src_path, data, out_path)
    return out_path


if __name__ == "__main__":
    import json
    if len(sys.argv) < 4:
        print("usage: python xmind_writer.py <organized.json> <src.xmind> <out.xmind>")
        sys.exit(1)
    with open(sys.argv[1], encoding="utf-8") as f:
        organized = json.load(f)
    result = build_xmind(organized, sys.argv[2], sys.argv[3])
    print(f"output: {result}")
