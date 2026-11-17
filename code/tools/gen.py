"""生成测试输入：每个文件一个 n，写进 build/in/。

分三档，理由写在 gen 里而不是报告里：
  边界   1、2、3  —— 一个点、两个点（一个黑根加一个红儿子）、三个点（红叶子挂在黑根上）
  上限   255 256 499 500 —— 255 是黑高 8 能撑满的最小结点数，256 刚好撑不住，499/500 压规模上限
  随机   12 个种子固定的 n，用来看有没有哪个中间值特别慢

    python tools/gen.py            # 写进 build/in/，打印写了几个
"""
import os
import random

FIXED = [1, 2, 3, 255, 256, 499, 500]

def main():
    out = os.path.join("build", "in")
    os.makedirs(out, exist_ok=True)
    cases = [("edge", n) for n in FIXED[:3]]
    cases += [("bound", n) for n in FIXED[3:]]

    rng = random.Random(20261117)
    cases += [("rand", rng.randint(1, 500)) for _ in range(12)]

    for name, n in cases:
        with open(os.path.join(out, "%s-%d.in" % (name, n)), "w") as f:
            f.write("%d\n" % n)
    print("wrote %d cases to %s" % (len(cases), out))


if __name__ == "__main__":
    main()
