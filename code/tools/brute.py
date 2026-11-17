"""暴力参考实现：不查任何表，对每个形状分别数合法着色。

两种模式，互相之间也不共享代码：

  默认      按形状逐点枚举颜色。子树的着色按（根颜色, 黑高）分组累计，
            红根只允许接黑根儿子，这是唯一在染色途中就能剪掉的约束。
  --full    最笨的一版：n 个点各染黑白两色，2^n 种全试一遍，最后整体检查五条性质。
            只在小 n 上跑（n=9 时 1430 个形状 x 512 种着色，够慢了），用来验证默认模式本身没写错。

输出格式：每行 "n answer"，方便和可执行程序的输出直接 diff。

    python tools/brute.py            # n=1..12，默认模式
    python tools/brute.py --full 8   # n=1..8，全枚举模式
"""
import sys
from functools import lru_cache


@lru_cache(maxsize=None)
def shapes(n):
    """所有 n 个内部结点的有序二叉树形状，用嵌套元组表示，None 是空树。"""
    if n == 0:
        return (None,)
    out = []
    for left in range(n):
        for a in shapes(left):
            for b in shapes(n - 1 - left):
                out.append((a, b))
    return tuple(out)


def ways(shape):
    """{（根颜色, 黑高）: 着色数}。黑高按题面定义：从根往下到 NULL 的黑点数，含 NULL 本身。"""
    if shape is None:
        # 空树是黑叶子，黑高 0。把它当成"黑根、黑高 0、只有一种着色"最省事。
        return {("B", 0): 1}
    left = ways(shape[0])
    right = ways(shape[1])
    out = {}
    for (lc, lh), lw in left.items():
        for (rc, rh), rw in right.items():
            if lh != rh:
                continue                      # 两条路径黑点数不等，这一对儿子直接作废
            key = ("B", lh + 1)               # 根黑：自己算一层黑高
            out[key] = out.get(key, 0) + lw * rw
            if lc == "B" and rc == "B":       # 根红：两个儿子必须都黑
                key = ("R", lh)
                out[key] = out.get(key, 0) + lw * rw
    return out


def count_shape(shape):
    """根必须黑，所以只收 "B" 那几种黑高。"""
    return sum(w for (c, h), w in ways(shape).items() if c == "B")


class Node:
    __slots__ = ("left", "right", "color")

    def __init__(self):
        self.left = None
        self.right = None
        self.color = 0      # 0 黑 1 红


def build(shape):
    """按形状造一棵独立的对象树。

    这里必须每个点都新建 Node，不能像早期版本那样把形状（嵌套元组）里的 None
    直接当节点键用：lru_cache 下所有空树都是同一个 None 对象，id() 会撞，
    一份着色会同时染到两个不相干的点上，数出来的数就全错了。
    """
    if shape is None:
        return None
    x = Node()
    x.left = build(shape[0])
    x.right = build(shape[1])
    return x


def all_nodes(root):
    out, st = [], [root]
    while st:
        x = st.pop()
        if x is None:
            continue
        out.append(x)
        st.append(x.left)
        st.append(x.right)
    return out


def valid(root):
    """整棵树检查五条性质里真正影响计数的那几条：根黑、红点儿子黑、黑高一致。"""
    if root is None or root.color == 1:
        return False

    def black_height(x):
        if x is None:
            return 0
        if x.color == 1 and ((x.left is not None and x.left.color == 1) or
                             (x.right is not None and x.right.color == 1)):
            raise ValueError("red-red")
        lh = black_height(x.left)
        rh = black_height(x.right)
        if lh != rh:
            raise ValueError("height")
        return lh + (0 if x.color == 1 else 1)

    try:
        black_height(root)
    except ValueError:
        return False
    return True


def count_shape_full(shape):
    """2^n 种着色全试一遍：这是"笨到不会错"的那一版，只给 n<=9 用。"""
    root = build(shape)
    ns = all_nodes(root)
    total = 0
    for mask in range(1 << len(ns)):
        for i, x in enumerate(ns):
            x.color = (mask >> i) & 1
        if valid(root):
            total += 1
    return total


def brute(n, full=False):
    fn = count_shape_full if full else count_shape
    return sum(fn(s) for s in shapes(n))


def main():
    args = sys.argv[1:]
    full = "--full" in args
    args = [a for a in args if a != "--full"]
    upto = int(args[0]) if args else 12
    for n in range(1, upto + 1):
        print(n, brute(n, full=full))


if __name__ == "__main__":
    main()
