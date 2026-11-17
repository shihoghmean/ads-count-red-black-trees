"""源码规模与注释密度，自查用。

按行判：处在 /* */ 里、或者这一行有 // 的行都算注释行；
既有代码又有注释的行只算一次。块注释的起止跨行，所以用一个小状态机走一遍。

    python tools/stats.py
"""
import os
import re

SRC = os.path.join("code", "src")


def classify(text):
    """返回 (总行数, 注释行数)。"""
    lines = text.splitlines()
    in_block = False
    comment = 0
    for line in lines:
        s = line.strip()
        if not s:
            continue
        hit = False
        i = 0
        while i < len(s) - 1:
            if in_block:
                hit = True
                if s[i] == "*" and s[i + 1] == "/":
                    in_block = False
                    i += 2
                else:
                    i += 1
            elif s[i] == "/" and s[i + 1] == "*":
                in_block = True
                hit = True
                i += 2
            elif s[i] == "/" and s[i + 1] == "/":
                hit = True
                break          # 行尾注释，整行记一次就够
            elif s[i] == '"':
                j = i + 1
                while j < len(s) and s[j] != '"':
                    j += 2 if s[j] == "\\" else 1
                i = j + 1
            else:
                i += 1
        if hit:
            comment += 1
    return len(lines), comment


def main():
    total = cmt = 0
    for name in sorted(os.listdir(SRC)):
        if not name.endswith((".h", ".cpp")):
            continue
        with open(os.path.join(SRC, name), encoding="utf-8") as f:
            n, c = classify(f.read())
        total += n
        cmt += c
        print("%-12s %5d 行  注释 %4d  %.1f%%" % (name, n, c, 100.0 * c / max(n, 1)))
    print("%-12s %5d 行  注释 %4d  %.1f%%" % ("合计", total, cmt, 100.0 * cmt / max(total, 1)))


if __name__ == "__main__":
    main()
