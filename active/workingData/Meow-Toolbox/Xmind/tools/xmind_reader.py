"""
xmind_reader.py - Xmind 讀寫工具
讀取、搜尋、修改、寫回 .xmind 檔案（content.json 格式）
"""

import zipfile
import json
import os
import uuid
from typing import Optional


# ── 讀取 ──────────────────────────────────────────────

def read_xmind(path: str) -> list:
    """解壓 .xmind，回傳 content.json 的原始 list（多工作表）"""
    with zipfile.ZipFile(path, 'r') as z:
        with z.open('content.json') as f:
            return json.load(f)


# ── 寫回 ──────────────────────────────────────────────

def write_xmind(src_path: str, data: list, out_path: Optional[str] = None) -> str:
    """
    將修改後的 data 打包回 .xmind。
    重建整個 ZIP，確保 content.json 不重複。
    out_path 不填則覆蓋原檔。
    """
    if out_path is None:
        out_path = src_path

    tmp_path = out_path + '.tmp'
    new_content = json.dumps(data, ensure_ascii=False, indent=2).encode('utf-8')

    with zipfile.ZipFile(src_path, 'r') as zin:
        with zipfile.ZipFile(tmp_path, 'w', zipfile.ZIP_DEFLATED) as zout:
            for item in zin.infolist():
                if item.filename == 'content.json':
                    zout.writestr(item, new_content)
                else:
                    zout.writestr(item, zin.read(item.filename))

    os.replace(tmp_path, out_path)
    return out_path


# ── 取得節點 ──────────────────────────────────────────

def get_root_topic(data: list, sheet_index: int = 0) -> dict:
    """取得指定工作表的根節點"""
    return data[sheet_index]['rootTopic']


def _walk(node: dict, result: list, depth: int = 0):
    """遞迴走訪，收集所有節點"""
    result.append({
        'id': node.get('id', ''),
        'title': node.get('title', ''),
        'depth': depth,
        'node': node,
    })
    for child in node.get('children', {}).get('attached', []):
        _walk(child, result, depth + 1)


def get_all_nodes(data: list, sheet_index: int = 0) -> list:
    """攤平所有節點，回傳 list of {id, title, depth, node}"""
    root = get_root_topic(data, sheet_index)
    result = []
    _walk(root, result)
    return result


def find_node(data: list, title: str, sheet_index: int = 0, fuzzy: bool = True) -> Optional[dict]:
    """依標題尋找節點（fuzzy=True 時部分比對），找不到回傳 None"""
    for item in get_all_nodes(data, sheet_index):
        if fuzzy:
            if title in item['title'] or item['title'] in title:
                return item['node']
        else:
            if item['title'] == title:
                return item['node']
    return None


# ── 修改節點 ──────────────────────────────────────────

def update_node(node: dict, title: Optional[str] = None, note: Optional[str] = None) -> dict:
    """
    修改節點標題或備註。
    直接修改傳入的 node dict（同步反映到原 data），回傳該節點。
    """
    if title is not None:
        node['title'] = title
    if note is not None:
        node['note'] = {'content': note}
    return node


def add_child(parent_node: dict, title: str, note: Optional[str] = None) -> dict:
    """在 parent_node 下新增子節點，回傳新節點"""
    new_node = {
        'id': str(uuid.uuid4()),
        'class': 'topic',
        'title': title,
    }
    if note:
        new_node['note'] = {'content': note}

    children = parent_node.setdefault('children', {})
    children.setdefault('attached', []).append(new_node)
    return new_node


# ── 顯示 ──────────────────────────────────────────────

def print_tree(data: list, sheet_index: int = 0, max_depth: int = 99):
    """在 terminal 印出可讀的樹狀結構"""
    def _print(node, depth=0):
        if depth > max_depth:
            return
        indent = '  ' * depth
        prefix = '●' if depth == 0 else '└─'
        title = node.get('title', '').replace('\n', ' / ')
        note_hint = ' [note]' if node.get('note') else ''
        print(f"{indent}{prefix} {title}{note_hint}")
        for child in node.get('children', {}).get('attached', []):
            _print(child, depth + 1)

    sheet_title = data[sheet_index].get('title', f'Sheet {sheet_index + 1}')
    print(f"[{sheet_title}]")
    _print(get_root_topic(data, sheet_index))
