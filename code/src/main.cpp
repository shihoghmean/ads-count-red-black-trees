#include<bits/stdc++.h>
#include"rbtree.h"

/*
这个文件产出可执行程序 rbtcount，干两件事：读一个 n、按题目格式输出答案。

    rbtcount < case.in

另外留了一个 test 子命令跑内建自检（不打参数、不读文件）：

    rbtcount test

退出码只有 0 和 1：0 表示这一趟全对，1 表示读入失败、自检不过或者参数不对。

自检的期望值不是从递推里抄的，而是另一条路数出来的：tools/brute.py 把 n ≤ 10 的所有形状
和所有着色真枚举一遍（n=1..10 = 1,2,2,4,8,16,33,56,90,164）。两套实现各自独立，
写进这里当回归用例；n=500 那一条没有第三方可以对照，只能把当时算出来的数钉住，
防止以后改坏了没人发现。
*/

// 十二组内建用例。n ≤ 10 的期望值来自暴力枚举，n=5 还额外对上题面样例（8）。
// 500 是规模上限，钉住它是为了让任何改动引起的回归都能在 test 里立刻露头。
int runTest(){
    struct Case{int n;int want;};
    const Case cs[]={
        {1,1},{2,2},{3,2},{4,4},{5,8},{6,16},
        {7,33},{8,56},{9,90},{10,164},{11,330},{12,688},
        {500,905984258},
    };

    int bad=0;
    for(size_t k=0;k<sizeof(cs)/sizeof(cs[0]);k++){
        const int got=count(cs[k].n);
        const bool pass=(got==cs[k].want);
        // 一行一个用例、末尾打 fail 的原因：挂的那一条要能直接看见是哪一行，
        // 只打一个 "13/13" 的汇总，挂的时候还得再跑一遍才知道挂在哪。
        printf("n=%-4d want=%-12d got=%-12d %s\n",cs[k].n,cs[k].want,got,pass?"ok":"FAIL");
        if(!pass) bad++;
    }
    printf("%d/%d ok\n",(int)(sizeof(cs)/sizeof(cs[0]))-bad,(int)(sizeof(cs)/sizeof(cs[0])));
    return bad==0?0:1;
}

int main(int argc,char** argv){
    if(argc>1&&strcmp(argv[1],"test")==0) return runTest();

    bool stats=false;
    int repeat=1;
    for(int i=1;i<argc;i++){
        if(strcmp(argv[i],"--stats")==0) stats=true;
        // --repeat 只给实验用：同一个 n 连算 repeat 次，报"平均一次的毫秒数"。
        // 单个 n 只要零点几毫秒，而 Windows 上 clock() 的粒度是 1 ms，单跑一次读出来非 0 即 1，
        // 连算几十次把总时长顶到毫秒级以上才量得准。答案路径上默认 repeat=1，不改变任何行为。
        else if(strcmp(argv[i],"--repeat")==0&&i+1<argc) repeat=atoi(argv[++i]);
    }
    if(repeat<1) repeat=1;

    // 题面是一个文件一个 n，这里仍然写成"读到多少个数就答多少行"：
    // 判题时只进来一个数，行为一样；自己批量跑的时候省一次进程启动。
    // 用 scanf/printf 而不是 cin/cout：答案就是一个整数，stdio 足够，也省得再碰同步开关。
    vector<int> ns;
    int x;
    while(scanf("%d",&x)==1) ns.push_back(x);

    if(ns.empty()){
        fprintf(stderr,"usage: rbtcount [test] [--stats] < input\n");
        // 退出码和"读失败"走同一条：脚本只看退出码就能分清"输入没进来"和"答案不对"。
        return 1;
    }

    for(size_t k=0;k<ns.size();k++){
        const int n=ns[k];
        // 题面给的是正整数，0 和负数都属于输入坏了。这里直接报错退出，不返回 0——
        // 静默给个答案会让上游的对拍脚本把"读错了"当成"算对了"。
        if(n<=0){
            fprintf(stderr,"n must be positive, got %d\n",n);
            return 1;
        }
        // 计时只包住建表和求和。读入输出不算进去，否则报告里的微秒级读数会被 stdio 盖住。
        // clock() 拿的是进程 CPU 时间，同一台机器上连跑几十次比墙钟稳。
        const clock_t t0=clock();
        int ans=0;
        long long mults=0;
        for(int r=0;r<repeat;r++){
            Counter c(n);
            c.build();
            ans=c.solve();
            mults=c.mults;
        }
        const double ms=(double)(clock()-t0)*1000.0/CLOCKS_PER_SEC/repeat;

        // 输出严格一行一个整数，不带前后空行：判题机按行比对，多一个空行就算错。
        printf("%d\n",ans);

        // 统计走 stderr，所以带 --stats 时 stdout 仍然是干净答案，可以直接喂给对拍脚本。
        if(stats) fprintf(stderr,"n=%d time_ms=%.4f mults=%lld\n",n,ms,mults);
    }
    return 0;
}
