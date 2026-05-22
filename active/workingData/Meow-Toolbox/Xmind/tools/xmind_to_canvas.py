"""
xmind_to_canvas.py - Xmind 轉 Obsidian Canvas 工具
排版：L1 節點由上往下排列，L2+ 向右延伸，L1 區塊間有明確間距
支援 boundaries（Xmind 圈選框）→ Canvas group 節點
節點寬高依文字量動態計算
"""

import json
import uuid
import sys
import os
import math

sys.path.insert(0, os.path.dirname(__file__))
from xmind_reader import read_xmind, get_root_topic

# ── 排版參數 ──────────────────────────────────────────
NODE_W_MIN     = 260   # 節點最小寬度
NODE_H         = 60    # 節點最小高度
CHARS_PER_LINE = 15    # 每行估算字數（CJK）
CHAR_W         = 14    # CJK 字元估算寬度（px），用於動態寬度計算
NODE_W_PAD     = 40    # 節點左右留白（寬度估算用）
LINE_H         = 22    # 每行文字高度（px）
NODE_V_PAD     = 20    # 節點上下留白

H_GAP_WIDE     = 240   # boundary 層以上：parent 右邊到 child 左邊的間距
H_GAP_NARROW   = 140   # 深層或無 boundary：parent 右邊到 child 左邊的間距
V_GAP          = 40    # 同層節點垂直間距
SECTION_GAP    = 192   # L1 區塊間額外間距
GROUP_PAD_X    = 16    # group 水平 padding（內縮）
GROUP_PAD_Y    = 8     # group 垂直 padding（< V_GAP/2）
GROUP_MARGIN   = 120   # group 向外的最小間距（CSS margin 概念），baked 進排版
NEST_PAD       = 14    # 巢狀 group 外框最小超出距離

L1_COLORS = ["4", "5", "3", "2", "6", "1"]  # 綠/藍/黃/橘/紫/紅


# ── 節點尺寸計算 ──────────────────────────────────────

def _node_height(title: str) -> int:
    """根據文字行數動態估算節點高度（+1 行緩衝補償 Canvas 渲染誤差）"""
    if not title:
        return NODE_H
    lines = title.split('\n')
    rows = 0
    for line in lines:
        stripped = line.strip()
        if stripped:
            rows += max(1, math.ceil(len(stripped) / CHARS_PER_LINE))
        else:
            rows += 1
    rows += 1  # 補一行緩衝，避免 Canvas 渲染時最後一行被截
    return max(NODE_H, rows * LINE_H + NODE_V_PAD)


def _node_width(title: str) -> int:
    """有換行字元時，依最長行字數動態延伸寬度，確保不折行"""
    if '\n' not in title or not title:
        return NODE_W_MIN
    lines = title.split('\n')
    max_chars = max((len(l.strip()) for l in lines if l.strip()), default=0)
    return max(NODE_W_MIN, max_chars * CHAR_W + NODE_W_PAD)


# ── Boundary 深度偵測 ─────────────────────────────────

def _find_boundary_depth(node: dict, depth: int = 0):
    """
    掃描樹狀結構，找出所有 boundary 涵蓋節點中最淺的深度。
    回傳 int（有 boundary）或 None（無 boundary）。
    """
    min_depth = None
    for bd in node.get('boundaries', []):
        start, end = _parse_range(bd.get('range', '(0,0)'))
        children = node.get('children', {}).get('attached', [])
        if children[start:end + 1]:
            d = depth + 1
            if min_depth is None or d < min_depth:
                min_depth = d
    for child in node.get('children', {}).get('attached', []):
        child_d = _find_boundary_depth(child, depth + 1)
        if child_d is not None:
            if min_depth is None or child_d < min_depth:
                min_depth = child_d
    return min_depth


# ── Boundary 邊界索引 ─────────────────────────────────

def _get_boundary_sets(node: dict):
    """
    回傳 (margin_before: set, margin_after: set)
    - margin_before[i]：第 i 子節點是某 boundary 的起點，前方需加 GROUP_MARGIN
    - margin_after[i]：第 i 子節點是某 boundary 的終點，後方需加 GROUP_MARGIN
    """
    children = node.get('children', {}).get('attached', [])
    margin_before, margin_after = set(), set()
    for bd in node.get('boundaries', []):
        start, end = _parse_range(bd.get('range', '(0,0)'))
        if children[start:end + 1]:
            margin_before.add(start)
            margin_after.add(end)
    return margin_before, margin_after


# ── 排版計算 ──────────────────────────────────────────

