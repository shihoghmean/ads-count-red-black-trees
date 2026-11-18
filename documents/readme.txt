提交包内容与浏览顺序
====================

本包是 Research Project 4（Red-black Tree）的提交包，PR（互相评阅）阶段使用。
包内不写姓名、学号与组号：文件名里的 ## 是组号占位，等确认后由本人替换。

documents/（本目录）
--------------------
  wc_2026G##_P4.pdf     报告正文，8 页
  readme.txt            本文件
  results/bench.md      规模与时间的原始输出（程序 --stats 打出来的那张表）

code/
-----
  Readme.txt            编译与运行说明、参数、脚本清单
  src/                  源码三个文件（rbtree.h、rbtree.cpp、main.cpp）
  samples/              三组样例：输入 .in 与参考输出 .out
  tools/                Python 脚本：暴力参考、生成器、对拍、基准、行数统计

建议的浏览顺序
--------------
1. 先看 code/src/rbtree.h 的文件头：为什么"黑高"能代替形状。
2. 再看 code/src/rbtree.cpp 的两条递推，各十来行。
3. 报告第 1–2 章是问题与方程；第 3 章是验证（含两次数错的过程）；第 4 章是分析与局限。
4. 想复现数字就跑 code/Readme.txt 里列的命令，全流程不需要联网。

构建
----
包内 code/ 一条命令即可编译：

  g++ -O2 -std=c++17 -Wall -Wextra src/main.cpp src/rbtree.cpp -I src -o rbtcount.exe

然后在 code/ 里跑 `.\rbtcount.exe test`，末行应为 13/13 ok。
