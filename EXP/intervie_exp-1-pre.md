
## 当前已做过的项目简述
入职一年左右，互联网行业，技术框架 flask后端+pg数据库+redis，后端开发
负责项目共五个，其中三个为独立一个人后端，两个为辅助后端
### 习得
- 数据库方面
    - 项目和数据库的链接主要是依靠字符串传输+sqlachemy
    - sql写的更加熟练了-基础优化点：
        >本科期间对数据库操作基本无，也涉及不到数据方便的优化或锻炼机会，此方面在入职后进步较大
        - 读写分离
        - 语法的优化，先将需要查询的数据分临时表 (with 语句或者 create temp table-再删除)
        - 索引构建，项目一般使用多个字符串/数字类型混合索引
        - 插入语法一般使用insert on conflict set
            批量插入分多个连接池 批量用一个session写入；
        - 数据库表的构建
            - 头表：主要维度-一般构建用于筛选框主要分类
                - 公司区域一般分 品牌-区域-多个级-门店-仓库/门店等
                - skc/sku的划分 品牌-产品季-产品线-大/中/小类-款-skc-sku等
                - （涉及到用户的一般可用用户区域/性别/年龄等划分，同理）
            - 行表：行表一般属于明细表
                - 公司/门店的行表一般是 区域-仓库/门店-最细粒度一般在1k-2k之间
                - 产品的行表一般是 skc/sku/product_code等-最细粒度一般在100k-200k之间
                - 最大数据量平均在 1m-2m (百万)
        - 数据库写入修改操作
            - 设计多个大表关联的掉异步，消息队列，（已开发独立的任务中心系统）
                - 对数据进行异步校验（是否正确-是否合理等校验）
                - 将数据写入redis缓存
                - 将数据写入数据库多张表
        - 数据库的查询操作
            - 数据分区域查询-比如表格数据表头和数据体一般分开查询，分页/滚动查询
                - 分页可分表，可用offset limit
            - 查询缓存若无则拉数据库同时缓存，key值为某个时间范围和筛选条件
    - inner join; left join/right join; join; full join 区别和性能?
    - sql执行的顺序?
        ```
        (8) SELECT (9)DISTINCT<Select_list>
        (1) FROM <left_table> (3) <join_type>JOIN<right_table>
        (2) ON<join_condition>
        (4) WHERE<where_condition>
        (5) GROUP BY<group_by_list>
        (6) WITH {CUBE|ROLLUP}
        (7) HAVING<having_condtion>
        (10) ORDER BY<order_by_list>
        (11) LIMIT<limit_number>
        ```
    - pgsql各个索引
        - https://developer.aliyun.com/article/111793
    - 公司有人在探索es系统，因为年底项目开发进度比较紧张还没开始
        - 个人认为/已有研究表明PG的性能是足以支撑现在的数据量的

- 底层项目的构建-分几个模块
    - 中间件的定义：
    - 数据校验对象的构造
    - 前后端相互传参-转成数据对象的中间件
    - CBV/FBV- 视图的构建
        - 构建装饰项目启动import时自动写入蓝图
        - 上述中间件也需要对返回json数据进行组装，并根据范围类型生成返回数据格式
        - 包装flask/django返回头
    - 底层模块
        - 工具模块
            - 数据转化-日期，算数等
        - 日志模块
    - 通过包分成不同的模块对应不同的功能

- 关于python
    > python对接的时高效率开发，性能方便缺失有不行，弱数据类型语言
    - python-golang的区别?

    - 基础python高效率的使用
        - 同功能中相对快的语法
            - dict(dict,**{})
            - map/filter
            - 生成式等
        - 可变对象不可变对象
        > 可变对象：list,dict.
        > 不可变对象有:int,string,float,tuple.
            - 描述就是引用后其子元素是否会随复制后的子类改变而改变
                - 最浅显的例子就是元组不可变
                - dict可变，引用（浅复制）后，修改复制后的子元素，父元素会改变
            - 可变对象dict使用比较多就用copy.deepcopy
            - 判断方法其实也比较简单，我一般是用的是是否能作为字典的key值
        - 垃圾回收机制
            - 计数回收-计数机制：python每个元素都是一个对象
                - 在创建-引用-传参-传入容器时+1
                - 在del-赋值-离开作用域-从容器删除时+1
                - 0 时销毁
                - 缺点：循环引用
                    -
                        ```
                        list1 = [] list2 = [] list1.append(list2) list2.append(list1)
                        ```
            - M * S，标记清除-GC算法
                - 对象之间通过指针连在一起，构成有向图，对象构成节点，而引用关系构成边
                - 根对象就是全局变量、调用栈、寄存器
                - 从根对象出发，沿着有向边遍历，可达的（reachable）对象标记，不可达的对象就是要被清除
                - 处理循环引用问题

    - pandas numpy
        - pandas使用的比较多
        - 常规apply-行-列；group by的使用
        - 合并 concat（列合并-排序使用比较多）；merge关联-使用比较多的场景-界面展示多个年份的数据，多线程查询 merge结果
        - melt/unstack使用比较多，特别是涉及到行表，头表的时候
            - 近期在北京出差 很多复杂的界面需要短时间开发出来都使用 很长的sql查询 结果数据用 pandas 的上述语法来进行处理
            - 高峰时间基本上两三天开发一个模块的主界面，后续一天开发一个子界面
            
    - 我个人对go还是很期待的
        - 就性能而言go对比java不相上下，而且go对分布式计算支持比pandas好很多，仔细地研究还没开始。
        - 公司也准备招java工程-整体转java，我个人也开始准备入手go，继续规划自己地职业道路了
    
    

