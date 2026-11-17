cmake_minimum_required(VERSION 3.20)
project(ads_count_red_black_trees LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

add_executable(rbtcount
    code/src/main.cpp
    code/src/rbtree.cpp
)
target_include_directories(rbtcount PRIVATE code/src)

# 固定 -O2：报告里的运行时间都在这个优化级别下测，换级别数字不可比。
target_compile_options(rbtcount PRIVATE -O2 -Wall -Wextra)
