import re
import sys
from pyspark import SparkConf, SparkContext

# instantiate a SparkConf Object
conf = SparkConf()
#  A SparkContext represents the connection to a Spark cluster, and can be used to create RDDs and broadcast variables on that cluster.
sc = SparkContext(conf=conf)
lines = sc.textFile(sys.argv[1])
words = lines.flatMap(lambda l: re.split(" ",l))
pairs = words.map(lambda w: (w, 1))
counts = pairs.reduceByKey(lambda n1, n2: n1 + n2)
counts.saveAsTextFile(sys.argv[2])
sc.stop()