def _children_span(node: dict) -> int:
    """計算所有子節點的總高度，含 V_GAP 與 boundary 前後的 GROUP_MARGIN"""
    children = node.get('children', {}).get('attached', [])
    if not children:
        return 0
    margin_before, margin_after = _get_boundary_sets(node)
    n = len(children)
    total = 0
    if 0 in margin_before:
        total += GROUP_MARGIN
        # 第一個子節點有自己的子節點時，額外加 V_GAP，避免群組框標籤與內容重疊
        if children[0].get('children', {}).get('attached', []):
            total += V_GAP
    total += _subtree_height(children[0])
    for i in range(1, n):
        gap = V_GAP
        if (i - 1) in margin_after or i in margin_before:
            gap += GROUP_MARGIN
        total += gap + _subtree_height(children[i])
    if (n - 1) in margin_after:
        total += GROUP_MARGIN
    return total


def _subtree_height(node: dict) -> int:
    children = node.get('children', {}).get('attached', [])
    nh = _node_height(node.get('title', ''))
    if not children:
        return nh
    return max(nh, _children_span(node))


def _layout(node: dict, x: int, y: int, depth: int, color: str,
            nodes: list, edges: list, parent_id: str,
            h_step_fn):
    """
    遞迴擺放節點與連線。
    h_step_fn(depth) 回傳 parent 右邊到 child 左邊的間距（H_GAP）。
    child_x = x + nw + h_step_fn(depth)
    """
    nid = node.get('id') or str(uuid.uuid4())
    children = node.get('children', {}).get('attached', [])
    title = node.get('title', '').strip()  # 保留 \n 讓 Canvas 正確換行
    nh = _node_height(title)
    nw = _node_width(title)

    span = _children_span(node) if children else 0
    if not children:
        node_y = y
        children_start = y
    elif span >= nh:
        # 子節點群高度 >= 節點高度：節點置中於子節點群
        node_y = y + (span - nh) / 2
        children_start = y
    else:
        # 節點高度 > 子節點群高度：節點貼頂，子節點群向下置中
        node_y = y
        children_start = y + (nh - span) / 2

    entry = {
        "id": nid,
        "type": "text",
        "text": title,
        "x": round(x),
        "y": round(node_y),
        "width": nw,
        "height": nh,
    }
    if color:
        entry["color"] = color
    nodes.append(entry)

    if parent_id:
        edges.append({
            "id": str(uuid.uuid4()),
            "fromNode": parent_id,
            "fromSide": "right",
            "toNode": nid,
            "toSide": "left",
        })

    if not children:
        return

    margin_before, margin_after = _get_boundary_sets(node)
    child_x = x + nw + h_step_fn(depth)  # h_step_fn 回傳 H_GAP
    cur_y = children_start
    if 0 in margin_before:
        cur_y += GROUP_MARGIN
        # 對齊 _children_span：第一個子節點有子節點時額外加 V_GAP
        if children[0].get('children', {}).get('attached', []):
            cur_y += V_GAP
    for i, child in enumerate(children):
        _layout(child, child_x, cur_y, depth + 1, color,
                nodes, edges, nid, h_step_fn)
        gap = V_GAP
        if i in margin_after or (i + 1) in margin_before:
            gap += GROUP_MARGIN
        cur_y += _subtree_height(child) + gap


# ── Boundaries → Canvas Groups ────────────────────────

def _parse_range(range_str: str):
    s = range_str.strip('()')
    parts = s.split(',')
    return int(parts[0]), int(parts[1])


def _collect_boundaries(node: dict, result: list):
    for bd in node.get('boundaries', []):
        result.append((node, bd))
    for child in node.get('children', {}).get('attached', []):
        _collect_boundaries(child, result)


def _all_descendant_ids(node: dict) -> list:
    ids = [node.get('id')]
    for child in node.get('children', {}).get('attached', []):
        ids += _all_descendant_ids(child)
    return [i for i in ids if i]


def _build_groups(root: dict, node_pos: dict) -> list:
    raw_bds = []
    _collect_boundaries(root, raw_bds)
    groups = []
    for parent_node, bd in raw_bds:
        title = bd.get('title', '')
        start, end = _parse_range(bd.get('range', '(0,0)'))
        children = parent_node.get('children', {}).get('attached', [])
        covered = children[start:end + 1]
        if not covered:
            continue
        covered_ids = []
        for child in covered:
            covered_ids += _all_descendant_ids(child)
        positions = [node_pos[i] for i in covered_ids if i in node_pos]
        if not positions:
            continue
        min_x = min(p['x'] for p in positions) - GROUP_PAD_X
        min_y = min(p['y'] for p in positions) - GROUP_PAD_Y
        max_x = max(p['x'] + p['width'] for p in positions) + GROUP_PAD_X
        max_y = max(p['y'] + p['height'] for p in positions) + GROUP_PAD_Y
        groups.append({
            "id": str(uuid.uuid4()),
            "type": "group",
            "label": title,
            "x": round(min_x),
            "y": round(min_y),
            "width": round(max_x - min_x),
            "height": round(max_y - min_y),
        })
    return groups


