# My First Spark Application
This is the very first spark application I developed using Python. This will include some very basic explanation.
```
import re
import sys
from pyspark import SparkConf, SparkContext
```

> instantiate a SparkConf Object
```
conf = SparkConf()
```

> A SparkContext represents the connection to a Spark cluster, and can be used to create RDDs and broadcast variables on that cluster.
```
sc = SparkContext(conf=conf)
```

>Read a text file from HDFS, a local file system (available on all nodes), or any Hadoop-supported file system URI, and return it as an RDD of Strings.\

> sys.argv[1]: The second argument in the command line.
```
lines = sc.textFile(sys.argv[1])
````

> flatMap: Return a new RDD by first applying a function to all elements of this RDD, and then flattening the results.
```
words = lines.flatMap(lambda l: re.split(" ",l))
```

> map: Return a new RDD by applying a function to each element of this RDD.
```
pairs = words.map(lambda w: (w, 1))
```
> reduceByKey: Merge the values for each key using an associative and commutative reduce function.\
This will also perform the merging locally on each mapper before sending results to a reducer, similarly to a “combiner” in MapReduce.\
Output will be partitioned with numPartitions partitions, or the default parallelism level if numPartitions is not specified. Default partitioner is hash-partition.
```
counts = pairs.reduceByKey(lambda n1, n2: n1 + n2)
```
```
counts.saveAsTextFile(sys.argv[2])
sc.stop()
```
