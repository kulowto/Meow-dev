"""
xmind_to_canvas.py - Xmind 轉 Obsidian Canvas 工具
排版：L1 節點由上往下排列，L2+ 向右延伸，L1 區塊間有明確間距
支援 boundaries（Xmind 圈選框）→ Canvas group 節點
"""

import json
import uuid
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from xmind_reader import read_xmind, get_root_topic

# ── 排版參數 ──────────────────────────────────────────
NODE_W        = 260   # 節點寬度
NODE_H        = 60    # 節點高度
H_STEP_WIDE   = 420   # 有 boundary 時上層使用的水平間距
H_STEP_NARROW = 340   # 深層或無 boundary 時的水平間距
V_GAP         = 28    # 同層節點垂直間距
SECTION_GAP   = 64    # L1 區塊間額外間距
GROUP_PAD_X   = 16    # group 水平 padding（內縮）
GROUP_PAD_Y   = 8     # group 垂直 padding（< V_GAP/2）
GROUP_MARGIN  = 120   # group 向外的最小間距（CSS margin 概念），baked 進排版
NEST_PAD      = 14    # 巢狀 group 外框最小超出距離

L1_COLORS = ["4", "5", "3", "2", "6", "1"]  # 綠/藍/黃/橘/紫/紅


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
    # boundary 覆蓋首個子節點時，頂部保留 GROUP_MARGIN
    if 0 in margin_before:
        total += GROUP_MARGIN
    total += _subtree_height(children[0])
    for i in range(1, n):
        gap = V_GAP
        if (i - 1) in margin_after or i in margin_before:
            gap += GROUP_MARGIN
        total += gap + _subtree_height(children[i])
    # boundary 覆蓋末個子節點時，底部保留 GROUP_MARGIN
    if (n - 1) in margin_after:
        total += GROUP_MARGIN
    return total


def _subtree_height(node: dict) -> int:
    children = node.get('children', {}).get('attached', [])
    if not children:
        return NODE_H
    return max(NODE_H, _children_span(node))


def _layout(node: dict, x: int, y: int, depth: int, color: str,
            nodes: list, edges: list, parent_id: str,
            h_step_fn):
    """遞迴擺放節點與連線，h_step_fn(depth) 回傳當層水平間距"""
    nid = node.get('id') or str(uuid.uuid4())
    children = node.get('children', {}).get('attached', [])
    title = node.get('title', '').replace('\n', ' ').strip()

    if children:
        node_y = y + (_children_span(node) - NODE_H) / 2
    else:
        node_y = y

    entry = {
        "id": nid,
        "type": "text",
        "text": title,
        "x": round(x),
        "y": round(node_y),
        "width": NODE_W,
        "height": NODE_H,
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

    margin_before, margin_after = _get_boundary_sets(node)
    child_x = x + h_step_fn(depth)
    cur_y = y
    # boundary 覆蓋首個子節點時，頂部先空出 GROUP_MARGIN
    if children and 0 in margin_before:
        cur_y += GROUP_MARGIN
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

    # 偵測最淺 boundary 深度，決定 H_STEP 和 ROOT_X
    d_boundary = _find_boundary_depth(root)
    if d_boundary:
        root_x = -(d_boundary * (H_STEP_WIDE - H_STEP_NARROW))
        def h_step_fn(depth): return H_STEP_WIDE if depth < d_boundary else H_STEP_NARROW
    else:
        root_x = 0
        def h_step_fn(depth): return H_STEP_NARROW

    l1_nodes = root.get('children', {}).get('attached', [])

    # 計算每個 L1 節點的 y 座標，取中位數給 Root 用
    l1_y_centers, cur_y = [], 0
    for i, child in enumerate(l1_nodes):
        if i > 0:
            cur_y += SECTION_GAP
        sh = _subtree_height(child)
        node_y = cur_y + (sh - NODE_H) / 2 if sh > NODE_H else cur_y
        l1_y_centers.append(node_y)
        cur_y += sh + V_GAP

    n = len(l1_y_centers)
    root_y = l1_y_centers[n // 2] if n % 2 == 1 else (l1_y_centers[n // 2 - 1] + l1_y_centers[n // 2]) / 2

    root_id = root.get('id') or str(uuid.uuid4())
    root_title = root.get('title', '').replace('\n', ' ').strip()
    nodes.append({
        "id": root_id,
        "type": "text",
        "text": root_title,
        "x": round(root_x),
        "y": round(root_y),
        "width": NODE_W,
        "height": NODE_H,
    })

    # 擺放所有節點，depth=0 → L1 用 h_step_fn(0)
    cur_y = 0
    l1_x = root_x + h_step_fn(0)
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