def _ensure_nesting(groups: list):
    """確保外層 group 邊界比任何內層 group 多出至少 NEST_PAD px"""
    def contains(outer, inner):
        return (inner['x'] >= outer['x'] and inner['y'] >= outer['y'] and
                inner['x'] + inner['width'] <= outer['x'] + outer['width'] and
                inner['y'] + inner['height'] <= outer['y'] + outer['height'])

    changed = True
    while changed:
        changed = False
        for outer in groups:
            for inner in groups:
                if outer is inner or not contains(outer, inner):
                    continue
                if outer['x'] + outer['width'] < inner['x'] + inner['width'] + NEST_PAD:
                    outer['width'] = inner['x'] + inner['width'] + NEST_PAD - outer['x']
                    changed = True
                if outer['y'] + outer['height'] < inner['y'] + inner['height'] + NEST_PAD:
                    outer['height'] = inner['y'] + inner['height'] + NEST_PAD - outer['y']
                    changed = True
                if outer['x'] > inner['x'] - NEST_PAD:
                    diff = (inner['x'] - NEST_PAD) - outer['x']
                    outer['x'] += diff
                    outer['width'] -= diff
                    changed = True
                if outer['y'] > inner['y'] - NEST_PAD:
                    diff = (inner['y'] - NEST_PAD) - outer['y']
                    outer['y'] += diff
                    outer['height'] -= diff
                    changed = True


# ── 主轉換函式 ────────────────────────────────────────

def convert(xmind_path: str, canvas_path: str, sheet_index: int = 0) -> str:
    data = read_xmind(xmind_path)
    root = get_root_topic(data, sheet_index)
    nodes, edges = [], []

    # 偵測最淺 boundary 深度，決定每層 H_GAP
    d_boundary = _find_boundary_depth(root)
    if d_boundary:
        def h_step_fn(depth): return H_GAP_WIDE if depth < d_boundary else H_GAP_NARROW
    else:
        def h_step_fn(depth): return H_GAP_NARROW

    root_title = root.get('title', '').strip()
    root_nh = _node_height(root_title)
    root_nw = _node_width(root_title)

    l1_nodes = root.get('children', {}).get('attached', [])

    # 計算每個 L1 節點的 top y（與 _layout 邏輯一致），取中位數給 Root 對齊用
    l1_y_centers, cur_y = [], 0
    for i, child in enumerate(l1_nodes):
        if i > 0:
            cur_y += SECTION_GAP
        sh = _subtree_height(child)
        child_nh = _node_height(child.get('title', ''))
        child_span = _children_span(child) if child.get('children', {}).get('attached', []) else 0
        if not child.get('children', {}).get('attached', []) or child_span < child_nh:
            node_y = cur_y
        else:
            node_y = cur_y + (child_span - child_nh) / 2
        l1_y_centers.append(node_y)
        cur_y += sh + V_GAP

    n = len(l1_y_centers)
    root_y = l1_y_centers[n // 2] if n % 2 == 1 else (l1_y_centers[n // 2 - 1] + l1_y_centers[n // 2]) / 2

    root_id = root.get('id') or str(uuid.uuid4())
    nodes.append({
        "id": root_id,
        "type": "text",
        "text": root_title,
        "x": 0,
        "y": round(root_y),
        "width": root_nw,
        "height": root_nh,
    })

    # 擺放所有節點，depth=0 → L1
    cur_y = 0
    l1_x = root_nw + h_step_fn(0)
    for i, child in enumerate(l1_nodes):
        if i > 0:
            cur_y += SECTION_GAP
        color = L1_COLORS[i % len(L1_COLORS)]
        _layout(child, l1_x, cur_y, 1, color, nodes, edges, root_id, h_step_fn)
        cur_y += _subtree_height(child) + V_GAP

    node_pos = {n['id']: n for n in nodes if 'id' in n}
    groups = _build_groups(root, node_pos)
    _ensure_nesting(groups)
    nodes = groups + nodes

    canvas = {"nodes": nodes, "edges": edges}
    with open(canvas_path, 'w', encoding='utf-8') as f:
        json.dump(canvas, f, ensure_ascii=False, indent=2)
    return canvas_path


if __name__ == '__main__':
    if len(sys.argv) >= 3:
        print(f"output: {convert(sys.argv[1], sys.argv[2])}")
    else:
        print("usage: python xmind_to_canvas.py <input.xmind> <output.canvas>")
