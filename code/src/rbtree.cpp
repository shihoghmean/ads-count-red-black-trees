#include"rbtree.h"

/*
两条递推，都是从"根是什么颜色"这一个判断出来的：

  红根、黑高 h   : r[h][m] = Σ_{i+j=m-1} b[h][i] * b[h][j]
                   红点自己不贡献黑高，两个儿子必须都是黑根、黑高同为 h。

  黑根、黑高 h+1 : b[h+1][m] = Σ_{i+j=m-1} t[h][i] * t[h][j]
                   黑根贡献一层黑高，两个儿子的黑高同为 h，且各自可以是黑根或红根，
                   所以用 t。

下标对称，i 从 0 到 m-1、j=m-1-i，正好把 m-1 个结点全部分配给左右两棵子树。
m=1 时 i=j=0，两者都取"空树"，于是红根只有一个 NULL 儿子对（红叶子）算一种，
这正是 b[0][0]=1 那条哨兵在起作用的地方。
*/

Counter::Counter(int n):n(n),hmax(0),mults(0){
    if(n<=0) return;
    // 黑高 h 的树至少有 2^h-1 个内部结点（每一层黑点都满，h 层全黑是最省的形状）。
    // n ≤ 500 时 hmax ≤ 8；多留两层是给 b[h+1] 那一行留位置，省掉边界判断。
    while((1<<(hmax+1))-1<=n) hmax++;
    b.assign((size_t)hmax+2,vector<int>((size_t)n+1,0));
    r.assign((size_t)hmax+2,vector<int>((size_t)n+1,0));
    t.assign((size_t)hmax+2,vector<int>((size_t)n+1,0));
}

void Counter::build(){
    if(n<=0) return;

    // 空树当黑子树，黑高 0。这一行是整份代码里唯一一处"编出来"的边界，也是唯一错过的地方。
    b[0][0]=1;
    t[0][0]=1;

    // 逐层往上填：算 b[h+1] 之前，r[h] 和 t[h] 必须都已经定好，所以循环变量是儿子那一层。
    // 填表顺序反过来（先定黑根再算红根）会读到上一轮的旧值，数出来会偏小。
    for(int h=0;h<hmax;h++){
        // 红根：两个儿子都必须是黑根，所以只用 b[h] 这一层，不需要 t。
        for(int m=1;m<=n;m++){
            long long acc=0;
            for(int i=0;i<m;i++){
                acc+=(long long)b[h][i]*b[h][m-1-i];
                mults++;
                if((i&3)==3) acc%=MOD;   // 每 4 项取一次模：累加上界 4e18，还在 64 位里
            }
            r[h][m]=(int)(acc%MOD);
        }

        for(int m=0;m<=n;m++) t[h][m]=(b[h][m]+r[h][m])%MOD;

        // 黑根：两个儿子的黑高同为 h，颜色不限，所以用 t[h]。
        // i 从 0 扫到 m-1 而不是扫到 (m-1)/2：左右儿子互换是两棵不同的树（有序树），
        // 对称只能用来少写一遍乘法，不能用来去重。
        for(int m=1;m<=n;m++){
            long long acc=0;
            for(int i=0;i<m;i++){
                acc+=(long long)t[h][i]*t[h][m-1-i];
                mults++;
                if((i&3)==3) acc%=MOD;
            }
            b[h+1][m]=(int)(acc%MOD);
        }
    }
}

// 根必须是黑的，所以答案只把 b 那一族加起来；r[·][n] 是"根红"的树，题目不算。
// 同一批结点数下黑高可以不同（黑点密的树矮、黑点稀的树高），所以这一层循环不能省。
int Counter::solve(){
    long long ans=0;
    for(int h=0;h<=hmax;h++) ans+=b[h][n];
    return (int)(ans%MOD);
}

int count(int n){
    if(n<=0) return 0;
    Counter c(n);
    c.build();
    return c.solve();
}
