"""对拍：把可执行程序的答案和暴力参考逐个比。

    python tools/stress.py                 # n=1..12，和默认模式的暴力比
    python tools/stress.py --full          # n=1..10，和全枚举模式比（慢，20 秒左右）

另外顺带核两件事：题面样例 5 -> 8，以及程序在 n=1 这种最小输入上不许崩。
"""
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import brute

EXE = os.path.join("build", "rbtcount.exe")


def ask(n):
    p = subprocess.run([EXE], input="%d\n" % n, capture_output=True, text=True)
    if p.returncode != 0:
        raise SystemExit("n=%d 退出码 %d: %s" % (n, p.returncode, p.stderr.strip()))
    return int(p.stdout.strip())


def main():
    full = "--full" in sys.argv
    upto = 10 if full else 12
    bad = 0
    for n in range(1, upto + 1):
        want = brute.brute(n, full=full)
        got = ask(n)
        ok = want == got
        print("n=%-3d brute=%-8d program=%-8d %s" % (n, want, got, "ok" if ok else "DIFF"))
        bad += 0 if ok else 1

    sample = ask(5)
    ok = sample == 8
    print("sample 5 -> %d %s" % (sample, "ok" if ok else "DIFF"))
    bad += 0 if ok else 1

    print("%d/%d mismatch" % (bad, upto + 1))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
