# Red-Black Tree —— 数形状

ADS（数据结构基础）Research Project 4。题目：给正整数 $N\le 500$，问恰好 $N$ 个内部结点的红黑树有多少种，答案对 $10^9+7$ 取模。样例 `5 -> 8`。

解法只有两条卷积：把红黑树的五条性质压成「根黑、红点儿子黑、黑高一致」，用黑高把子树折成 $(h,n)$ 两个参数，然后逐层填表。$N=500$ 时 200 万次乘法、1.55 毫秒。

## 结构

```
code/src/       rbtree.h 计数表；rbtree.cpp 两条递推；main.cpp 读写与自检
code/samples/   三组样例（输入 + 参考输出）
code/tools/     brute.py 暴力参考（两版），gen.py 生成输入，stress.py 对拍，
                bench.py 规模实验，stats.py 行数与注释统计
documents/      report.tex / report.pdf，results/bench.md，打包用的 readme.txt
```

## 构建与运行

```bash
mkdir -p build
g++ -O2 -std=c++17 -Wall -Wextra code/src/main.cpp code/src/rbtree.cpp -I code/src -o build/rbtcount.exe
echo 5 | ./build/rbtcount.exe          # 8
./build/rbtcount.exe test              # 13/13 ok
```

也可以用 CMake（`CMakePresets.json` 走 Ninja）：

```bash
cmake --preset default
cmake --build --preset default
```

## 验证

- 题面样例 `5 -> 8`。
- 内建自检 13 条（$n=1\ldots12$ 加 $n=500$）。
- 与两个独立的暴力实现在 $n\le 12$ 上逐项一致（`--full` 那版全枚举到 $n=10$，跑 19 秒）。

## 报告

`documents/report.pdf`，9 页。数字都出自 `documents/results/bench.md` 与 `code/tools/` 里的命令。
