"""
xmind_organize_run.py - Xmind 整理工具 CLI 入口
usage: python xmind_organize_run.py <input.xmind> [output_path]
"""

import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(__file__))
from xmind_organizer import organize
from xmind_writer import build_xmind


def main():
    if len(sys.argv) < 2:
        print("usage: python xmind_organize_run.py <input.xmind> [output_path]")
        sys.exit(1)

    xmind_path = sys.argv[1]
    custom_out = sys.argv[2] if len(sys.argv) >= 3 else None
    base = os.path.splitext(xmind_path)[0] + "_organized"

    print("輸出格式？")
    print("  1. Canvas (.canvas)")
    print("  2. Xmind  (.xmind)")
    choice = input("選擇 [1/2，預設 1]：").strip() or "1"

    organized = organize(xmind_path)

    if choice == "2":
        out = custom_out or (base + ".xmind")
        build_xmind(organized, xmind_path, out)
        print(f"[done] Xmind 輸出：{out}")
    else:
        out = custom_out or (base + ".canvas")
        # 整理結果先寫臨時 xmind，再轉 canvas
        tmp_fd, tmp_path = tempfile.mkstemp(suffix=".xmind")
        os.close(tmp_fd)
        try:
            build_xmind(organized, xmind_path, tmp_path)
            from xmind_to_canvas import convert
            convert(tmp_path, out)
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
        print(f"[done] Canvas 輸出：{out}")


if __name__ == "__main__":
    main()
