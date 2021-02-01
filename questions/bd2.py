#!/usr/bin/python
# -*- coding: utf-8 -*-
# __author__ : stray_camel
# __description__ : 
# __REFERENCES__ : 
# __date__: 2021/01/29 15
"""
存在n+1个房间，每个房间依次为房间1 2 3...i，每个房间都存在一个传送门，i房间的传送门可以把人传送到房间pi(1<=pi<=i),现在路人甲从房间1开始出发(当前房间1即第一次访问)，每次移动他有两种移动策略：
    A. 如果访问过当前房间 i 偶数次，那么下一次移动到房间i+1；
    B. 如果访问过当前房间 i 奇数次，那么移动到房间pi；
现在路人甲想知道移动到房间n+1一共需要多少次移动；
输入描述:
第一行包括一个数字n(30%数据1<=n<=100，100%数据 1<=n<=1000)，表示房间的数量，接下来一行存在n个数字 pi(1<=pi<=i), pi表示从房间i可以传送到房间pi。
输出描述:
输出一行数字，表示最终移动的次数，最终结果需要对1000000007 (10e9 + 7) 取模。
示例1
输入
复制
2
1 2
输出
4

从题目中，我们发现1<=pi<=i，说明我们只会被传送到当前房间之前的房间（包括当前房间）。所以当我们到i房间时，我们已经走过所有从第一个房间到第i-1个房间且均为偶数次。我们定义dp[i]表示从第一个房间达到第i个房间且为偶数次的移动次数。状态转移方程为dp[i] = dp[i-1] + (dp[i-1] - dp[tp[i-1] - 1] + 1) + 1. 

dp[i-1]是第一次到i-1房间的步数，第二次到i-1房间的步数则为第一次步数减去第一次到传送到的房间步数
"""


n = int(input())
tp = list(map(int, input().split()))
dp = [float("inf") for _ in range(n + 1)]
dp[0] = 0
 
mod = 1000000007
# dp[i]表示从第一个房间达到第i个房间且为偶数次的移动次数
for i in range(1, n+1):
    dp[i] = (dp[i-1] + (dp[i-1] - dp[tp[i-1] - 1] + 1) + 1) % mod
 
print(dp[-1])