## 网络通信
### socket编程的select和epoll函数
### tcp的拥塞机制


## 数据库
### 数据库三大范式，隔离级别
### pg数据库的索引


# OS系统

## 进程和线程的区别
## 各个排序算法
|排序方式|排序方法|时间复杂度 avg.|时间复杂度 max.|时间复杂度 min.|空间复杂度|举例|
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
|交换排序|冒泡排序|N^2|N^2|N|1| 比较相邻的元素。如果第一个比第二个大，就交换它们两个|
|交换排序|快速排序|nlogn|n^2|nlogn|nlogn||
|插入排序|简单的插入排序|n^2|n^2|n|1|第一个元素不管；取出下一个元素，在已经排序的元素序列中从后向前扫描；如果该元素（已排序）大于新元素，将该元素移到下一位置-直到找到已排序的元素小于或者等于新元素的位置|
|插入排序|希尔排序|n^1.3|n^2|n|1|设定好从n/2~2的步长，依次递减2，每个步长的两端进行顺序排序，一次遍历步长list，从而进行排序；也称为减小增量排序。|
|选择排序|简单选择排序|n^2|n^2|N|1| 找到最小（大）元素，放在起始位置，再从剩余中继续寻找最小（大）元素，然后放到已排序序列的末尾|
|选择排序|堆排序|nlogn|nlogn|nlogn|1|从原nums左向右，构建从上向下的不完全二叉树，再堆二叉树进行排序，大顶堆或者小顶堆，从小到大用大顶堆，从小到大用小顶堆|
|归并排序|简单归并排序|nlogn|nlogn|nlogn|n|把长度为n的输入序列分成两个长度为n/2的子序列；对这两个子序列分别采用归并排序（递归）；将两个排序好的子序列合并成一个最终的排序序列。--当归并排序排序三、四个元素的时候用的选择排序|
|归并排序|多路归并排序||||||
|非比较排序|计数排序|||||
|非比较排序|桶排序|||||
|非比较排序|基数排序|||||

