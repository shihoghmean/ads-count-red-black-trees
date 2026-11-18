Red-black Tree —— Research Project 4 的 code/ 说明（build & run）
================================================================

code/ 内部结构
--------------
src/          主程序源码，三个文件，C++17
  rbtree.h         计数表的声明：三张表 b/r/t 的含义与那条哨兵
  rbtree.cpp       两条递推的实现
  main.cpp         读入、调用计数、按题目格式输出；命令行入口
samples/      三组样例（题面那组 5->8，加两组最小与中等规模）
tools/        辅助脚本：暴力参考、生成器、对拍、基准、注释行统计
Readme.txt    本文件

浏览顺序：src/rbtree.h（先看文件头那段，把五条性质压成"黑高"这一步）→
src/rbtree.cpp（两条递推，各十来行）→ src/main.cpp（只是读写与自检）。

环境要求
--------
g++ 支持 C++17（实测 GCC 16.2.0 / MinGW-w64，Linux 的 g++ 同样可以）。
只用 C++17 标准库，不依赖任何第三方库。

tools/ 里的脚本都是 Python 3，只用标准库，不需要 numpy、matplotlib；
主程序本身不依赖它们，只编 C++ 也能跑完所有功能。

编译
----
源码是 C++17，扩展名 .cpp 与 .h。在本目录（code/）内一条命令，三个文件里编两个实现：

    g++ -O2 -std=c++17 -Wall -Wextra src/main.cpp src/rbtree.cpp -I src -o rbtcount.exe

-O2 必须保留：报告里的全部时间都是在这个优化级别下测的，换级别数字不可比。

如果拿到的是完整仓库（含仓库根的 CMakeLists.txt 与 CMakePresets.json），
也可以按仓库根 README.md 的说明用 CMake 构建，产物在 build/rbtcount.exe：

    cmake --preset default
    cmake --build --preset default

运行
----
输入格式（题面）：一个正整数 N（N ≤ 500），表示内部结点个数。
程序从标准输入读，往标准输出写一行，是答案对 1000000007 取模的结果。

下面的 "< 文件" 是 cmd 的重定向写法；在 PowerShell 里 "<" 不可用，等价写法是
    Get-Content samples\sample1.in | .\rbtcount.exe

1) 跑样例（在 code/ 内执行）：

       .\rbtcount.exe < samples\sample1.in
       .\rbtcount.exe < samples\sample2.in
       .\rbtcount.exe < samples\sample3.in

   sample1 是题面给的那组，输入 5，输出必须是 8；sample2 输入 1（单个黑根）；
   sample3 输入 10（164）。三组的参考输出在 samples\*.out。

2) 看耗时与乘法次数（往 stderr 打一行统计，stdout 的答案不受影响）：

       .\rbtcount.exe --stats < samples\sample1.in

   形如 n=5 time_ms=0.0000 mults=60（同样的例子换成 sample3 的 n=10 是 mults=330）。报告里的时间都来自这一行。

3) --repeat K（做计时实验用，正常求解不需要）：

       .\rbtcount.exe --stats --repeat 2000 < samples\sample1.in

   同一个 N 连算 K 次，报的是"平均一次的毫秒数"。Windows 上 clock() 的粒度是
   1 ms，单个 N 只要几微秒，不连算就只读得出 0。答案路径上它默认是 1，
   不会改变任何输出。

4) 内建自检（程序自带，不需要外部文件，十三个用例一起跑并逐个比对）：

       .\rbtcount.exe test

   输出逐条 ok / FAIL，末行 13/13 ok 才算过。n=1..12 的期望值来自暴力枚举
   （tools\brute.py），n=500 是规模上限、把当时的结果钉住防回归。

辅助脚本（tools/，在 code/ 或仓库根执行都可以：脚本自己按仓库根找 rbtcount.exe，
不挑当前目录；两种编译方式放在 build/ 或 code/ 下都能找到）
----------------------------------------------------------------------------------
    python tools\brute.py                 暴力参考：n=1..12，按形状数着色
    python tools\brute.py --full 8        最笨的一版：2^n 种着色全枚举（n=9 约 3 秒，n=10 约 20 秒）
    python tools\gen.py                   生成 19 个输入文件到 build\in\
    python tools\stress.py                对拍 n=1..12 与题面样例，末行给不符处数
    python tools\stress.py --full         对拍 n=1..10 的全枚举结果（慢，约 20 秒）
    python tools\bench.py                 跑报告第 3 章的规模表，输出 markdown
    python tools\stats.py                 统计 src/ 每个文件的行数与注释行比例

没有 Python 也不影响交作业：这些脚本只是复现测量与自查用的，主程序不需要它们。

数据
----
本题没有外部数据集，输入就是一个整数；bench.py 用的 N 由脚本里写死的列表给出，
随机用例由固定种子生成（gen.py 的 20261117），报告里的数字可以照上面的命令复现。
基准原始输出存在 documents/results/bench.md。
