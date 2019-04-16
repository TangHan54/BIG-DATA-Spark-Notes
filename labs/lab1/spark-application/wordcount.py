# Reference: http://spark.apache.org/docs/2.1.0/api/python/index.html
# The command would be `spark-submit lab1.py in.txt outfile`
import re
import sys
from pyspark import SparkContext

if __name__ == "__main__":
    # instantiate a SparkConf Object
    
    # A SparkContext represents the connection to a Spark cluster, and can be used to create RDDs and broadcast variables on that cluster.
    sc = SparkContext()

    # Read a text file from HDFS, a local file system (available on all nodes), or any Hadoop-supported file system URI, and return it as an RDD of Strings.
    # sys.argv[1]: The second argument in the command line.
    lines = sc.textFile('s3://test-spark-application/in.txt')

    # split the text by all kinds of common delimitors.
    # flatMap: Return a new RDD by first applying a function to all elements of this RDD, and then flattening the results.
    words = lines.flatMap(lambda l: l.split())

    # The map function is to generate key-value pairs with key as the initial letter in lower case and ignore the non-letter character and value as 1.
    # map: Return a new RDD by applying a map function 
    pairs = words.map(lambda w: ((''.join([c for c in w if c.isalpha()]))[0].lower(),1))

    # reduceByKey: Merge the values for each key using an associative and commutative reduce function.
    # This will also perform the merging locally on each mapper before sending results to a reducer, similarly to a “combiner” in MapReduce.
    # Output will be partitioned with numPartitions partitions, or the default parallelism level if numPartitions is not specified. Default partitioner is hash-partition.
    counts = pairs.reduceByKey(lambda n1, n2: n1 + n2)

    # saved the result in distributed files.
    counts.saveAsTextFile('s3://test-spark-application/output')

    # stop the session
    sc.stop()
