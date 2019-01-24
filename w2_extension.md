# Week 2 Extension. MapReduce and Spark

## Deficits of MapReduce
1. iterative jobs（迭代任务）: 很多常见的机器学习算法都反复地用到同一个数据集去优化参数。每一次迭代都可以被表示为一次MapReduced的任务，每次任务都需要从disk（磁盘）里重新读取，这就造成了巨大的代价。
2. interactive analytics（交互式分析）: Hadoop经常用于在很大的数据里通过SQL接口，比如说Pig和Hive，进行一些特定的探索性质的查询。理想状态下，用户应该能够加载他感兴趣的数据到memory（内存）并且进行多次查询。但是，使用Hadoop的过程中，每次查询都会产生大量的latency（延迟，十多秒）因为他是一个单独的MapReduce 任务，而且是从磁盘里读取数据的。
## Apache Spark
1. 是一个开源集群运算框架。相对于Hadoop的MapReduce会在运行完工作后将中介数据存放到磁盘中，Spark使用了存储器内运算技术，能在数据尚未写入硬盘时即在存储器内分析运算。Spark在存储器内运行程序的运算速度能做到比Hadoop MapReduce的运算速度快上100倍，即便是运行程序于硬盘时，Spark也能快上10倍速度。Spark允许用户将数据加载至集群存储器，并多次对其进行查询，非常适合用于机器学习算法。
2. Spark 项目核心：
    - Spark Core 和 RDD（Resilient Distributed Datasets 弹性分布式数据集
        - Spark Core是整个项目的核心, 提供项目调度，调度，和基本的I/O（input and output）功能。
        - 核心抽象（abstraction）： RDD, 一个只读，可以并行操作，有容错机制的数据合集。用户可以明确地将一个RDD缓存在不同机器的存储器中并且可以重复进行多个像MapReduce的多线程操作。
        - RDD最重要的特性就是，提供了容错性，可以自动从节点失败中恢复过来。即如果某个节点上的RDD partition，因为节点故障，导致数据丢了，那么RDD会自动通过自己的数据来源重新计算partition。这一切对使用者是透明的。
        - RDD的数据默认的情况下是存放在内存中的，但是在内存资源不足时，Spark会自动将RDD数据写入磁盘。(弹性的特性)
        - 在Spark里，每个RDD都由一个Scala对象表示。有四种办法来生成一个RDD：
            - 通过引用外部存储系统的数据集创建，比如说Hadoop Distributed File System （HDFS）
            - 通过并行化（paralleling）集合来创建RDD，Spark会将集合中的数据拷贝到集群上去，形成一个分布式的数据集合，也就是一个RDD。即：集合中的部分数据会到一个节点上，而另一部分数据会到其它节点上。然后就可以采用并行的方式来操作这个分布式数据集合。
            - 通过利用flatMap操作对已有的RDD转型。
            - 通过改变现有的RDD的持久性。 在默认情况下，RDD具有惰性并且短暂的。

## Reference
- [What is MapReduce?](https://www.ibm.com/analytics/hadoop/mapreduce)
- [Apache Spark](https://zh.wikipedia.org/wiki/Apache_Spark)
- [Scala (programming language)](https://en.wikipedia.org/wiki/Scala_(programming_language))
- [Spark: Cluster Computing with Working Sets](https://www.usenix.org/legacy/event/hotcloud10/tech/full_papers/Zaharia.pdf)
- [NIPS 2011 Big Learning - Algorithms, Systems, & Tools Workshop: Spark: In-Memory Cluster...](https://www.youtube.com/watch?v=qLvLg-sqxKc)
- [RDD的几种创建方式](https://blog.csdn.net/lemonZhaoTao/article/details/77923337)