[比较类算法vs非比较类算法](https://www.cnblogs.com/onepixel/articles/7674659.html)
![](https://cdn.learnku.com/uploads/images/202001/04/22893/oVXLJOpmg3.png!large)

- 冒泡排序
    - 比较相邻的元素。如果第一个比第二个大，就交换它们两个；针对所有的元素重复以上的步骤，除了最后一个；
    - 每一遍比较 最后一个总是最大的
- 快速排序
    - 假设一开始序列{xi}是：
        - [5]，3，7，6，4，1，0，2，9，10，[8]。
        - 此时，ref=5，i=1，j=11，从后往前找，第一个比5小的数是x8=2，因此序列为：[2]，3，7，6，4，1，0，[5]，9，10，8。
        - 此时i=1，j=8，从前往后找，第一个比5大的数是x3=7，因此序列为：2，3，[5]，6，4，1，0，[7]，9，10，8。
        - 此时，i=3，j=8，从第8位往前找，第一个比5小的数是x7=0，因此：2，3，[0]，6，4，1，[5]，7，9，10，8。
        - 此时，i=3，j=7，从第3位往后找，第一个比5大的数是x4=6，因此：2，3，0，[5]，4，1，[6]，7，9，10，8。
        - 此时，i=4，j=7，从第7位往前找，第一个比5小的数是x6=1，因此：2，3，0，[1]，4，[5]，6，7，9，10，8。
        - 此时，i=4，j=6，从第4位往后找，直到第6位才有比5大的数
        - 这时，i=j=6，ref成为一条分界线，它之前的数都比它小，之后的数都比它大，对于前后两部分数，可以采用同样的方法来排序。 

- 插入排序
    - 第一个元素不管；取出下一个元素，在已经排序的元素序列中从后向前扫描；如果该元素（已排序）大于新元素，将该元素移到下一位置-直到找到已排序的元素小于或者等于新元素的位置；
- 希尔排序
    - 希尔排序的排序思想在先将原序列划分成若干个子序列，其中划分的依据为按照间隔gap的大小分开。至于gap的选法可以不一样，我们以gap初始值选为序列总长度的一半为例。在每个子序列之内，使用直接插入排序（插入一个数字，前一个跟后一个相比，如果后一个值比前一个值小则调换两者之间的位置）。进行完第一轮排序之后，减小gap的大小，重复上述操作。由于间隔gap的值在不断减小，也称为减小增量排序，直到gap=1的时候，也就完成了整个序列的排序。
    ```
    a = [56,52,-96,-53,23,-789,520]    #测试案例
    b = len(a)                         #列表长度
    gap = b // 2                       #初始步长设置为总长度的一半
    while gap >= 1:
        for i in range (b):
            j = i
            while j>=gap and a[j-gap] > a[j]:   #在每一组里面进行直接插入排序
                a[j],a[j-gap] = a[j-gap],a[j]
                j-= gap
        gap=gap//2                              #更新步长
    print(a)
    ```
- 选择排序
    - 找到最小（大）元素，放在起始位置，再从剩余中继续寻找最小（大）元素，然后放到已排序序列的末尾
    - O(n2)
- 堆排序
    -堆排序（Heapsort）是指利用堆这种数据结构所设计的一种排序算法。堆积是一个近似完全二叉树的结构，并同时满足堆积的性质：即子结点的键值或索引总是小于（或者大于）它的父节点。堆排序可以说是一种利用堆的概念来排序的选择排序。分为两种方法：

    大顶堆：每个节点的值都大于或等于其子节点的值，在堆排序算法中用于升序排列；
    小顶堆：每个节点的值都小于或等于其子节点的值，在堆排序算法中用于降序排列；
    - https://www.runoob.com/w3cnote/heap-sort.html

- 归并排序
    - 把长度为n的输入序列分成两个长度为n/2的子序列；
    - 对这两个子序列分别采用归并排序（递归）；
    将两个排序好的子序列合并成一个最终的排序序列。
- 计数排序
    - 分别对每个数的个位数、十位数、、、等进行如下操作
    - 找到待排序的range(min,max+1)-构建字典key为 range(min,max+1)
    - 计数每个key的出现次数
    - 重新生成所有value
- 桶排序
- 基数排序
    - 基数排序是按照低位先排序，然后收集；再按照高位排序，然后再收集；依次类推，直到最高位。有时候有些属性是有优先级顺序的，先按低优先级排序，再按高优先级排序。最后的次序就是高优先级高的在前，高优先级相同的低优先级高的在前。
- 不得不说python sorted 的Timsort算法
    - 利用了归并排序与插入排序
    - TimSort 算法
        - 利用大多数据通常是有部分已经排好序的数据块的特点


## 其他面经

### session/cookie区别，作用，seesion存在哪

- cookie保存在C端，seesion保存在S端

session
简单的说，当你登陆一个网站的时候，如果web服务器端使用的是session，那么所有的数据都保存在服务器上，客户端每次请求服务器的时候会发送当前会话sessionid，服务器根据当前sessionid判断相应的用户数据标志，以确定用户是否登陆或具有某种权限。由于数据是存储在服务器上面，所以你不能伪造。

cookie
sessionid是服务器和客户端连接时候随机分配的，如果浏览器使用的是cookie，那么所有数据都保存在浏览器端，比如你登陆以后，服务器设置了cookie用户名，那么当你再次请求服务器的时候，浏览器会将用户名一块发送给服务器，这些变量有一定的特殊标记。服务器会解释为cookie变量，所以只要不关闭浏览器，那么cookie变量一直是有效的，所以能够保证长时间不掉线。

- Cookie可以存储在浏览器或者本地，Session只能存在服务器
- session 能够存储任意的 java 对象，cookie 只能存储 String 类型的对象
- Session比Cookie更具有安全性（Cookie有安全隐患，通过拦截或本地文件找得到你的cookie后可以进行攻击）
- Session占用服务器性能，Session过多，增加服务器压力
- 单个Cookie保存的数据不能超过4K，很多浏览器都限制一个站点最多保存20个Cookie，Session是没有大小限制和服务器的内存大小有关。

### CSRF攻击和django得CSRF攻击防御机制
[quote](https://www.jianshu.com/p/a178f08d9389)
> 攻击者获取到了用户的session，然后伪造用户请求。他说不太准确。事后查了一下：要让客户访问虚假网站，然后浏览器默认会带上cookie，虚假网站再直接向正规网站提交，伪造用户请求

1. 用户C打开浏览器，访问受信任网站A，输入用户名和密码请求登录网站A;

2. 在用户信息通过验证后，网站A产生Cookie信息并返回给浏览器，此时用户登录网站A成功，可以正常发送请求到网站A;

3. 用户未退出网站A之前，在同一浏览器中，打开一个TAB页访问网站B;

4. 网站B接收到用户请求后，返回一些攻击性代码，并发出一个请求要求访问第三方站点A;

5.浏览器在接收到这些攻击性代码后，根据网站B的请求，在用户不知情的情况下携带Cookie信息，向网站A发出请求。网站A并不知道该请求其实是由B发起的，所以会根据用户C的Cookie信息以C的权限处理该请求，导致来自网站B的恶意代码被执行。

> csrf的攻击之所以会成功是因为服务器端身份验证机制可以通过Cookie保证一个请求是来自于某个用户的浏览器，但无法保证该请求是用户允许的。因此，预防csrf攻击简单可行的方法就是在客户端网页上添加随机数，在服务器端进行随机数验证，以确保该请求是用户允许的。Django也是通过这个方法来防御csrf攻击的。

### tcp三次握手为什么握三次-进阶之如何确认序列号？
[quote](https://blog.csdn.net/boyaaboy/article/details/102520285)



### 线程池是什么作用，为什么要用线程池，你说说线程池的几个参数。
[quote](https://zhuanlan.zhihu.com/p/92632090#:~:text=1%20%E9%99%8D%E4%BD%8E%E8%B5%84%E6%BA%90%E6%B6%88%E8%80%97%E3%80%82%E7%BA%BF%E7%A8%8B%E6%98%AF%E6%93%8D%E4%BD%9C%E7%B3%BB%E7%BB%9F%E5%8D%81%E5%88%86%E5%AE%9D%E8%B4%B5%E7%9A%84%E8%B5%84%E6%BA%90%EF%BC%8C%E5%BD%93%E5%A4%9A%E4%B8%AA%E4%BA%BA%E5%90%8C%E6%97%B6%E5%BC%80%E5%8F%91%20...%202,%E6%8F%90%E9%AB%98%E5%93%8D%E5%BA%94%E9%80%9F%E5%BA%A6%E3%80%82%E5%BD%93%E8%AF%B7%E6%B1%82%E5%88%B0%E8%BE%BE%E6%97%B6%EF%BC%8C%E7%94%B1%E4%BA%8E%E7%BA%BF%E7%A8%8B%E6%B1%A0%E4%B8%AD%E7%9A%84%E7%BA%BF%E7%A8%8B%E5%B7%B2%E7%BB%8F%E5%88%9B%E5%BB%BA%E5%A5%BD%E4%BA%86%EF%BC%8C%20...%203%20%E6%8F%90%E9%AB%98%E7%BA%BF%E7%A8%8B%E7%9A%84%E5%8F%AF%E7%AE%A1%E7%90%86%E6%80%A7%E3%80%82%E7%BA%BF%E7%A8%8B%E6%98%AF%E7%A8%80%E7%BC%BA%E8%B5%84%E6%BA%90%EF%BC%8C%E5%BD%93%E5%88%9B%E5%BB%BA%E8%BF%87%E5%A4%9A%E7%9A%84%E7%BA%BF%E7%A8%8B%E6%97%B6%EF%BC%8C%E4%BC%9A%E9%80%A0%20)





IPv6？为什么 v4 不够？怎么缓解不够(子网，NAT)？还知道4和6哪些区别？


我？？？我面的不是后端吗？？

强答了一发智能家居智慧农业云计算边缘计算，然后面试官说"哦没事我只是好奇现在学校都在教什么"

= =满脸黑线

了解线程池吗？联系项目问了问？(淦基本不会)

如果你这个项目用到两个服务器？怎么通信？(卡了一会，答得不好)

MySql 隔离级别

可重复读是什么？幻影读？

项目里是怎么写事务的（就正常一条语句一事务，没优化)

什么时候注解不生效？(没了解)

MySql 是怎么存储数据的？(答了 InnoDB 和 MyISAM 的)

为什么是 B+ 树？

所有数据都在叶子节点吗？

1
select from user where a=1 order by update time desc limit 10 0
怎么建索引？((a,time) 和 (time))为什么？如果 a 只取 0 和 1 还是这么建吗？(只砍一半的话没必要索引，而且用日期是自然升序的更好)



自我介绍，做的项目的介绍，项目架构设计，
Dubbo原理介绍，netty原理介绍

hashMap原理，是线程安全的吗？为什么不安全。

redis缓存过期策略，准备同步，哨兵机制和集群的区别
算法题：leetcode394
给定一个经过编码的字符串，返回它解码后的字符串。

编码规则为: k[encoded_string]，表示其中方括号内部的 encoded_string 正好重复 k 次。注意 k 保证为正整数。

你可以认为输入字符串总是有效的；输入字符串中没有额外的空格，且输入的方括号总是符合格式要求的。

此外，你可以认为原始数据不包含数字，所有的数字只表示重复的次数 k ，例如不会出现像 3a 或 2[4] 的输入。

示例:

s = "3[a]2[bc]", 返回 "aaabcbc".
s = "3[a2[c]]", 返回 "accaccacc".
s = "2[abc]3[cd]ef", 返回 "abcabccdcdcdef".

二面:
算法在线编程：leetcode213
你是一个专业的小偷，计划偷窃沿街的房屋，每间房内都藏有一定的现金。这个地方所有的房屋都围成一圈，这意味着第一个房屋和最后一个房屋是紧挨着的。同时，相邻的房屋装有相互连通的防盗系统，如果两间相邻的房屋在同一晚上被小偷闯入，系统会自动报警。

给定一个代表每个房屋存放金额的非负整数数组，计算你在不触动警报装置的情况下，能够偷窃到的最高金额。

示例 1:
输入: [2,3,2]
输出: 3
解释: 你不能先偷窃 1 号房屋（金额 = 2），然后偷窃 3 号房屋（金额 = 2）, 因为他们是相邻的。

示例 2:
输入: [1,2,3,1]
输出: 4
解释: 你可以先偷窃 1 号房屋（金额 = 1），然后偷窃 3 号房屋（金额 = 3）。
偷窃到的最高金额 = 1 + 3 = 4 。

项目，主要做了什么，项目中碰到的问题有哪些，都市怎么解决？你觉得那个项目是最有挑战的

java多线程，线程池的选型，为什么要选这个，底层实现原理

三面:
你最熟悉的项目，做了什么，为什么这么做，怎么体现你项目的价值

让你来推广广告，你会怎么设计？

java基础问了些，JVM内存模型 G1和CMS垃圾回收器

如何中断线程，await和sleep区别

设计一个秒杀系统


本人非科班985渣硕。
字节跳动对数据结构和算法要求比较高，也会占较大的比重。基本不考语言的东西，这次面试的主要问mysql和redis。会对项目进行深挖。
一面（14：00 60min)
1.自我介绍
2.mysql事务，和隔离级别有哪些，仔细介绍一下
3. 丢失更新可以怎么解决？
4.什么是覆盖索引？
5.非聚簇索引怎么优化？
6. hyperloglog原理及用途？
7. 说一下https的过程
8. https里面证书的具体内容是什么？
9.https为什么采用混合加密？
9. redis的事务，说一下出现什么样的异常后面的语句还可以继续执行？
10. redis主从复制
11.算法题：输入两个字符串s1, s2，求和，求差。

二面(15：10 40min)
1.自我介绍；
2. 问项目的东西
3. 如何解决最后一个商品可能卖不出去？mysql减库存异常出现事务回滚。
4. MD5算加密算法吗？为什么加两次，加一次不可以吗。
5. MD5算不算加密算法；
6. 两个字符串hash后会得到同一个密文吗？如何解决hash冲突。
7. 说一下聚集索引和非聚集索引
8. 说一下hash索引，hash索引有什么优缺点；
9. 知道什么是组合索引吗？说一下怎么创建组合索引
10 .说一下，Next-lock锁：比如有这样一张表table ，事务的隔离级别为默认Repeatedly Read
id name
1 p1
2 p2
5 p5
如果我想插入一条数据：insert into table(id, name) values(6, p6)此时会加锁吗？如果加锁锁住的是哪些内容
如果现在执行查询操作：select * from table where id = 5 ;可以查询吗？
那这条查询语句可以查到结果吗？
select * from table where id = 5 for update;
11. 说一下mysql的优化，水平分表怎么做？按什么来分？
12. redis的事务不严谨，怎么优化一下？

算法题：
给两个数m,n 其中m表示1，2，3，4，5，…,m ，求在m中所有满足和等于n的组合
比如m = 5, n =6, 满足条件的结果有：[1,2,3], [1,5], [2,4]


作者：zzjjhh
链接：https://www.nowcoder.com/discuss/589920?type=all&order=time&pos=&page=1&channel=-1&source_id=search_all_nctrack
来源：牛客网

后端一面 2020.12.23 15:00
数组和链表的区别是什么，数组和链表在内存里是否是连续的，为什么数组可以用索引直接取数？（数组保存了数组起始的地址，索引是数组的偏移量，起始地址+偏移就可以直接定位到某一个位置的数了）
int和Integer的区别？int++和Integer++的区别？（这里是自动装箱和拆箱，没答出来，面试官温馨提示了一下）
HashMap的底层是否了解，get方法怎么比较两个key是否是相同的？
一个小代码题，ArrayList里有10000个数，删除里面的奇数（楼主用的奇葩的方式解决的，后来面试官提示这个考察Iterator的用法）
java的内存模型，方法区里有什么
进程、线程的区别，线程的工作内存里存放什么
用户态、内核态是如何切换的
网络是如何划分的？（7层网络模型），各个层的协议都有哪些？
TCP三次握手、四次挥手的过程，为什么要3次握手？
HTTP请求的内容，方式
GET、POST的区别
手写一个线程安全的单例
堆排的时间复杂度是多少，为什么？
面试官看到我简历上写了Android项目，问我对Android、Kotlin的了解（不是很了解），想不想转Android（当然想啦）
反问
一面面试官很棒，面试中有什么问题都会反馈并给与解答，一面的体验还是很不错的，很快HR就打电话约了二面的时间
后端二面 2020.12.23 18:00
二面面试官不讲武德，一上来就给了一道leetcode困难题，leetcode25.K个一组翻转链表https://leetcode-cn.com/problems/reverse-nodes-in-k-group/，

我大意了啊，没防住，做了半个小时测试用例只通过了50%，然后面试官让我回去再看看，又问了几个基础的面试题就结束了本次面试，楼主本以为二面凉了，后来接到了三面的电话。
后端三面 2020.12.25 18:00
自我介绍
问了简历上自己所写的项目，自己的工作内容（大概10分钟）
接着开始问我简历上写的“了解”的内容，因为只是“了解”，所以这一块被问惨了（小伙伴们简历这块要吸取我的教训啊，不懂的或了解不深的不要往简历上写），当时就觉得自己凉了一半。
问到了访问url的过程是什么
介绍一下数据库索引
反问环节
三面后大概过了一周，楼主问了HR面试的结果，果然还是凉了，不过HR问我愿不愿意换个岗位再试一试，不过要从一面开始，楼主还是很希望可以去字节实习的，所以就选择了再来一次。
客户端一面 2020.12.30 20:00
面试官看我简历上写了了解C和C++，就问了C++的构造函数、析构函数、复制构造函数、符号重载，并让我实现一下（我说平时java用的比较多，C和C++很久没看了，这个就跳过了）
算法题：用两个栈实现一个队列，leetcode232：https://leetcode-cn.com/problems/implement-queue-using-stacks/
算法题：两数之和，leetcode1：https://leetcode-cn.com/problems/two-sum/
手写一个生产者——消费者模型
了解Android的looper吗？（答不了解）
访问网址的过程
HTTP 1.1和2.0的区别，1.1是否是全双工的（答案是半双工）
HTTPS加密的过程
TCP的3次握手，4次挥手，为什么要3次握手？
客户端二面 2021.01.05 14:00
了解C和C++吗？（不了解）
实现一个单例模式，楼主准备动手时，面试官看到之前的面试写过单例了，就为了节省时间跳过了这个内容
java中可以作为GC Roots的有哪些？
输入url的过程
介绍一下DNS协议
一个TCP支持多少个HTTP？了解HTTP复用吗？
算法题：链表求和，https://leetcode-cn.com/problems/sum-lists-lcci/
算法题：回字形输出数组，比如说 1  2  3  要输出1,2,3,4,5,6,7,8,9
8  9  4
7  6  5
HashMap的底层了解吗，如何缓解哈希碰撞？
HTTP状态码有几类？
反问
客户端三面 2021.01.11 18:00
三面的内容不太记得了，只记得了一道算法题：寻找第一个缺失的正整数，leetcode41： https://leetcode-cn.com/problems/first-missing-positive/ ，用时间复杂度O(n)，空间复杂度O(1)的算法解决。
楼主当时第一时间想到了两种解法，但是时空复杂度不满足条件，给面试官说了思路，并实现了其中一种。然后面试官问有没有更好的解法，后来又想到了一种解法，但是由于紧张，没继续深入思考，后来被面试官提示我的想法是对的，问我为什么没有继续想下去 😂。
之后是一道智力题，64匹马问题，说出自己的思路。
最后是反问。

三面后第二天HR打电话聊了十几分钟，好像是HR面试，内容大概是自己的基本情况，以及能实习多长时间，目前拿到了哪些offer，为什么会选择字节，选择这个岗位等等。
2021.01.14晚上9点多HR打电话过来问我什么时候可以到岗，电话完就发了offer mail，开心~祝小伙伴们


作者：shencastle
链接：https://www.nowcoder.com/discuss/573473?type=all&order=time&pos=&page=1&channel=-1&source_id=search_all_nctrack
来源：牛客网

今晚上9点多收到了正式的邮件，距离HR面过去刚好一周，中途一直以为挂掉了😂
因为有同学在字节实习，所以一直鼓励我直接投简历，所以一开始就投了字节的广告部门，不过二面就挂掉了，运气好的是，第二天被数据平台部门的HR小姐姐给捞起来了（再度感谢），经过三轮面试也算是没辜负这一段时间的努力和身边各位同学的帮助，当然也有牛客上各位大佬的功劳。吃水不忘挖井人，我也来分享一下这几次面试经历吧 😁
广告部门
第一次面试（11.19 14:00）
因为我简历上主要写的语言是C++，所以上来先问了C++11的两个特性，lambda表达式和智能指针的理解，接着是问智能指针是否是线程安全的；然后是计网的经典问题，TCP/UDP区别，怎么确保TCP的可靠性，三次握手和四次挥手，为什么握手是三次而挥手需要四次；之后问了一个关于序列化的问题，当时没有回答上来因为确实没有接触过，面试官也一直在提醒但还是回答无果；接下来问到否接触过分布式，因为之前实验室有做过Redis相关的就提到了一些做过的业务内容，面试官提问怎么保证多个服务器之间的数据一致性，一开始没有回答出来，后面在面试官的引导下谈到了主从复制、写时修改；最后是一道算法题，实现LFU，之前刷题时遇到过，但是太久了很多细节忘记了，写了一会和面试官讲了思路，面试官说时间有限就先这样吧，但肯定了思路说等通知
10分钟后HR打来电话约到下午五点二面
第二次面试（11.19 17:00）
上来先问我的本科毕设（没想明白），接着就是一道海量数据处理的题（之前完全没有接触过的topN问题），1T的大文件，每一行是一个单词（可以进阶成随机字符串），请在4G的内存条件下统计出频次最高的10个单词。做法应该是先哈希取模保证每个单词分到同一个小文件中，然后分别统计每个小文件中的top10，最后使用排序（堆、归并等）得到原文件的top10；面试官看到我简历中提到有用过Vue，就问我Vue的基本工作原理，随后问是否看过Vue的底层代码实现。。我只能说没有；然后问了操作系统的组成是什么，应该是进程管理、内存管理、文件管理、设备管理，我却回答成cpu、内存、磁盘、设备IO😂；接着让介绍一下文件系统，很久之前看过相关的知识但是忘记了，所以仅凭些许碎片讲了inode，实际上什么也没回答出来😂；最后是一道算法题，合并n个有序数组，每个数组长度不一定相同，我当时想的是两两合并，总体用归并的思想，面试官问了空间复杂度，说性能不是很好。
二面结束后我也觉得这次面试基本结束了，结果不出所料😂
数据平台部门
第一次面试（11.22 14:00）
也是先问的C++的相关知识，智能指针和lambda表达式，auto关键字的用法（主要考察了能否只声明不初始化）； 然后问到python装饰器，我说python用的少面试官也就没再问；计网依旧问到了 TCP/UDP区别，我就一股脑把相关问题的回答顺便都说了一遍；数据库问到经典问题，何时该使用索引，隔离级别以及各自解决的问题（脏读、不可重复读、幻读等）；操作系统方面也是经典问题，select、poll、epoll的区别，进程和线程的区别，谈一谈页面置换算法；最后是两道算法题，不是很难，奇偶位置分别升序和降序的链表转化为升序链表、旋转数组找最小值（本来只有一道，但是第一道做完还有时间就又出了一道）。
10分钟后二面
第二次面试（11.22 15:10）
首先问了做过的一些项目，问的不深，看到有用C++写过服务端就问了IO多路复用和epoll适合的场景；看到有用过线程池所以就问到了生产者消费者模型，并手写实现，我用到条件变量和互斥锁，面试官提出两个疑问：生产者和消费者要用一把锁吗？单个生产者，多个消费者的情况下生产者还需要加锁吗？这两个问题大家可以仔细想一想，咱们可以互相交流一下；谈一谈你所知道的锁，我说了互斥锁和自旋锁，说到自旋锁时面试官就问到了它和互斥锁在工作机制上的区别；最后是阐述对C++中继承的理解。
10分钟后HR打来电话约到晚上七点半三面
第三次面试（11.22 19:30）
首先是进程线程的区别，谈到线程共享同一进程资源的时候面试官提问都有哪些资源，然后是进程间的通信方式，都是经典问题；再次问到 TCP/UDP区别 ，浏览器输入域名到页面返回的详细过程，也很经典；最后就直接一道算法题，找出n个长度相同的有序数组合并为一个有序数组后的中位数，我一开始也是笨办法两两合并的归并，面试官将问题简化为只找到两个有序数组合并后的中位数，不断提示可以优化后终于想到比O(n)更好的就是O(logn)，写出答案。

整体来讲不是很难，但是两个部门的二面都抓住一个点问的很深，最终拿到offer的部门也确实是给机会，所以我建议大家不要只看面经，学有遗力的同学一定要翻翻书，实习生面试的问题可能不会很难但是一定很广，加油冲冲冲！


作者：牛客444506407号
链接：https://www.nowcoder.com/discuss/589565?type=all&order=time&pos=&page=1&channel=-1&source_id=search_all_nctrack
来源：牛客网

广州某理工大学大四在读，考完研想找个实习，通过hr内推了简历，也是本人第一次工作面试，忘了录音，凭记忆写一下面经（2021.1.18）
从2点开始面试，三轮面试一个下午面试完
一面：（50min)
1 先做了自我介绍，大概讲了一下本科参与过校内acm比赛，一些数模奖学金等一般般的奖项，以及本科跟的实验室做的智能计算方面的研究
2 中间面试官看我提到acm就问了我算法相关的问题，因为我本身没有专门培训过acm，只是参与过校内的比赛，我就大概讲了一下从链表到图到dp和字符串的算法，面试官问了我kmp算法的实现，之前手写过这个代码，直接讲一遍next数组的实现
3 然后面试官开始问项目，我大概讲了一下简历上的项目，unix文件系统，网上商城，智能计算研究的交通流问题，主要聊了我最近在做的交通流问题，面试官问了项目分为哪几个部分， 本身我做项目没有分这么清楚，大概 分为路网设计及可视化，差分进化算法得最优解，基因编程算法得到的代理模型三个部分，他最后问了最后有没有什么直观的结果，当时我没有get到他的意思，后来三面面试官又问了差不多的问题，我才讲了我这个项目最终的结果和结论
4 ”那我们来做道题吧“，一道比较简单的dp问题，空间复杂度O(1)，时间复杂度O(n)，给定一个数组，求子数组的最大和（子数组连续，数组内有正有负），我本身牛客网上刷的题比较少再加上第一次面试有点紧张，开始愣了一会，然后想到思路就直接写出来了，面试官很nice，中间没有催促我，最后还提醒了一遍最大值变量初始化不应该为0
5 下面一些套路问题，socket编程的select和epoll函数；数据库三大范式，隔离级别；进程和线程的区别；tcp的拥塞机制；等等吧 牛客网上的面经都有
二面：（50min）
1 仍旧是自我介绍，讲到acm的时候，面试官问我当时比赛做了哪写题目，我确实是记不到了，都是大二参加的，他有些质疑我是否参加过acm...额，质疑有理吧，确实本科不算搞过acm，团体奖主要也是靠队友带飞
2 这次项目讲的比较细，感觉应该有半个小时都在聊项目，因为交通流优化的问题是我一个人在做，我把三块内容都详细讲了一下，可能面试官对我我后面两个部分不是很感兴趣，着重介绍了路网的设计与实现，中间提到了od对和迪杰特斯拉算法，面试官就问了我迪杰特斯拉算法的实现过程；unix文件系统让我介绍了一遍，大概就是超级块、i-node区、数据区，空闲块成组链表法，文件分配直接索引，一级索引，二级索引...，磁盘高速缓存等等
3 仍旧是做题部分，一道链表的题目，奇数位升序，偶数位降序，最终得到一个升序链表，我先写了一个反转链表的函数，然后两个指针分别指向两个升序链表，依次比较得到最终链表
leader面：(30min)
1 还是自我介绍
2 开始问了我数学建模中做的项目，这个确实也是不大记得了，我就说我可以详细介绍近期做的项目，也就是上面那个交通流问题，balabala一堆
3 算法题：做了一个括号匹配的问题，开始用的c++库里的vector，面试官要求自己实现一个栈，然后就手写了一个stack类
最后说等hr通知，过了一个小时不到hr就打电话通知面试成功
经验教训：简历里写的获奖项目一定要重点看啊，还有就是字节对算法的要求比较多吧，中间还有一些套路问题我答的不好，好像最后也没有影响太大，像tcp三次握手，四次挥手，http都没问，说明字节比较注重coding能力，也可能是只是实习岗位，要求没有这么多

那个，请你解释一下TCP的快恢复和传统的拥塞窗口控制有什么区别？（逆向面试）


## 其他

### 查找算法
- 暴力：遍历for循环
- 二分：前提-有序，
- 哈希：最高效
- 插值
- 索引：数据库
- bfs&dfs：图论内的遍历
- 平衡树
- **B+树**
- B-树
- **红黑树**
- **二叉搜索树**：