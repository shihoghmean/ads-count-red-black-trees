"""规模与时间：固定一组 n，每个跑 REPEAT 次，取最小值和中间值。

时间来自程序自己的 --stats（clock() 计的 CPU 时间，只包住建表和求和）。
Windows 上 clock() 的粒度是 1 ms，单个 n 只有零点几毫秒，单跑一次读出来非 0 即 1。
所以先按 n 反推一个 repeat，让一个进程里的总计算量到毫秒级以上，再除以次数；
程序里 --repeat 就是这么用的，答案路径上它默认是 1。

    python tools/bench.py > documents/results/bench.md
"""
import os
import re
import statistics
import subprocess

# 三种构建方式的产物位置不同：CMake 落在仓库根 build/，code/Readme.txt 那条命令
# 落在 code/，直接从仓库根编的落在根目录。按顺序找第一个存在的，脚本就不挑 cwd。
_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(os.path.dirname(_HERE))


def find_exe():
    for rel in (("build", "rbtcount.exe"), ("code", "rbtcount.exe"), ("rbtcount.exe",)):
        p = os.path.join(_ROOT, *rel)
        if os.path.exists(p):
            return p
    raise SystemExit("找不到 rbtcount.exe：先按 README.md 或 code/Readme.txt 编译")


EXE = find_exe()
REPEAT = 7
NS = [10, 50, 100, 200, 300, 400, 500]
PAT = re.compile(r"time_ms=([0-9.]+) mults=(\d+)")


def repeat_for(n):
    """小 n 多算几遍，大 n 少算几遍：目标是每次进程里跑出百毫秒级的计算量。"""
    return max(1, min(50000, 200000 // n))


def run(n):
    rep = repeat_for(n)
    p = subprocess.run([EXE, "--stats", "--repeat", str(rep)],
                       input="%d\n" % n, capture_output=True, text=True)
    m = PAT.search(p.stderr)
    if not m:
        raise SystemExit("n=%d 没解析到统计: %s" % (n, p.stderr))
    return float(m.group(1)), int(m.group(2)), int(p.stdout.strip())


def main():
    print("| n | 黑高层数 | 乘法次数 | 中位 (ms) | 最小 (ms) | 答案 |")
    print("|---:|---:|---:|---:|---:|---:|")
    for n in NS:
        ts, mults, ans = [], 0, 0
        for _ in range(REPEAT):
            t, mults, ans = run(n)
            ts.append(t)
        ts.sort()
        # 黑高层数 = 最大的 h 使 2^h-1 <= n，和程序里 while 算的是同一个量
        hmax = (n + 1).bit_length() - 1
        print("| %d | %d | %d | %.4f | %.4f | %d |" % (
            n, hmax, mults, statistics.median(ts), ts[0], ans))


if __name__ == "__main__":
    main()
